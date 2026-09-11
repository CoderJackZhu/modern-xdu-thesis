#!/usr/bin/env python3
"""验收：把测得的 PDF 与 docs/前置部分规格.md 的官方数值逐项对照。

用法:
    python3 dev/verify-front.py <pdf> --degree professional
    python3 dev/verify-front.py <pdf> --degree academic --pages 1,3,5,7,9,11

两类检查：
  KEY_EXPECT —— 按**唯一关键字**找 span（文字内容可预知的元素）
  POS_EXPECT —— 按**页码 + 基线 y + 字号**找 span（内容随用户填写而变的元素，
                如论文题目、Supervisor 行）

--pages 给定时只在指定页里找（用于直接校验官方 templet.pdf 自身）。
"""
import sys
import fitz

# (标签, 唯一关键字, 期望基线 y(mm), 期望字号 pt, 容差 mm, 适用学位, 官方页码)
KEY_EXPECT = [
    # ---- 封面 ----
    ("封面-作者姓名",    "作者姓名",                      239.34, 14.0, 1.0, "both", 1),
    ("封面-指导教师",    "指导教师姓名、职称",             249.88, 14.0, 1.0, "academic", 1),
    ("封面-申请学位类别", "申请学位类别",                  260.42, 14.0, 1.0, "academic", 1),
    ("封面-学校导师",    "学校导师姓名、职称",             249.88, 14.0, 1.0, "professional", 1),
    ("封面-企业导师",    "企业导师姓名、职称",             260.42, 14.0, 1.0, "professional", 1),
    ("封面-申请学位类别", "申请学位类别",                  270.96, 14.0, 1.5, "professional", 1),
    # ---- 中文题名页 ----
    ("题名页-学校代码",  "学校代码",                       38.36, 10.5, 1.0, "both", 3),
    ("题名页-分类号",    "分类号",                         44.39, 10.5, 1.0, "both", 3),
    ("题名页-校名",      "西安电子科技大学",                80.02, 26.0, 1.0, "both", 3),
    ("题名页-硕士学位论文", "硕士学位论文",                  111.13, 24.0, 1.0, "both", 3),
    ("题名页-作者姓名：", "作者姓名：",                     200.69, 14.0, 1.0, "both", 3),
    ("题名页-一级学科",  "一级学科：",                     211.93, 14.0, 1.0, "academic", 3),
    ("题名页-二级学科",  "二级学科（研究方向）：",           223.18, 14.0, 1.0, "academic", 3),
    ("题名页-学院",      "学院",                          256.92, 14.0, 1.0, "both", 3),
    ("题名页-提交日期",  "提交日期：",                     268.17, 14.0, 1.0, "both", 3),
    ("题名页-领域",      "域：",                          211.93, 14.0, 1.0, "professional", 3),
    ("题名页-学校导师：", "学校导师姓名、职称：",            234.43, 14.0, 1.0, "professional", 3),
    ("题名页-企业导师：", "企业导师姓名、职称：",            245.67, 14.0, 1.0, "professional", 3),
    # ---- 英文题名页 ----
    ("英文题名页-A Thesis", "A Thesis submitted",           103.88, 16.0, 1.0, "both", 5),
    ("英文题名页-By",    "By",                             232.54, 16.0, 1.0, "both", 5),
    ("英文题名页-Sup1",  "Supervisor",                     253.63, 16.0, 1.0, "both", 5),
    # ---- 声明 ----
    ("声明-标题",        "学位论文独创性",                  42.14, 14.0, 1.0, "both", 7),
    ("声明-正文首行",    "秉承学校严谨的学风",               53.74, 12.0, 1.0, "both", 7),
    ("声明-授权标题",    "关于论文使用授权的说明",           185.55, 14.0, 1.0, "both", 7),
    ("声明-授权正文",    "本人完全了解",                    197.15, 12.0, 1.0, "both", 7),
    # ---- 中文摘要 ----
    ("摘要-页眉",       "摘要",                            25.82, 10.5, 1.0, "both", 9),
    ("摘要-标题",       "摘要",                            44.25, 16.0, 1.0, "both", 9),
    ("摘要-正文首行",    "摘要是学位论文",                  57.61, 12.0, 1.5, "both", 9),
    # ---- ABSTRACT ----
    ("ABSTRACT-页眉",   "ABSTRACT",                        25.82, 10.5, 1.0, "both", 11),
    ("ABSTRACT-标题",   "ABSTRACT",                        44.25, 16.0, 1.0, "both", 11),
    ("ABSTRACT-正文",   "The Abstract",                    53.80, 12.0, 1.5, "both", 11),
]

# (标签, 页码, 期望基线 y(mm), 期望字号 pt, 容差 mm)
# 内容随用户填写而变，只能按位置判定
POS_EXPECT = [
    ("封面-题目行1",       1, 172.37, 22.0, 1.0),
    ("封面-题目行2",       1, 181.68, 22.0, 1.5),   # 官方 LaTeX 用单倍行距 26.4pt；本模板按 Word 的 30pt
    ("题名页-题目行1",      3, 150.20, 22.0, 1.0),
    ("题名页-题目行2",      3, 160.74, 22.0, 1.5),
    ("英文题名页-大标题行1",  5,  45.03, 22.0, 1.0),
    ("英文题名页-大标题行2",  5,  55.57, 22.0, 1.5),
    ("英文题名页-Sup2行",   5, 264.17, 16.0, 1.0),  # 专硕才有；学硕模式自动跳过
]


def main():
    if len(sys.argv) < 2:
        print(__doc__)
        return 2
    pdf = sys.argv[1]
    degree = "professional"
    pages = None
    if "--degree" in sys.argv:
        degree = sys.argv[sys.argv.index("--degree") + 1]
    if "--pages" in sys.argv:
        pages = {int(v) for v in sys.argv[sys.argv.index("--pages") + 1].split(",")}

    d = fitz.open(pdf)
    mm = lambda v: round(v / 72 * 25.4, 2)
    spans = []
    for pno, page in enumerate(d, 1):
        for blk in page.get_text("dict")["blocks"]:
            if blk.get("type"):
                continue
            for ln in blk["lines"]:
                for sp in ln["spans"]:
                    if sp["text"].strip():
                        spans.append({"p": pno, "y": mm(sp["origin"][1]),
                                      "x": mm(sp["bbox"][0]), "x1": mm(sp["bbox"][2]),
                                      "size": round(sp["size"], 2), "t": sp["text"].strip()})

    print(f"PDF: {pdf}\n页数={len(d)}  总 span={len(spans)}  学位模式={degree}"
          f"  页限制={sorted(pages) if pages else '无'}\n")
    print(f"{'项目':<20}{'页':>4}{'期望y':>8}{'实测y':>8}{'Δy':>7}{'期望pt':>7}{'实测pt':>8}  判定")
    print("-" * 80)
    used, bad, checked = {}, 0, 0

    def 判定(label, hit, ey, es, tol, hint=None):
        nonlocal bad
        if hit is None:
            print(f"{label:<20}{'--':>4}{ey:>8.2f}{'未找到':>8}{'':>7}{es:>7.1f}{'':>8}  ❌ 缺失")
            bad += 1
            return
        dy = hit["y"] - ey
        ok = abs(dy) <= tol and abs(hit["size"] - es) <= 0.6
        bad += 0 if ok else 1
        print(f"{label:<20}{hit['p']:>4}{ey:>8.2f}{hit['y']:>8.2f}{dy:>+7.2f}"
              f"{es:>7.1f}{hit['size']:>8.2f}  {'✅' if ok else '❌'}")

    # ---- 关键字匹配 ----
    for label, kw, ey, es, tol, deg, hint in KEY_EXPECT:
        if deg != "both" and deg != degree:
            continue
        checked += 1
        pool = [s for s in spans if kw in s["t"] and (pages is None or s["p"] in pages)]
        if hint and pages:
            pool = [s for s in pool if s["p"] == hint]
        key = (kw, hint)
        idx = used.get(key, 0)
        判定(label, pool[idx] if len(pool) > idx else None, ey, es, tol)
        used[key] = idx + 1

    # ---- 位置匹配 ----
    for label, pno, ey, es, tol in POS_EXPECT:
        if degree != "professional" and label == "英文题名页-Sup2行":
            continue
        checked += 1
        if pages is not None and pno not in pages:
            continue
        pool = [s for s in spans if s["p"] == pno
                and abs(s["y"] - ey) <= tol and abs(s["size"] - es) <= 0.6]
        判定(label, pool[0] if pool else None, ey, es, tol)

    # ---- 首行缩进（回归项）----
    # Typst 的 `first-line-indent` 默认 `all: false`：**标题/块级元素后的第一段不缩进**。
    # 必须写 `(amount: 2em, all: true)`，否则正文第一段顶格——官方实测首行 x=38.47。
    摘要行 = [s for s in spans if s["p"] == 9 and 55 < s["y"] < 62
              and abs(s["size"] - 12) < 0.6]
    checked += 1
    if not 摘要行:
        print(f"{'摘要首行缩进':<20}{'--':>4}{38.47:>8.2f}{'未找到':>8}{'':>7}{'':>7}{'':>8}  ❌ 缺失")
        bad += 1
    else:
        hit = 摘要行[0]
        dx = hit["x"] - 38.47
        ok = abs(dx) <= 2.0
        bad += 0 if ok else 1
        print(f"{'摘要首行缩进':<20}{hit['p']:>4}{38.47:>8.2f}{hit['x']:>8.2f}"
              f"{'':>7}{'':>7}{'':>8}  {'✅' if ok else '❌'}  (期望 x=38.47)")

    # ---- 页码基线（回归项）----
    # 格式规格 §2.1「页脚距页底 1.75cm」→ 页码基线 = 297 − 17.5 = 279.50mm。
    # 与已过检的真实论文实测 279.50mm 完全一致（官方 2024.04 为 278.29mm）。
    # 这条以前没进验收表，结果 281.73mm 的错误位置长期没人发现。
    页脚行 = [s for s in spans if s["y"] > 272 and s["size"] < 11.5]
    checked += 1
    if not 页脚行:
        print(f"{'页码基线':<20}{'--':>4}{279.50:>8.2f}{'未找到':>8}{'':>7}{'':>7}{'':>8}  ❌ 缺失")
        bad += 1
    else:
        hit = min(页脚行, key=lambda s: abs(s["y"] - 279.50))
        dy = hit["y"] - 279.50
        ok = abs(dy) <= 1.0 and abs(hit["size"] - 9.0) <= 0.6
        bad += 0 if ok else 1
        print(f"{'页码基线':<20}{hit['p']:>4}{279.50:>8.2f}{hit['y']:>8.2f}{dy:>+7.2f}"
              f"{9.0:>7.1f}{hit['size']:>8.2f}  {'✅' if ok else '❌'}")

    # ---- 封面填空横线的线型（回归项）----
    # 官方 templet.pdf 与已过检的参考论文实测**都是实线**（PDF 的 dashes 为空）。
    # 本模板曾用 `dash: ("dot", 1pt, 1.5pt)` 画成点线，肉眼可见一排小点，
    # 而当时的验收只比坐标、不比线型，所以长期没被发现。坐标对不上不算完，
    # 线型也要对：这里直接读 PDF 的 dash 模式。
    # 覆盖面：**全文所有页**，不是只看封面。第一版只扫了第 1 页，结果把声明页
    # 改回点线它照样报 ✅ —— 假绿。当前正确版本全文零条虚线（目录的点引线不是用
    # dash 画的），所以判据可以做到最强：出现任何虚线即失败。
    doc0 = fitz.open(pdf)
    有虚线, 线条数 = [], 0
    for pno in range(1, len(doc0) + 1):
        for g in doc0[pno - 1].get_drawings():
            ds = g.get("dashes")
            横线段 = [it for it in g["items"]
                      if it[0] == "l" and abs(it[1].y - it[2].y) < 0.6]
            线条数 += len(横线段)
            if 横线段 and ds and str(ds).strip() not in ("[] 0", ""):
                有虚线.append((pno, round(横线段[0][1].y / 72 * 25.4, 1), ds))
    checked += 1
    if 线条数 == 0:
        print(f"{'横线线型':<20}{'--':>4}{'--':>8}{'未找到':>8}{'':>7}{'':>7}{'':>8}  ❌ 缺失")
        bad += 1
    else:
        ok = not 有虚线
        bad += 0 if ok else 1
        说明 = f"全文 {线条数} 条横线全为实线" if ok else \
               f"p{有虚线[0][0]} y={有虚线[0][1]}mm 出现虚线 {有虚线[0][2]}"
        print(f"{'横线线型':<20}{('--' if ok else 有虚线[0][0]):>4}{'--':>8}{'--':>8}{'':>7}"
              f"{'':>7}{'':>8}  {'✅' if ok else '❌'} {说明}")

    # ---- 前置空白填充页必须有页眉 + 页码（回归项）----
    # 前置每个小节都从奇数页起，中间空出的偶数页官方是这么处理的：
    #   封面↔声明 之间（p2~p8）：无页眉无页码
    #   「摘要」之后（p10=II、p12=IV…）：**固定页眉 + 罗马页码**
    # 本模板原先这些填充页全空，而当时的验收只看内容页的页码基线，永远发现不了。
    doc1 = fitz.open(pdf)
    n = len(doc1)
    正文标题 = [""] * (n + 1)

    def 页内容(pno):
        return doc1[pno - 1].get_text().strip()

    # 定位「摘要」页：含 16pt 的「摘要」标题（页面大标题），且是最早出现的
    摘要页 = None
    for pno in range(1, n + 1):
        for blk in doc1[pno - 1].get_text("dict")["blocks"]:
            if blk.get("type"):
                continue
            for ln in blk["lines"]:
                for sp in ln["spans"]:
                    if sp["text"].strip() == "摘要" and sp["size"] > 15:
                        摘要页 = 摘要页 or pno
    # 空页判定：去掉页眉（校名）与纯页码行后没有内容
    import re as _re
    空页 = []
    for pno in range(1, n + 1):
        t = _re.sub("西安电子科技大学硕士学位论文", "", 页内容(pno))
        t = _re.sub(r"^[IVX]+$|^\d+$", "", t, flags=_re.M).strip()
        if not t:
            空页.append(pno)
    错 = []
    for pno in 空页:
        t = 页内容(pno)
        有眉 = "西安电子科技大学硕士学位论文" in t
        有码 = bool(_re.search(r"^[IVX]+$|^\d+$", t, flags=_re.M))
        if 摘要页 and pno > 摘要页 and not (有眉 and 有码):
            错.append(f"p{pno} 缺{'页眉' if not 有眉 else ''}{'页码' if not 有码 else ''}")
        if 摘要页 and pno < 摘要页 and 有码:
            错.append(f"p{pno} 不该有页码")
    checked += 1
    ok = (not 错) and len(空页) > 0
    bad += 0 if ok else 1
    说明 = (f"{len(空页)} 张填充页表现正确（摘要后 {len([p for p in 空页 if 摘要页 and p > 摘要页])} 张带页眉页码）"
            if ok else ("；（无填充页，检查无效）" if not 空页 else "；".join(错[:3])))
    print(f"{'前置填充页':<20}{'--':>4}{'--':>8}{'--':>8}{'':>7}{'':>7}{'':>8}  "
          f"{'✅' if ok else '❌'} {说明}")

    print("-" * 80)
    print(f"不合格：{bad} / {checked}")
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
