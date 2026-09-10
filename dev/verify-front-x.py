#!/usr/bin/env python3
"""前置部分横向（x）验收：与官方 templet.pdf 对照元素的左边界。

用法: OFFICIAL_PDF=<官方 templet.pdf> python3 dev/verify-front-x.py <pdf> [academic|professional]

按「页 + 基线 y」定位元素后再比 x，避免同一页同名元素（如页眉与标题都叫
ABSTRACT）互相干扰。
"""
import os
import sys
import fitz

mm = lambda v: round(v / 72 * 25.4, 2)

# 官方 templet.pdf 不在仓库内（学校分发材料），用环境变量指定。
# 本地路径写在 dev/local-paths.sh（已被 .gitignore 忽略），见 local-paths.example.sh。
OFF = os.environ.get("OFFICIAL_PDF")
if not OFF:
    sys.exit("请设置环境变量 OFFICIAL_PDF 指向官方 templet.pdf")

# (标签, 官方页, 期望基线 y, 关键字, 官方 x0, 适用学位)
CHECKS = [
    ("封面-作者姓名标签",    1, 239.34, "作者姓名", 60.00, "both"),
    ("封面-指导教师标签",    1, 249.88, "指导教师姓名", 60.00, "academic"),
    ("封面-申请学位类别标签", 1, 260.42, "申请学位类别", 60.00, "academic"),
    ("题名页-学校代码",      3, 38.36, "学校代码", 30.00, "both"),
    ("题名页-分类号",        3, 44.39, "分类号", 30.00, "both"),
    ("题名页-校名",          3, 80.02, "西安电子科技大学", 69.71, "both"),
    ("题名页-硕士学位论文",    3, 111.13, "硕士学位论文", 81.34, "both"),
    ("题名页-作者姓名：",     3, 200.69, "作者姓名：", 75.00, "both"),
    ("题名页-提交日期：",     3, 268.17, "提交日期：", 75.00, "both"),
    ("英文题名页-A Thesis",  5, 103.88, "A Thesis submitted", 82.65, "both"),
    ("英文题名页-By",        5, 232.54, "By", 104.21, "both"),
    ("声明-标题1",          7, 35.11, "西安电子科技大学", 87.15, "both"),
    ("摘要-标题",           9, 44.25, "摘要", 101.85, "both"),
    ("ABSTRACT-标题",      11, 44.25, "ABSTRACT", 92.87, "both"),
]


def collect(pdf, pages=None):
    d = fitz.open(pdf)
    out = {}
    for pno, page in enumerate(d, 1):
        if pages and pno not in pages:
            continue
        lst = []
        for blk in page.get_text("dict")["blocks"]:
            if blk.get("type"):
                continue
            for ln in blk["lines"]:
                for sp in ln["spans"]:
                    t = sp["text"].strip()
                    if t:
                        lst.append((t, mm(sp["bbox"][0]), mm(sp["origin"][1])))
        out[pno] = lst
    return out


target = sys.argv[1]
deg = sys.argv[2] if len(sys.argv) > 2 else "professional"
ours = collect(target)

print(f"横向对照：官方 templet.pdf  vs  {target}（{deg}）")
print(f"{'项目':<22}{'官方x':>8}{'实测x':>8}{'Δx':>7}  判定")
print("-" * 58)
bad = checked = 0
for label, pno, ey, kw, ex, dg in CHECKS:
    if dg != "both" and dg != deg:
        continue
    checked += 1
    hit = next(((t, x) for t, x, y in ours.get(pno, [])
                if kw in t and abs(y - ey) <= 2.0), None)
    if hit is None:
        print(f"{label:<22}{ex:>8.2f}{'未找到':>8}{'':>7}  ❌")
        bad += 1
        continue
    dx = hit[1] - ex
    ok = abs(dx) <= 2.0
    bad += 0 if ok else 1
    print(f"{label:<22}{ex:>8.2f}{hit[1]:>8.2f}{dx:>+7.2f}  {'✅' if ok else '❌'}")
print("-" * 58)
print(f"不合格：{bad} / {checked}（容差 2mm）")
