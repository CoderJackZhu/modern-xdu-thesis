#!/usr/bin/env python3
"""从官方 templet.pdf 抽出正文文本，生成「内容与官方一致」的示例论文 .typ。

用途：节 / 小节标题的 y 位置由前面的内容流决定，只能靠**内容完全一致**才能逐行对照。
本脚本把官方正文的文字按段落结构还原成 Typst 标记，配合 dev/compare-lines.py 即可
逐行比对基线 y。

用法: python3 dev/extract-official.py <官方pdf> <输出typ>

要点（踩过的坑）：
- 只抽正文（跳过前置与后置部分），并跳过第四章图表页（代码还原不了图）。
- 页眉（y < 30mm）与页码（y > 250mm）不抽。
- **跨页续段必须接上**：官方某页第一行若是「顶格正文行」，它是上一页某段落的续行；
  按页切断会凭空多出一个段间距（5.44pt），后续基线全部下移。
- **节/小节标题要剥掉编号**：官方正文里写着「2.1 封面」，而本模板的编号由 Typst 自动生成，
  照抄会变成「2.1 2.1 封面」。
- 标题层级按字号判定：16pt=章、15pt=节、14pt=小节。
"""
import re
import sys

import fitz

MM = lambda v: round(v / 72 * 25.4, 2)

# 正文页范围（官方 templet.pdf）：p23 第一章、p24 空白、p25-32 第二章
BODY_PAGES = [23, 25, 26, 27, 28, 29, 30, 31, 32]

# 官方标题里的编号前缀，如「2.1」「2.6」「3.1」
编号前缀 = re.compile(r"^(\d+(?:\.\d+)*)\s*")


def spans_of(page):
    out = []
    for blk in page.get_text("dict")["blocks"]:
        if blk.get("type"):
            continue
        for ln in blk["lines"]:
            for sp in ln["spans"]:
                if not sp["text"].strip():
                    continue
                y = MM(sp["origin"][1])
                if y < 30 or y > 250:      # 页眉 / 页码
                    continue
                out.append({
                    "y": y, "x": MM(sp["bbox"][0]),
                    "size": round(sp["size"], 2), "t": sp["text"],
                })
    out.sort(key=lambda s: (round(s["y"], 2), s["x"]))
    return out


def group_lines(spans):
    """把 span 按基线分组还原成「行」，再取整行的字号/左边界。"""
    lines, cur = [], []
    for s in spans:
        if cur and abs(s["y"] - cur[-1]["y"]) > 0.5:
            lines.append(cur)
            cur = []
        cur.append(s)
    if cur:
        lines.append(cur)
    return [{
        "y": ln[0]["y"],
        "x": min(s["x"] for s in ln),
        "size": max(s["size"] for s in ln),
        "t": "".join(s["t"] for s in ln).strip(),
    } for ln in lines]


def to_typst(items, pages):
    """还原成 Typst 标记。标题按字号映射层级；正文按缩进断段，跨页续段自动接上。"""
    out, buf = [], []
    段数 = 0

    def flush():
        nonlocal 段数
        if buf:
            段数 += 1
            out.append("".join(buf))
            out.append("")
            buf.clear()

    for it in items:
        if it["size"] >= 13.9:                      # 任意级别的标题
            flush()
            if it["size"] >= 15.9:
                lvl, text = 1, it["t"]
                # 章标题：「第一章」+ 题目，补一个空格便于阅读（不影响基线）
                text = re.sub(r"^(第[一二三四五六七八九十]+章)\s*", r"\1 ", text)
            elif it["size"] >= 14.9:
                lvl, text = 2, 编号前缀.sub("", it["t"])
            else:
                lvl, text = 3, 编号前缀.sub("", it["t"])
            out.append("=" * lvl + " " + text)
            out.append("")
        else:                                       # 正文
            if it["x"] > 32:                        # 首行缩进 → 新段落
                flush()
            buf.append(it["t"])
    flush()
    return "\n".join(out), 段数, pages


def main(pdf, outpath):
    doc = fitz.open(pdf)
    stream, pages = [], []
    页范围 = []
    for pno in BODY_PAGES:
        if pno > doc.page_count:
            continue
        items = group_lines(spans_of(doc[pno - 1]))
        if not items:
            continue
        if stream:
            页范围.append((pno, len(stream)))
        else:
            页范围.append((pno, 0))
        stream.extend(items)
    body, 段数, _ = to_typst(stream, pages)
    header = '''// 由 dev/extract-official.py 从官方 templet.pdf 抽取生成 —— 请勿手改
// 内容与官方正文（第一、二章）完全一致，用于逐行基线对照（dev/compare-lines.py）
//
// 抽取范围：''' + "、".join(f"p{p}" for p, _ in 页范围) + f'''（官方页号）
// 段落数：{段数}
#import "../lib.typ": documentclass

#let (doc, mainmatter) = documentclass(
  degree: "academic",
  info: (
    title: ("内容与官方一致的对照用示例",),
    author: "对照用",
    discipline: "电子科学与技术", supervisor: ("对照用", "教授"),
    department: "电子工程学院", submit-date: (year: 2025, month: 6),
    school-code: "10701", clc: "TN82", student-id: "00000000000", secret-level: "公开",
  ),
)
#show: doc

#show: mainmatter.with(header-title: "西安电子科技大学硕士学位论文")

'''
    open(outpath, "w", encoding="utf-8").write(header + body + "\n")
    print(f"写出 {outpath}")
    print(f"  官方页映射（官方页 → 抽取起点行号）：{页范围}")
    print(f"  段落数：{段数}")
    标题 = [l for l in body.split("\n") if l.startswith("=")]
    print(f"  标题数：{len(标题)}（章 {sum(1 for l in 标题 if l[0]=='=' and l[1]!='=')}、"
          f"节 {sum(1 for l in 标题 if l.startswith('== ') )}、"
          f"小节 {sum(1 for l in 标题 if l.startswith('=== '))}）")


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])
