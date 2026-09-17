#!/usr/bin/env python3
"""本科毕业设计（论文）PDF 反向测量。

期望值来自 docs/本科规格.md，并用 xduugthesis.cls 生成的 55 页实物论文自检。
"""

from __future__ import annotations

import argparse
from collections import Counter
import re
import sys
from pathlib import Path

import fitz

BP_PER_MM = 72 / 25.4


def mm(value: float) -> float:
    return value * BP_PER_MM


def lines(page: fitz.Page) -> list[dict]:
    result = []
    for block_index, block in enumerate(page.get_text("dict")["blocks"]):
        for line_index, line in enumerate(block.get("lines", [])):
            spans = line.get("spans", [])
            text = "".join(span["text"] for span in spans).strip()
            if not text or not spans:
                continue
            result.append(
                {
                    "text": text,
                    "x0": line["bbox"][0],
                    "x1": line["bbox"][2],
                    "y": spans[0]["origin"][1],
                    "size": spans[0]["size"],
                    "block": block_index,
                    "line": line_index,
                }
            )
    return result


def solid(dashes: object) -> bool:
    return dashes in (None, "", "[]", "[] 0")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("pdf", type=Path)
    parser.add_argument("--reference", action="store_true", help="同时核对 55 页实物论文分页基准")
    parser.add_argument("--stress", action="store_true", help="核对由真实论文转换出的压力测试稿")
    args = parser.parse_args()
    if args.reference and args.stress:
        parser.error("--reference 与 --stress 不能同时使用")

    doc = fitz.open(args.pdf)
    checks: list[tuple[str, bool, str]] = []

    def check(name: str, ok: bool, detail: str = "") -> None:
        checks.append((name, ok, detail))
        print(f"  {'✓' if ok else '✗'} {name}" + (f"：{detail}" if detail else ""))

    check("PDF 非空", len(doc) > 0, f"{len(doc)} 页")
    page_sizes = {(round(p.rect.width, 2), round(p.rect.height, 2)) for p in doc}
    check("A4 页面", page_sizes == {(595.28, 841.89)} or page_sizes == {(595.3, 841.9)}, str(page_sizes))

    all_lines = [lines(page) for page in doc]
    header_pages: list[tuple[int, fitz.Rect, float, object]] = []
    for index, page in enumerate(doc):
        for drawing in page.get_drawings():
            rect = drawing["rect"]
            if rect.width > mm(140) and rect.height < 1:
                header_pages.append((index + 1, rect, drawing["width"], drawing["dashes"]))
                break

    check("存在本科页眉单线", bool(header_pages), f"{len(header_pages)} 页")
    if header_pages:
        widths = [rect.width for _, rect, _, _ in header_pages]
        ys = [rect.y0 for _, rect, _, _ in header_pages]
        strokes = [stroke for _, _, stroke, _ in header_pages]
        check("页眉线宽 150mm", max(abs(width - mm(150)) for width in widths) <= mm(0.1),
              f"{min(widths):.2f}–{max(widths):.2f}bp")
        check("页眉线 y=23.15mm", max(abs(y - mm(23.15)) for y in ys) <= mm(0.15),
              f"{min(ys):.2f}–{max(ys):.2f}bp")
        check("页眉线 0.75pt 实线",
              all(abs(stroke - 0.75) <= 0.03 and solid(dashes) for _, _, stroke, dashes in header_pages),
              f"stroke={min(strokes):.3f}–{max(strokes):.3f}")

        odd = next(((pn, rect) for pn, rect, _, _ in header_pages if pn % 2 == 1), None)
        even = next(((pn, rect) for pn, rect, _, _ in header_pages if pn % 2 == 0), None)
        check("奇页正文边界 40–190mm", odd is not None and abs(odd[1].x0 - mm(40)) <= mm(0.1)
              and abs(odd[1].x1 - mm(190)) <= mm(0.1), repr(odd))
        check("偶页正文边界 20–170mm", even is not None and abs(even[1].x0 - mm(20)) <= mm(0.1)
              and abs(even[1].x1 - mm(170)) <= mm(0.1), repr(even))

    header_text = [line for page in all_lines for line in page
                   if line["y"] < mm(25) and abs(line["size"] - 10.5) < 0.1]
    page_numbers = [line for page in all_lines for line in page
                    if line["y"] < mm(25) and abs(line["size"] - 9) < 0.1]
    check("页眉宋体五号基线 21.7mm", bool(header_text)
          and max(abs(line["y"] - mm(21.7)) for line in header_text) <= mm(0.15))
    check("页码小五号与页眉同基线", bool(page_numbers)
          and max(abs(line["y"] - mm(21.7)) for line in page_numbers) <= mm(0.15))
    odd_numbers = [(pn, line) for pn, page in enumerate(all_lines, 1) for line in page
                   if pn % 2 == 1 and line in page_numbers]
    even_numbers = [(pn, line) for pn, page in enumerate(all_lines, 1) for line in page
                    if pn % 2 == 0 and line in page_numbers]
    check("奇页页码在外侧 190mm", bool(odd_numbers)
          and max(abs(line["x1"] - mm(190)) for _, line in odd_numbers) <= mm(0.15))
    check("偶页页码在外侧 20mm", bool(even_numbers)
          and max(abs(line["x0"] - mm(20)) for _, line in even_numbers) <= mm(0.15))

    title_lines = [line for page in all_lines for line in page
                   if abs(line["size"] - 16) < 0.1 and mm(40) < line["y"] < mm(46)]
    check("章和页面标题黑体三号", bool(title_lines), f"{len(title_lines)} 行")
    check("章和页面标题基线 42.8mm", bool(title_lines)
          and max(abs(line["y"] - mm(42.8)) for line in title_lines) <= mm(0.7),
          f"{min((line['y'] for line in title_lines), default=0):.2f}–{max((line['y'] for line in title_lines), default=0):.2f}bp")

    candidate_runs: list[float] = []
    for page in all_lines:
        ys = sorted({round(line["y"], 2) for line in page
                     if abs(line["size"] - 12) < 0.1 and line["y"] > mm(50)})
        for first, second in zip(ys, ys[1:]):
            delta = second - first
            if 18 <= delta <= 28:
                candidate_runs.append(delta)
    frequencies = Counter(round(delta, 1) for delta in candidate_runs)
    dominant = frequencies.most_common(1)[0][0] if frequencies else 0
    body_runs = [delta for delta in candidate_runs if round(delta, 1) == dominant]
    check("正文存在连续基线", len(body_runs) >= 2, f"主模态 {dominant:.1f}pt，共 {len(body_runs)} 组")
    check("正文 1.5 倍行距（23.4pt）", bool(body_runs)
          and max(abs(delta - 23.4) for delta in body_runs) <= 0.12,
          f"{min(body_runs, default=0):.2f}–{max(body_runs, default=0):.2f}pt")

    cover = all_lines[0]
    cover_main = [line for line in cover if "本科毕业设计" in line["text"]]
    check("封面主标题 42pt", bool(cover_main) and abs(cover_main[0]["size"] - 42) < 0.1)
    check("封面主标题基线 84.2mm", bool(cover_main)
          and abs(cover_main[0]["y"] - mm(84.2)) <= mm(0.2))
    cover_top = [line["y"] for line in cover if abs(line["size"] - 12) < 0.1 and line["y"] < mm(45)]
    check("封面班级/学号基线", len(cover_top) >= 2
          and any(abs(y - mm(28.2)) <= mm(0.2) for y in cover_top)
          and any(abs(y - mm(36.5)) <= mm(0.2) for y in cover_top))
    cover_fields = [line["y"] for line in cover if abs(line["size"] - 16) < 0.1 and line["y"] > mm(165)]
    expected_fields = [171.7, 188.2, 204.8, 221.3, 237.8, 254.3]
    check("封面题目与字段基线", len(cover_fields) >= 5 and all(
        any(abs(y - mm(expected)) <= mm(0.25) for y in cover_fields)
        for expected in (171.7, 204.8, 221.3, 237.8, 254.3)
    ), f"{len(cover_fields)} 行")

    chapter_pages = []
    for pn, page in enumerate(all_lines, 1):
        if any("章" in line["text"] and abs(line["size"] - 16) < 0.1
               and mm(40) < line["y"] < mm(46) for line in page):
            chapter_pages.append(pn)
    check("各章从右页开始", bool(chapter_pages) and all(pn % 2 == 1 for pn in chapter_pages), str(chapter_pages))

    texts = ["".join(line["text"] for line in page) for page in all_lines]
    if len(texts) >= 4:
        check("封面背面无页眉页码", not texts[1].strip())
        check("前置页码从 i 开始", re.search(r"(?:^|\D)i(?:\D|$)", texts[2]) is not None)
        check("前置偶页续为 ii", "ii" in texts[3])

    if not args.reference and not args.stress:
        full_text = "\n".join(texts)
        check("附录图编号独立", "图 A1" in full_text)
        check("附录公式编号独立", "(A-1)" in full_text)

        # 目录里的后置部分条目不得带章号：附录/参考文献/致谢的页面标题以
        # numbering: none 登记，目录条目必须与页面一致（官方实物论文同此）。
        toc_text = texts[6] if len(texts) > 6 else ""
        bad_entries = []
        for line in toc_text.split("\n"):
            for kw in ("附录", "参考文献", "致谢"):
                if re.search(r"第[一二三四五六七八九十]+章\s*" + kw, line):
                    bad_entries.append(line.strip()[:24])
        check("目录后置条目无章号", not bad_entries, "；".join(bad_entries))

        # 封面填写横线共 8 条：班级/学号 2 条（146.0~174.8mm）+ 题目 2 条与
        # 字段 4 条（82.1~166.8mm）。官方封面实测同此。
        cover_rects = []
        for drawing in doc[0].get_drawings():
            rect = drawing["rect"]
            if rect.width > mm(20):
                cover_rects.append((round(rect.x0 / 72 * 25.4, 1),
                                    round(rect.width / 72 * 25.4, 1)))
        top_rows = [r for r in cover_rects if abs(r[0] - 146.0) <= 0.5 and abs(r[1] - 28.8) <= 0.5]
        field_rows = [r for r in cover_rects if abs(r[0] - 82.1) <= 0.5 and abs(r[1] - 84.7) <= 0.5]
        check("封面填写横线 8 条", len(top_rows) == 2 and len(field_rows) == 6,
              f"班级/学号 {len(top_rows)} 条、题目与字段 {len(field_rows)} 条")

        # 官方标识不随包分发；默认封面必须以固定几何的占位框明确提示用户提供素材。
        wordmark_label = "请用户提供校名标准字图片"
        emblem_label = "请用户提供校徽图片"
        check("封面含校名标准字占位提示", len(doc[0].search_for(wordmark_label)) == 1)
        check("封面含校徽占位提示", len(doc[0].search_for(emblem_label)) == 1)
        drawings = [drawing["rect"] for drawing in doc[0].get_drawings()]

        def has_rect(x: float, y: float, width: float, height: float) -> bool:
            return any(
                abs(rect.x0 - mm(x)) <= mm(0.3)
                and abs(rect.y0 - mm(y)) <= mm(0.3)
                and abs(rect.width - mm(width)) <= mm(0.3)
                and abs(rect.height - mm(height)) <= mm(0.3)
                for rect in drawings
            )

        check("封面校名标准字占位框", has_rect(77.7, 49.5, 64.5, 12.04))
        check("封面校徽占位框", has_rect(89.0, 107.2, 42.1, 42.1))
    else:
        profile = "实物论文" if args.reference else "压力测试稿"
        check(f"{profile}总页数 55", len(doc) == 55)
        printed_starts = []
        for pn in chapter_pages:
            nums = [line["text"] for line in all_lines[pn - 1]
                    if abs(line["size"] - 9) < 0.1 and line["y"] < mm(25)]
            printed_starts.append(int(nums[0]) if nums and nums[0].isdigit() else None)
        check(f"{profile}章起始页", printed_starts == [1, 7, 19, 27, 41], str(printed_starts))
        references = set()
        for page in all_lines:
            for line in page:
                match = re.match(r"\[(\d+)\]", line["text"])
                if match:
                    references.add(int(match.group(1)))
        check(f"{profile}参考文献 27 条", references == set(range(1, 28)),
              f"{len(references)} 条")

    failures = [(name, detail) for name, ok, detail in checks if not ok]
    print(f"不合格：{len(failures)} / {len(checks)}")
    if failures:
        for name, detail in failures:
            print(f"  - {name}: {detail}", file=sys.stderr)
    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
