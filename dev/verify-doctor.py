#!/usr/bin/env python3
"""博士完整示例的 PDF 验收；独立期望值来自 docs/博士规格.md。

基线由原始 Word 锚点及已裁定的行盒规则重建，不能替代原生 Word 或学校验收。
"""
import argparse
import re
import sys
from pathlib import Path

import fitz

PT30MM = 30 * 72 / 25.4


def spans(page):
    return [s for b in page.get_text("dict")["blocks"]
            for line in b.get("lines", []) for s in line["spans"]]


def compact(text):
    return re.sub(r"\s+", "", text)


def verify(path, degree="academic", blind=False, enterprise=True):
    doc = fitz.open(path)
    errors = []
    pro = degree == "professional"
    enterprise = pro and enterprise

    def check(name, ok):
        if not ok:
            errors.append(name)

    check("完整示例页数31", len(doc) == 31)
    if len(doc) < 31:
        return errors
    check("全篇A4", all(abs(p.rect.width - 595.276) < .03
                         and abs(p.rect.height - 841.89) < .03 for p in doc))
    pages = [spans(p) for p in doc]
    texts = [compact(p.get_text()) for p in doc]

    def row(pn, key, y, size, x=None, bold=False):
        candidates = pages[pn - 1] + [
            dict(line["spans"][0], text="".join(s["text"] for s in line["spans"]))
            for b in doc[pn - 1].get_text("dict")["blocks"]
            for line in b.get("lines", []) if line["spans"]
        ]
        hits = [s for s in candidates if compact(key) in compact(s["text"])
                and abs(s["origin"][1] - y) < .15 and abs(s["size"] - size) < .05]
        check(f"p{pn} {key} 基线/字号", bool(hits))
        if x is not None:
            check(f"p{pn} {key} 横坐标", any(abs(s["origin"][0] - x) < .15 for s in hits))
        if bold:
            check(f"p{pn} {key} 加粗", any(s["flags"] & 16 for s in hits))

    # 直接列出由独立 Word 锚点推导的基线，不读取被测 Typst 常量。
    cover_y = PT30MM + (524.5 if pro else 567) + 20.32
    title_y = PT30MM + (411.1 if pro else 439.45) + 23.36
    row(1, "复杂系统的可靠建模", title_y, 22, bold=True)
    row(1, "与验证方法研究", title_y + 30, 22, bold=True)
    row(1, "作者姓名", cover_y, 14, PT30MM + 99.25, bold=True)
    row(1, "学校导师" if pro else "指导教师", cover_y + 30, 14)
    row(1, "申请学位类别", cover_y + 30 * (3 if enterprise else 2), 14)
    if enterprise:
        row(1, "企业导师", cover_y + 60, 14)

    row(3, "学校代码", PT30MM + (8.45 if pro else 8.5) + 12.165,
        10.5, PT30MM + (5.9 if pro else 5.65))
    row(3, "西安电子科技大学", PT30MM + (113.75 if pro else 113.4) + 24.88, 26, bold=True)
    row(3, "博士学位论文", PT30MM + (113.75 if pro else 113.4) + 90 + 24.12, 24, bold=True)
    row(3, "复杂系统的可靠建模", PT30MM + (311.5 if pro else 311.85) + 23.36, 22)
    cn_y = PT30MM + (453.35 if pro else 453.6) + 21.32
    row(3, "作者姓名", cn_y, 14, PT30MM + 127.6)
    row(3, "领域" if pro else "一级学科", cn_y + 32, 14)
    row(3, "提交日期", cn_y + 32 * (5 if pro and not enterprise else 6), 14)
    row(5, "Reliable Modeling and Verification", PT30MM + (-.15 if pro else 0) + 23.36, 22, bold=True)
    middle_y = PT30MM + (169.65 if pro else 170.1) + 21.08
    row(5, "A dissertation submitted to", middle_y, 16)
    row(5, "XIDIAN UNIVERSITY", middle_y + 30, 16)
    degree_name = "Doctor of Engineering" if pro else "Doctor of Philosophy"
    row(5, "for the degree of " + degree_name, middle_y + 90, 16)
    row(5, "in Electronic Information" if pro else "in Electronic Science and Technology",
        middle_y + 120, 16)
    by_y = PT30MM + (510.3 if pro else 530.25) + 21.08
    row(5, "By", by_y, 16)
    row(5, "October 2026", by_y + (120 if pro else 90), 16)
    if not blind:
        row(5, "Zhang San", by_y + 30, 16)
        if pro:
            row(5, "Supervisor: Li Si", PT30MM + 570.2 + 21.08, 16, PT30MM + 47.1)
            row(5, "Title: Professor", PT30MM + 571.15 + 21.08, 16, PT30MM + 230.85)
            if enterprise:
                row(5, "Supervisor: Wang Wu", PT30MM + 570.2 + 51.08, 16)
        else:
            row(5, "Supervisor: Li Si", by_y + 60, 16)
    for pn in (1, 3, 5, 7):
        check(f"p{pn}无页眉页码", not any(s["origin"][1] < 80 or s["origin"][1] > 785
                                         for s in pages[pn - 1]))
    check("前置未编号填充页全空", all(not texts[n - 1] for n in (2, 4, 6, 8)))
    # 不只扫首页；正文偶数页和后置部分间的填充页都必须切换。
    for pn in range(10, len(doc) + 1, 2):
        row(pn, "西安电子科技大学博士学位论文", 20 * 72 / 25.4 + 13.99, 10.5)
    check("没有硕士固定页眉", all("硕士学位论文" not in text for text in texts))
    check("博士成果栏", "攻读博士学位期间的研究成果" in texts[-1])
    for pn in range(9, len(doc) + 1):
        footers = [s for s in pages[pn - 1] if abs(s["origin"][1] - 279.5 * 72 / 25.4) < .1]
        expected = ("I", "II", "III", "IV", "V", "VI", "VII", "VIII", "IX", "X", "XI", "XII",
                    "XIII", "XIV")[pn - 9] if pn < 23 else str(pn - 22)
        check(f"p{pn}连续页码", len(footers) == 1 and footers[0]["text"] == expected)
    body_ys = sorted({round(s["origin"][1], 3) for s in pages[22]
                      if abs(s["size"] - 12) < .05})
    check("正文20pt基线距", len(body_ys) > 5 and all(abs(b - a - 20) < .03
                                                   for a, b in zip(body_ys, body_ys[1:])))
    for pn in range(9, len(doc) + 1):
        rules = [d for d in doc[pn - 1].get_drawings()
                 if 75 < d["rect"].y0 < 80 and d["rect"].width > 400]
        check(f"p{pn}双线页眉", len(rules) == 2
              and all(abs(d["rect"].width - 155 * 72 / 25.4) < .05 for d in rules))
    lines = [d for d in doc[0].get_drawings() if d["rect"].width > 20]
    check("封面实线数量", len(lines) == (4 if enterprise else 3)
          and all(d["dashes"] in (None, "", "[]", "[] 0") for d in lines))
    check("封面实线基线位置", all(any(abs(d["rect"].y0 - cover_y - i * 30 - 1.5) < .1
                                                   for d in lines) for i in range(len(lines))))
    for pn in (1, 3, 5):
        check(f"p{pn}文字位于页面内", all(0 <= s["bbox"][0] < s["bbox"][2] <= 595.3
                                          and 0 <= s["bbox"][1] < s["bbox"][3] <= 841.9
                                          for s in pages[pn - 1]))
    if not enterprise:
        check("无企业导师栏目", all("企业导师" not in t and "WangWu" not in t for t in texts[:5]))
    identities = ("张三", "ZhangSan", "李四", "LiSi", "王五", "WangWu", "20261029001")
    if blind:
        check("内置身份字段隐去", all(s not in "".join(texts) for s in identities))
        check("PDF作者元数据隐去", not doc.metadata["author"])
    else:
        check("作者与学号可见", "张三" in texts[0] and "20261029001" in texts[2])
        check("PDF作者元数据", doc.metadata["author"] == "张三")
    return errors


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("pdf", type=Path)
    parser.add_argument("--degree", choices=("academic", "professional"), default="academic")
    parser.add_argument("--blind", action="store_true")
    parser.add_argument("--no-enterprise", action="store_true")
    args = parser.parse_args()
    errors = verify(args.pdf, args.degree, args.blind, not args.no_enterprise)
    for error in errors:
        print("不合格：" + error)
    print(f"博士PDF验收：不合格 {len(errors)} 项（Word锚点重建口径）")
    sys.exit(bool(errors))
