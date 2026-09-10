#!/usr/bin/env python3
"""把真实论文（LaTeX）移植成 Typst，用本模板排版，作为全尺寸压力测试。

源：一份 112 页、已通过学校格式检查的硕士论文（专业学位）
    main.tex + chapter/*.tex + chapter/references.bib + Figure/

策略
----
正文用 pandoc 打底（pandoc 的 typst writer 会把章节、公式、图、交叉引用、引用
都转成 Typst 语法），再用本脚本做后处理：

  1. 章标题补编号 —— 本模板要求章号写在正文里（`= 第一章 绪论`），
     Typst 的 numbering 产不出「第一章」这种形式
  2. `\\(` / `\\)` → `(` / `)` —— pandoc 把 `\left(` `\right)` 转成了转义括号
  3. pandoc 在标题后插的 `<label>` 行保留（`@xxx` 交叉引用要靠它解析）
  4. 去掉 pandoc 留下的空 `<>` 与游离反斜杠

已知不保真的地方（压力测试的目的是暴露**模板**的问题，不追求像素级复刻）：
  - 表格：pandoc 丢了 `\caption`，所以表格没有表题与编号（表格正文与样式仍在）
  - 个别 LaTeX 表格宏（multirow / booktabs 的跨行跨列）会被展平成普通表格

用法: python3 dev/stress/port.py <源仓库目录> <输出目录>
"""
import os
import re
import shutil
import subprocess
import sys

中文数字 = "一二三四五六七八九十"


def 章号(n):
    if n <= 10:
        return 中文数字[n - 1]
    return "十" + 中文数字[n - 11] if n < 20 else str(n)


def 跑pandoc(tex路径):
    r = subprocess.run(["pandoc", "-f", "latex", "-t", "typst", tex路径],
                       capture_output=True, text=True)
    if r.returncode != 0:
        raise SystemExit(f"pandoc 失败：{r.stderr[:400]}")
    return r.stdout


def 引用改cite(s, bibkeys):
    """把 `@key` 改成 `#cite(<key>)`。

    不能留成 `@key`：Typst 的 label 允许中文字符，所以 `@krizhevsky2012imagenet和自编码器`
    会被当成一个 label（报 label does not exist）。`#cite(<key>)` 有明确边界，
    也是本模板推荐写法。只改真正存在于 .bib 的 key，避免误伤 `@fig:…` 这类交叉引用。
    """
    模式 = re.compile(r"@([A-Za-z0-9_.:+\-]+)")
    return 模式.sub(lambda m: f"#cite(<{m.group(1)}>)" if m.group(1) in bibkeys else m.group(0), s)


def 收集标签(s):
    """pandoc 把 LaTeX 的 label 输出成独占一行的 `<label>`。"""
    return set(re.findall(r"^<([^<>\n]+)>\s*$", s, flags=re.M))


def 去重标签(s):
    """pandoc 从标题文本自动生成的 label 可能重名（同名标题出现两次），
    Typst 直接报 `label occurs multiple times`。保留首个，后续加后缀。"""
    见过 = {}

    def 换(m):
        lab = m.group(1)
        if lab not in 见过:
            见过[lab] = 1
            return m.group(0)
        见过[lab] += 1
        return f"<{lab}-{见过[lab]}>"

    return re.sub(r"^<([^<>\n]+)>\s*$", 换, s, flags=re.M)


def 引用改ref(s, labels):
    """`@label` → `#ref(<label>, supplement: none)`。

    为什么不能用正则匹配 `@xxx`：Typst 的 label 允许中文，`@fig:clip所示` 会被整体
    当成一个 label；而 pandoc 从中文标题自动生成的 label（如 `@多模态智能装修设计生成框架所示`）
    根本没有前缀可依。所以改成**按文档里真实存在的 label 逐一替换，长的优先**
    （长的先替换可避免短 label 是长 label 前缀时误伤）。

    LaTeX 的 `\ref` 只给编号（正文里已写「如图…所示」），故 `supplement: none`
    去掉 Typst 默认加的「图 / 表 / 公式」前缀。
    """
    for lab in sorted(labels, key=len, reverse=True):
        s = s.replace(f"@{lab}", f"#ref(<{lab}>, supplement: none)")
    return s


def 后处理(s):
    # 1) 转义括号还原（来自 \left( \right)）
    s = s.replace("\\(", "(").replace("\\)", ")")

    # 2) 去掉 pandoc 留下的空标签行与游离反斜杠
    s = re.sub(r"^<>\s*$", "", s, flags=re.M)
    s = re.sub(r"^\\\s*$", "", s, flags=re.M)

    # 3) 章标题补编号：把第 k 个一级标题 `= X` 变成 `= 第k章 X`
    计数 = [0]

    def 换(m):
        计数[0] += 1
        return f"= 第{章号(计数[0])}章 {m.group(1).strip()}"

    s = re.sub(r"^= +(.+)$", 换, s, flags=re.M)
    return s, 计数[0]


def 去重bib(源文件, 目标):
    """按 @type{key, 去重，保留首次出现；返回 (总条数, 丢弃条数)。"""
    s = open(源文件, encoding="utf-8").read()
    条目 = re.split(r"(?=^@)", s, flags=re.M)
    见过, 保留 = set(), []
    for e in 条目:
        m = re.match(r"@\w+\{\s*([^,\s]+)\s*,", e)
        if not m:
            保留.append(e)
            continue
        k = m.group(1)
        if k in 见过:
            continue
        见过.add(k)
        保留.append(e)
    open(目标, "w", encoding="utf-8").write("".join(保留))
    print(f"  references.bib：{len(见过)} 条唯一 key，丢弃重复 {len(条目) - 1 - len(见过)} 条")


def 读bibkeys(路):
    s = open(路, encoding="utf-8").read()
    return set(re.findall(r"^@\w+\{\s*([^,\s]+)\s*,", s, flags=re.M))


def main(源, 输出):
    os.makedirs(输出, exist_ok=True)
    bibkeys = 读bibkeys(os.path.join(源, "chapter", "references.bib"))
    print(f"  .bib 唯一 key：{len(bibkeys)}")

    # ---- 正文 ----
    正文, 章数 = 后处理(跑pandoc(os.path.join(源, "chapter", "Chapters.tex")))
    正文 = 引用改ref(正文, 收集标签(正文))
    正文 = 去重标签(正文)
    正文 = 引用改cite(正文, bibkeys)
    print(f"  正文：{len(正文.splitlines())} 行，识别到 {章数} 个章标题")

    # ---- 前置 / 后置 ----
    各文件 = {}
    for 名 in ("abstract-zh", "abstract-en", "acknowledgements", "bio", "los", "loa"):
        路 = os.path.join(源, "chapter", 名 + ".tex")
        if os.path.exists(路):
            文 = 跑pandoc(路)
            各文件[名] = 文.strip()
            print(f"  {名}: {len(文.splitlines())} 行")

    # ---- 资源 ----
    图源 = os.path.join(源, "Figure")
    图目标 = os.path.join(输出, "Figure")
    if not os.path.exists(图目标):
        os.symlink(os.path.abspath(图源), 图目标)
        print(f"  Figure/ → 软链到 {图源}")
    # BibLaTeX 的 key 必须唯一：源里有重复 key（Typst 的解析器直接报错，biblatex 容忍）
    去重bib(os.path.join(源, "chapter", "references.bib"),
            os.path.join(输出, "references.bib"))

    # ---- 落盘（正文与前置后置分开，便于替换/调试）----
    open(os.path.join(输出, "body.typ"), "w", encoding="utf-8").write(正文 + "\n")
    for 名, 文 in 各文件.items():
        open(os.path.join(输出, f"{名}.typ"), "w", encoding="utf-8").write(文 + "\n")
    print(f"  已写出到 {输出}/")


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])
