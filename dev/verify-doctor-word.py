#!/usr/bin/env python3
"""用原始 Word XML 自检博士前置页锚点；不依赖 LibreOffice 的替换字体输出。"""
import argparse
from pathlib import Path
import re
import sys
import xml.etree.ElementTree as ET
from zipfile import ZipFile

ROOT = Path(__file__).resolve().parents[1]
NS = {"w": "http://schemas.openxmlformats.org/wordprocessingml/2006/main",
      "v": "urn:schemas-microsoft-com:vml"}


def verify(docx, degree, implementation):
    root = ET.fromstring(ZipFile(docx).read("word/document.xml"))
    shapes = [s for s in root.findall(".//v:shape", NS)
              if s.find(".//w:txbxContent", NS) is not None]
    # 这两个官方文件各自固定的文本框顺序；若学校换版，明确失败以便重新裁定。
    order = {
        "cover-title": 0, "cover-fields": 1, "cn-title": 2, "cn-fields": 3,
        "school": 4, "info-right": 5, "info-left": 6,
        "en-by": 7, "en-middle": 8, "en-title": 9,
    } if degree == "academic" else {
        "cover-title": 0, "cover-fields": 1, "cn-title": 2, "school": 3,
        "cn-fields": 4, "info-right": 5, "info-left": 6,
        "en-middle": 9, "en-title": 10, "en-by": 11,
    }
    expected_count = 10 if degree == "academic" else 12
    if len(shapes) != expected_count:
        return [f"Word文本框数变更：{len(shapes)}，预期{expected_count}"]
    source = implementation.read_text()
    pro, academic = source.split("} else {", 1)
    source = pro if degree == "professional" else academic.split("// 使用行框", 1)[0]
    errors = []
    for key, index in order.items():
        actual = re.search(rf"{key}: \(([-\d.]+)pt, ([-\d.]+)pt, ([-\d.]+)pt\)", source)
        style = shapes[index].get("style", "")
        values = [float(re.search(rf"(?:^|;){field}:([-\d.]+)pt", style)[1])
                  for field in ("margin-left", "margin-top", "width")]
        if not actual or any(abs(float(a) - b) > .001 for a, b in zip(actual.groups(), values)):
            errors.append(f"{key}与原始Word锚点不一致：Word={values}")
    for index, text in ((0, "西安电子科技大学"), (1, "作者姓名"), (2, "西安电子科技大学")):
        content = "".join(shapes[index].itertext())
        if text not in content:
            errors.append(f"Word文本框{index}语义变更")
    return errors


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("docx", type=Path)
    parser.add_argument("--degree", choices=("academic", "professional"), required=True)
    args = parser.parse_args()
    errors = verify(args.docx, args.degree, ROOT / "pages/doctor-front.typ")
    for error in errors:
        print("不合格：" + error)
    print(f"原始Word锚点自检：不合格 {len(errors)} 项")
    sys.exit(bool(errors))
