#!/usr/bin/env python3
"""从原始 LaTeX 抽前置/后置数据，生成 dev/stress/front-data.typ。

为什么不让 pandoc 转这些：`notation` / `abbreviations` / `bio` 在本模板里是**元组数据**
（`(("符号", "说明"), …)`），而 pandoc 会把 LaTeX 表格转成 Typst 的 `#table(...)` 元素。
直接从 LaTeX 的 tabular 与 \\section* 抽结构更可靠。

用法: python3 dev/stress/front-data.py <源仓库 chapter 目录> <输出typ>
"""
import re
import subprocess
import sys


def 数学转typst(s):
    """单元格里的 $…$ 交给 pandoc 转成 Typst 数学；其余部分原样保留。"""
    if "$" not in s:
        return s
    r = subprocess.run(["pandoc", "-f", "latex", "-t", "typst"],
                       input=s, capture_output=True, text=True)
    # pandoc 把 \left( \right) 转成了转义括号，Typst 数学里要还原
    return (r.stdout.strip() if r.returncode == 0 else s).replace("\\(", "(").replace("\\)", ")")


def 抽表格(tex):
    """把 tabular 的行抽成 [[cell, cell], …]，跳过表头行。"""
    m = re.search(r"\\begin\{tabular\}.*?\n(.*?)\\end\{tabular\}", tex, re.S)
    if not m:
        return []
    行列表 = []
    for 行 in m.group(1).split("\\\\"):
        行 = re.sub(r"\\\\(toprule|midrule|bottomrule|hline)", "", 行).strip()
        行 = 行.replace("\\hline", "").strip()
        if not 行 or "&" not in 行:
            continue
        cells = [c.strip() for c in 行.split("&")]
        行列表.append([清理(数学转typst(c)) for c in cells])
    # 去掉表头行（首行往往是「符号 & 名称」这类）
    if 行列表 and all(len(c) < 8 for c in 行列表[0]):
        首 = "".join(行列表[0])
        if any(k in 首 for k in ("符号", "名称", "缩写", "英文", "中文")):
            行列表 = 行列表[1:]
    return 行列表


def 抽简介(tex):
    """\\section*{小标题} + 正文 → ((小标题, 内容), …)"""
    # bio.tex 用的是 \section{}（不是 \section*{}），两者都要认
    段 = re.split(r"\\section\*?\{([^}]*)\}", tex)
    条目 = []
    for i in range(1, len(段) - 1, 2):
        标题 = 段[i].strip()
        正文 = 段[i + 1].strip()
        if not 标题:
            continue
        # 正文里的列表环境转成 Typst 有序列表
        正文 = re.sub(r"\\begin\{enumerate\}(\[[^\]]*\])?", "", 正文)
        正文 = 正文.replace("\\end{enumerate}", "")
        正文 = re.sub(r"^\s*\\item\s*", "", 正文, flags=re.M)
        正文 = re.sub(r"\n{2,}", "\n", 正文).strip()
        正文 = 清理(正文)
        条目.append((标题, 正文))
    return 条目


def 清理(s):
    """清掉 LaTeX 残留：% 注释、\textasciitilde、\qquad 等。"""
    s = re.sub(r"(?<!\\)%.*$", "", s, flags=re.M)          # % 注释（不误伤 \%）
    s = s.replace("\\textasciitilde", "~")
    s = s.replace("\\textbackslash", "")
    s = re.sub(r"\\(qquad|quad|,|;|:|!)", " ", s)
    s = re.sub(r"[ \t]+$", "", s, flags=re.M)
    s = re.sub(r"\n{3,}", "\n\n", s)
    return s


def 转义(s):
    return s.replace('"', '\\"')


def main(章目录, 输出):
    读 = lambda n: open(f"{章目录}/{n}", encoding="utf-8").read()

    符号 = 抽表格(读("los.tex"))
    缩略 = 抽表格(读("loa.tex"))
    简介 = 抽简介(读("bio.tex"))

    行 = ["// 由 dev/stress/front-data.py 从原始 LaTeX 抽取生成 —— 请勿手改", ""]
    行.append("// 符号对照表")
    行.append("// 符号列写成 content（[…]，而非字符串）：字符串会被当纯文本，")
    行.append("// 真实论文的符号是数学（$x_0$），必须走 content 才能渲染成公式。")
    行.append("#let 符号表 = (")
    for c in 符号:
        if len(c) >= 2:
            行.append(f'  ([{c[0]}], [{c[1]}]),')
    行.append(")")
    行.append("")
    行.append("// 缩略语对照表")
    行.append("#let 缩略语表 = (")
    for c in 缩略:
        if len(c) >= 3:
            行.append(f'  ("{转义(c[0])}", "{转义(c[1])}", [{c[2]}]),')
        elif len(c) == 2:
            行.append(f'  ("{转义(c[0])}", "{转义(c[1])}", []),')
    行.append(")")
    行.append("")
    行.append("// 作者简介")
    行.append("#let 简介 = (")
    for 标题, 正文 in 简介:
        # 简介里的子标题（\subsection）降成加粗小标题，保持层级
        正文 = re.sub(r"\\subsection\{([^}]*)\}", r"\n#strong[\1]\n", 正文)
        行.append(f'  ("{转义(标题)}", [')
        for ln in 正文.splitlines():
            行.append("    " + ln)
        行.append("  ]),")
    行.append(")")

    open(输出, "w", encoding="utf-8").write("\n".join(行) + "\n")
    print(f"  符号表 {len(符号)} 条 / 缩略语表 {len(缩略)} 条 / 简介 {len(简介)} 段")
    print(f"  写出 {输出}")


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])
