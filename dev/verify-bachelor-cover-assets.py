#!/usr/bin/env python3
"""验收本科封面的用户素材与无素材占位符。"""

from __future__ import annotations

import argparse
from pathlib import Path

import fitz


BP_PER_MM = 72 / 25.4
WORDMARK_LABEL = "请用户提供校名标准字图片"
EMBLEM_LABEL = "请用户提供校徽图片"


def mm(value: float) -> float:
    return value * BP_PER_MM


def page_text(page: fitz.Page) -> str:
    return "".join(block[4] for block in page.get_text("blocks"))


def matching_rect(page: fitz.Page, expected: tuple[float, float, float, float]) -> bool:
    x, y, width, height = (mm(value) for value in expected)
    for drawing in page.get_drawings():
        rect = drawing["rect"]
        if (
            abs(rect.x0 - x) <= mm(0.3)
            and abs(rect.y0 - y) <= mm(0.3)
            and abs(rect.width - width) <= mm(0.3)
            and abs(rect.height - height) <= mm(0.3)
        ):
            return True
    return False


def label_in_region(page: fitz.Page, label: str, region: tuple[float, float, float, float]) -> bool:
    hits = page.search_for(label)
    if len(hits) != 1:
        return False
    x, y, width, height = (mm(value) for value in region)
    center = fitz.Point((hits[0].x0 + hits[0].x1) / 2, (hits[0].y0 + hits[0].y1) / 2)
    return x <= center.x <= x + width and y <= center.y <= y + height


def color_pixels(page: fitz.Page, region: tuple[float, float, float, float], channel: str) -> int:
    scale = 2
    pix = page.get_pixmap(matrix=fitz.Matrix(scale, scale), alpha=False)
    x, y, width, height = region
    x0 = max(0, round(mm(x) * scale))
    y0 = max(0, round(mm(y) * scale))
    x1 = min(pix.width, round(mm(x + width) * scale))
    y1 = min(pix.height, round(mm(y + height) * scale))
    count = 0
    for py in range(y0, y1):
        row = py * pix.stride
        for px in range(x0, x1):
            offset = row + px * pix.n
            red, green, blue = pix.samples[offset:offset + 3]
            if channel == "red" and red > 180 and green < 80 and blue < 80:
                count += 1
            if channel == "blue" and blue > 150 and red < 80 and green < 140:
                count += 1
    return count


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("pdf", type=Path)
    parser.add_argument("--mode", choices=("placeholders", "assets", "disabled"), required=True)
    args = parser.parse_args()

    document = fitz.open(args.pdf)
    if not document:
        print("封面验收失败：PDF 无页面")
        return 1
    page = document[0]
    text = page_text(page)
    failures: list[str] = []

    if args.mode == "placeholders":
        if not label_in_region(page, WORDMARK_LABEL, (77.7, 49.5, 64.5, 12.04)):
            failures.append("校名标准字占位文字缺失或不在预期区域")
        if not label_in_region(page, EMBLEM_LABEL, (89.0, 107.2, 42.1, 42.1)):
            failures.append("校徽占位文字缺失或不在预期区域")
        if not matching_rect(page, (77.7, 49.5, 64.5, 12.04)):
            failures.append("校名标准字占位框尺寸或位置错误")
        if not matching_rect(page, (89.0, 107.2, 42.1, 42.1)):
            failures.append("校徽占位框尺寸或位置错误")
    else:
        if WORDMARK_LABEL in text or EMBLEM_LABEL in text:
            failures.append("不应出现占位文字")

    if args.mode == "assets":
        red = color_pixels(page, (77.7, 49.5, 64.5, 12.04), "red")
        blue = color_pixels(page, (89.0, 107.2, 42.1, 42.1), "blue")
        if red < 500:
            failures.append(f"未在校名标准字区域检测到测试素材（红色像素 {red}）")
        if blue < 500:
            failures.append(f"未在校徽区域检测到测试素材（蓝色像素 {blue}）")

    if args.mode == "disabled":
        if len(document) != 1:
            failures.append(f"关闭封面后应只剩测试正文 1 页，实际 {len(document)} 页")
        if "封面已关闭测试" not in text:
            failures.append("关闭封面后第一页不是测试正文")

    if failures:
        print("封面素材验收失败：")
        for failure in failures:
            print(f"  - {failure}")
        return 1
    print(f"封面素材验收通过：{args.mode}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
