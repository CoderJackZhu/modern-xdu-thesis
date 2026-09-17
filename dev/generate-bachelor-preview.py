#!/usr/bin/env python3
"""从本科完整示例 PDF 生成 README 使用的三页并排预览图。"""

from __future__ import annotations

import argparse
from pathlib import Path

import fitz


SCALE = 0.92
GAP = 24
PAGES = (0, 6, 8)  # 封面、目录、第一章


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("pdf", type=Path)
    parser.add_argument("output", type=Path)
    args = parser.parse_args()

    document = fitz.open(args.pdf)
    if len(document) <= max(PAGES):
        parser.error(f"PDF 只有 {len(document)} 页，至少需要 {max(PAGES) + 1} 页")

    pages = [
        document[index].get_pixmap(matrix=fitz.Matrix(SCALE, SCALE), alpha=False)
        for index in PAGES
    ]
    if len({page.height for page in pages}) != 1:
        parser.error("所选页面高度不一致")

    width = sum(page.width for page in pages) + GAP * (len(pages) - 1)
    height = pages[0].height
    gap = b"\xff\xff\xff" * GAP
    rows = []
    for y in range(height):
        parts = []
        for page in pages:
            start = y * page.stride
            parts.append(page.samples[start:start + page.width * page.n])
        rows.append(gap.join(parts))
    preview = fitz.Pixmap(fitz.csRGB, width, height, b"".join(rows), False)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    preview.save(args.output)
    print(f"已生成 {args.output}（{width} × {height}px，页码 1/7/9）")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
