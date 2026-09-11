#!/usr/bin/env python3
"""验收：正文与后置部分的版式对照官方数值。

用法: python3 dev/verify-body.py <pdf>

检查方式与 一致：按内容定位页面/元素后再比 y 与 x。
y 为 None 表示该项不校 y（流式排版位置随内容变化）。
"""
import re
import sys
import fitz

mm = lambda v: round(v / 72 * 25.4, 2)

# (标签, 关键字, 期望y, 期望字号, 期望x, 容差y, 容差x)
CHECKS = [
    # ---- 章首页（官方 p23）----
    ("章首页-页眉",    "第一章", 25.82, 10.5, None, 2.0, None),
    ("章首页-章标题",  "第一章", 44.25, 16.0, None, 2.0, None),
    ("章首页-正文首行", None,     57.61, 12.0, 30.00, 2.5, 2.0),
    # ---- 节 / 小节标题（官方 p27）----
    ("节标题",        None,     None, 15.0, 30.00, None, 2.0),
    ("小节标题",      None,     None, 14.0, None, None, None),
    # ---- 图表题注（官方 p35 / p36）----
    ("图题",          "图",      None, 10.5, None, None, None),
    ("表题",          "表",      None, 10.5, None, None, None),
    # ---- 参考文献（官方 p37）----
    ("参考文献-标题",  "参考文献", 44.25, 16.0, None, 2.5, None),
    ("参考文献-首条",  "[1]",     60.02, 10.5, None, 2.5, None),
    # ---- 致谢（官方 p41）----
    ("致谢-标题",     "致谢",    44.25, 16.0, None, 2.0, None),
    ("致谢-正文首行",  None,      57.61, 12.0, 30.00, 2.5, 2.0),
    # ---- 作者简介（官方 p43）----
    ("作者简介-标题",  "作者简介", 44.25, 16.0, None, 2.0, None),
    ("作者简介-小标题", None,     57.61, 15.0, 30.00, 2.5, 2.0),
]

# 每章从奇数页起：一级标题所在的页必须是奇数
def check_chapter_pages(spans, bad):
    """返回 (不合格数, 说明)。一级标题由 16pt 黑体居中判定（页眉是 10.5pt，不会误判）。"""
    章页 = sorted({s["p"] for s in spans if s["size"] == 16 and s["y"] < 50
                   and re.search(r"第[一二三四五六七八九十]+章", s["t"])})
    if not 章页:
        章页 = []
    奇 = [p for p in 章页 if not p % 2]
    print(f"章起始页 = {章页}  偶数页(应为空) = {奇}  {'✅' if not 奇 else '❌'}")
    return (0 if not 奇 else 1), len(章页)


def main(pdf):
    d = fitz.open(pdf)
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
    print(f"PDF: {pdf}  页数={len(d)}  总 span={len(spans)}\n")
    print(f"{'项目':<18}{'页':>4}{'期望y':>8}{'实测y':>8}{'Δy':>7}{'期望x':>8}{'实测x':>8}{'Δx':>7} 判定")
    print("-" * 86)
    bad = checked = 0
    for label, kw, ey, es, ex, ty, tx in CHECKS:
        def 命中(s):
            if abs(s["size"] - es) > 0.6:
                return False
            if kw is not None and s["t"] != kw:
                return False
            if ey is not None and abs(s["y"] - ey) > ty:
                return False
            return True
        候选 = [s for s in spans if 命中(s)]
        if not 候选 and kw is not None:
            候选 = [s for s in spans if kw in s["t"]
                    and (ey is None or abs(s["y"] - ey) <= ty)]
        if not 候选:
            print(f"{label:<18}{'--':>4}{(ey if ey is not None else float('nan')):>8.2f}"
                  f"{'未找到':>8}{'':>7}{'':>8}{'':>8}{'':>7} ⏭ 跳过")
            continue
        checked += 1
        s = min(候选, key=lambda z: abs(z["x"] - ex) if ex is not None else 0)
        dy = None if ey is None else s["y"] - ey
        dx = None if ex is None else s["x"] - ex
        ok = ((dy is None or abs(dy) <= ty) and (dx is None or abs(dx) <= tx))
        bad += 0 if ok else 1
        print(f"{label:<18}{s['p']:>4}"
              f"{(ey if ey is not None else s['y']):>8.2f}{s['y']:>8.2f}"
              f"{(dy if dy is not None else 0):>+7.2f}"
              f"{(ex if ex is not None else s['x']):>8.2f}{s['x']:>8.2f}"
              f"{(dx if dx is not None else 0):>+7.2f} {'✅' if ok else '❌'}")
    # ---- 正文首行缩进（回归项）----
    # 官方 p23 正文首行 x=38.47（缩进 2 字符 = 8.47mm）；
    # 根因见 dev/verify-front.py 同名检查的注释。
    正文行 = [s for s in spans if 55 < s["y"] < 62 and abs(s["size"] - 12) < 0.6
              and s["x"] > 32]
    checked += 1
    if not 正文行:
        print(f"{'正文首行缩进':<18}{'--':>4}{'':>8}{'未找到':>8}  ❌ 缺失")
        bad += 1
    else:
        hit = 正文行[0]
        dx = hit["x"] - 38.47
        ok = abs(dx) <= 2.0
        bad += 0 if ok else 1
        print(f"{'正文首行缩进':<18}{hit['p']:>4}{38.47:>8.2f}{hit['x']:>8.2f}{dx:>+7.2f}"
              f"{'':>17} {'✅' if ok else '❌'}")

    # ---- 索引编号/页码 与 公式号（回归项）----
    # 这三处都是**压力测试**（112 页真实论文）发现的静默错误，33 页占位样例里全都不明显：
    #   ① 索引里的图表编号丢了章前缀（「图 2.1」变成「图 1」）
    #     根因：figure 元素没设 numbering，索引退回 Typst 的全局默认序号
    #   ② 索引页码用了物理页号（应为 3，实际输出 25）
    #     根因：用了 location().page() 而不是页计数器在该位置的值
    #   ③ 公式编号是手写文本，公式本体没有 numbering → @eq: 引用直接报错
    def 首条索引(pno):
        """取该页第一个条目的 (编号, 页码)。"""
        行 = {}
        for s in spans:
            if s["p"] != pno:
                continue
            行.setdefault(round(s["y"], 1), []).append(s)
        for y in sorted(行):
            ss = sorted(行[y], key=lambda z: z["x"])
            t = [z["t"] for z in ss]
            if ss and ss[0]["t"] == "图" or (ss and ss[0]["t"] == "表"):
                编号 = "".join(t[1:2])
                页 = t[-1] if t else ""
                return 编号, 页, y
        return None, None, None

    for 标签, 页, 期望编号 in (("插图索引", 13, "2.1"), ("表格索引", 15, "2.1")):
        编号, 页号, _ = 首条索引(页)
        checked += 1
        if 编号 is None:
            print(f"{标签 + '首条':<18}{页:>4}{期望编号:>8}{'未找到':>8}{'':>7}{'':>7}{'':>8}  ❌ 缺失")
            bad += 1
            continue
        ok = (编号 == 期望编号) and (页号 == "3")
        bad += 0 if ok else 1
        print(f"{标签 + '首条':<18}{页:>4}{期望编号:>8}{编号:>8}{'':>7}{'':>7}{'':>8}"
              f"  {'✅' if ok else '❌'}  编号={编号} 页码={页号}（应为 {期望编号} / 3）")

    # 索引页不得出现引用上标（回归项）
    # 图注里的 #cite 若在索引页被渲染，会因 Typst「按引用首次出现位置编号」而
    # 把整份参考文献顺序打乱（上游 typst/typst#3994 → #1880）。
    # 修复方式是在索引页渲染条目前 `show cite: it => none`；这里守住它不被回退。
    上标 = [s for s in spans if s["p"] in (13, 15) and s["size"] < 8.5 and s["t"].startswith("[")]
    checked += 1
    if 上标:
        bad += 1
        print(f"{'索引页无引用上标':<18}{上标[0]['p']:>4}{'':>8}{'':>8}{'':>7}{'':>7}{'':>8}"
              f"  ❌ 索引页出现引用上标 {上标[0]['t']!r}（会打乱参考文献顺序）")
    else:
        print(f"{'索引页无引用上标':<18}{'13/15':>4}{'':>8}{'':>8}{'':>7}{'':>7}{'':>8}  ✅")

    # 公式号：右对齐到版心右界 185.00mm
    公式号 = [s for s in spans if s["t"].startswith("(") and s["t"].endswith(")")
             and len(s["t"]) < 8 and s["size"] > 10]
    checked += 1
    if not 公式号:
        print(f"{'公式号':<18}{'--':>4}{185.00:>8.2f}{'未找到':>8}  ❌ 缺失")
        bad += 1
    else:
        s = 公式号[0]
        dx = s["x1"] - 185.00
        ok = abs(dx) <= 1.0
        bad += 0 if ok else 1
        print(f"{'公式号右对齐':<18}{s['p']:>4}{185.00:>8.2f}{s['x1']:>8.2f}{dx:>+7.2f}"
              f"{'':>17} {'✅' if ok else '❌'}  {s['t']}")

    print("-" * 86)
    b2, n2 = check_chapter_pages(spans, bad)
    bad += b2
    checked += max(n2, 1)
    print(f"\n不合格：{bad} / {checked}")
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1]))
