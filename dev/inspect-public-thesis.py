#!/usr/bin/env python3
"""只读抽查成品 PDF，输出可复核的版式观察值，不将第三方成品判为合格模板。"""
import argparse
from collections import Counter
import hashlib
import json
from pathlib import Path
import re

import fitz


def rows(page):
    for block in page.get_text("dict")["blocks"]:
        for line in block.get("lines", []):
            spans = [s for s in line["spans"] if s["text"].strip()]
            if spans:
                yield {
                    "x": spans[0]["origin"][0],
                    "y": spans[0]["origin"][1],
                    "size": max(s["size"] for s in spans),
                    "text": "".join(s["text"] for s in spans),
                }


def common(values):
    return Counter(round(v, 2) for v in values).most_common(3)


def inspect(path, start, count, scan=False):
    with fitz.open(path) as doc:
        if not 1 <= start <= len(doc) or count < 1:
            raise ValueError("正文物理起始页或抽样页数超出范围")
        result = {
            "file": path.name,
            "sha256": hashlib.sha256(path.read_bytes()).hexdigest(),
            "pages": len(doc),
            "page_size_bp": [round(doc[0].rect.width, 2), round(doc[0].rect.height, 2)],
            "producer": doc.metadata.get("producer"),
        }
        if scan:
            result["note"] = "扫描/OCR副本：不将文字层的字号、坐标当作原生排版值"
            return result
        headers, footers, steps = [], [], []
        left = {"odd": [], "even": []}
        rules = []
        for index in range(start - 1, min(start - 1 + count, len(doc))):
            page_rows = list(rows(doc[index]))
            headers += [r["y"] for r in page_rows
                        if 50 < r["y"] < 85 and 10 < r["size"] < 11 and len(r["text"]) > 3]
            footers += [r["y"] for r in page_rows if r["y"] > 775
                        and r["size"] < 11
                        and re.fullmatch(r"[0-9ivxlcdmIVXLCDM]+", r["text"].strip())]
            body = [r for r in page_rows if 145 < r["y"] < 755
                    and abs(r["size"] - 12) < .1 and len(r["text"]) > 25]
            ys = sorted({round(r["y"], 3) for r in body})
            steps += [b - a for a, b in zip(ys, ys[1:]) if 15 < b - a < 26]
            side = "odd" if (index - start + 2) % 2 else "even"
            left[side] += [r["x"] for r in body]
            if index == start - 1:
                for drawing in doc[index].get_drawings():
                    rect = drawing["rect"]
                    if rect.width > 350 and rect.height < 2 and 50 < rect.y0 < 90:
                        rules.append({
                            "x0": round(rect.x0, 2), "x1": round(rect.x1, 2),
                            "y": round(rect.y0, 2), "width": round(drawing["width"], 3),
                            "dashes": drawing["dashes"],
                        })
        result.update({
            "sample_physical_pages": [start, min(start - 1 + count, len(doc))],
            "header_baseline_bp": common(headers),
            "footer_baseline_bp": common(footers),
            "body_baseline_steps_bp": common(steps),
            "body_left_bp": {k: common(v) for k, v in left.items()},
            "chapter_first_page_header_rules": rules,
            "note": "众数及次数仅为观察；正文按长行筛选，短页可能没有足够样本，不作逐页复现判断",
        })
        return result


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("pdf", type=Path)
    parser.add_argument("--chapter-page", type=int, required=True,
                        help="第一章起始物理页，从1计数")
    parser.add_argument("--pages", type=int, default=10)
    parser.add_argument("--scan", action="store_true")
    args = parser.parse_args()
    print(json.dumps(inspect(args.pdf, args.chapter_page, args.pages, args.scan),
                     ensure_ascii=False, indent=2))
