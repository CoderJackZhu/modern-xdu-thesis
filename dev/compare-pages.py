#!/usr/bin/env python3
"""P5 逐页对照：把官方 templet.pdf 与本模板输出按「同一页面」配对，渲染成并排 PNG。

用法: python3 dev/compare-pages.py <官方pdf> <本模板pdf> <输出目录>

配对方式：不按页码（两者页数不同），按页面上的**标题文字**配对。
"""
import os
import sys
import fitz

# (显示名, 官方页号, 定位关键字)
PAIRS = [
    ("封面", 1, None),
    ("中文题名页", 3, None),
    ("英文题名页", 5, None),
    ("声明", 7, None),
    ("中文摘要", 9, None),
    ("英文摘要", 11, None),
    ("插图索引", 13, None),
    ("表格索引", 15, None),
    ("符号对照表", 17, None),
    ("缩略语对照表", 19, None),
    ("目录", 21, None),
    ("第一章正文", 23, "第一章"),
    ("参考文献", 37, "参考文献"),
    ("致谢", 41, "致谢"),
    ("作者简介", 43, "作者简介"),
]


def find_title(doc, kw, start=1):
    """找「文档大标题」所在页：关键字须以 16pt 居中标题出现且基线在页顶 50mm 内。

    只按文字搜索会被目录条目命中（目录里也有「第一章」「参考文献」），
    所以必须同时校验字号与位置。
    """
    mm = lambda v: v / 72 * 25.4
    for i in range(start - 1, doc.page_count):
        for blk in doc[i].get_text("dict")["blocks"]:
            if blk.get("type"):
                continue
            for ln in blk["lines"]:
                for sp in ln["spans"]:
                    if (round(sp["size"], 1) == 16.0
                            and mm(sp["origin"][1]) < 50
                            and kw in sp["text"]):
                        return i + 1
    return None


def main(official, ours, outdir):
    """逐页对照：每组输出一张并排图，最后再合成一张总览图。

    并排图是**可复现的派生产物**（已 gitignore），仓库里只留总览图，
    便于一眼看清全部页面。
    """
    os.makedirs(outdir, exist_ok=True)
    a, b = fitz.open(official), fitz.open(ours)
    print(f"官方 {a.page_count} 页 / 本模板 {b.page_count} 页\n")
    print(f"{'页面':<14}{'官方页':>7}{'本模板页':>9}   输出")
    print("-" * 60)
    made = 0
    缩略 = []
    for name, opage, kw in PAIRS:
        # 前置页面两者分页一致（封面 p1 / 中文题名页 p3 / … / 目录 p21），直接用官方页号；
        # 正文之后按 16pt 标题定位，因为页数不同。
        mpage = opage if kw is None else find_title(b, kw, start=23)
        if opage > a.page_count or mpage is None:
            print(f"{name:<14}{opage:>7}{'—':>9}   ⏭ 跳过（未找到对应页）")
            continue
        # 并排图用 1.6x（细节可读）；同时按小尺寸渲染一份，供末尾合成总览图
        pa = a[opage - 1].get_pixmap(matrix=fitz.Matrix(1.6, 1.6))
        pb = b[mpage - 1].get_pixmap(matrix=fitz.Matrix(1.6, 1.6))
        缩略.append((
            a[opage - 1].get_pixmap(matrix=fitz.Matrix(0.62, 0.62)),
            b[mpage - 1].get_pixmap(matrix=fitz.Matrix(0.62, 0.62)),
            name))
        h = max(pa.height, pb.height)
        canvas = fitz.Pixmap(fitz.csRGB, fitz.IRect(0, 0, pa.width + pb.width + 40, h), False)
        canvas.set_rect(canvas.irect, (255, 255, 255))
        canvas.copy(pa, fitz.IRect(0, 0, pa.width, pa.height))
        canvas.copy(pb, fitz.IRect(pa.width + 40, 0, pa.width + 40 + pb.width, pb.height))
        path = os.path.join(outdir, f"{made:02d}-{name}.png")
        canvas.save(path)
        made += 1
        print(f"{name:<14}{opage:>7}{mpage:>9}   {path}")
    print(f"\n共 {made} 组并排对照图（左=官方，右=本模板）")

    # ---- 总览图：6 列网格，每格「官方 | 本模板」 ----
    列 = 6
    行 = (len(缩略) + 列 - 1) // 列
    if 缩略:
        w = 缩略[0][0].width * 2 + 20
        h = 缩略[0][0].height
        总 = fitz.Pixmap(fitz.csRGB, fitz.IRect(0, 0, w * 列, h * 行), False)
        总.set_rect(总.irect, (255, 255, 255))
        for i, (pa, pb, name) in enumerate(缩略):
            x, y = (i % 列) * w, (i // 列) * h
            总.copy(pa, fitz.IRect(x, y, x + pa.width, y + pa.height))
            总.copy(pb, fitz.IRect(x + pa.width + 20, y,
                                  x + pa.width + 20 + pb.width, y + pb.height))
        路径 = os.path.join(outdir, "总览.png")
        总.save(路径)
        print(f"总览图：{路径}（{列} 列 × {行} 行，每格左=官方 右=本模板）")


if __name__ == "__main__":
    sys.exit(main(*sys.argv[1:4]))
