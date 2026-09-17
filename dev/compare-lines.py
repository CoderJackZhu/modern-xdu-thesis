#!/usr/bin/env python3
"""逐行对照：把「内容与官方一致」的示例论文输出与官方正文比版式。

为什么需要这个脚本
------------------
节/小节标题、图表题的 y 由前面的内容流决定，只有**内容完全一致**时 y 才有确定的期望值。
所以 dev/extract-official.py 会把官方正文抽成本模板能排的内容，再造一份出来对照。

比什么（以及为什么不比逐行 y）
------------------------------
字体度量不同（官方 SimSun / NimbusRomNo9L，本模板 Songti SC / Times New Roman），
**换行点会漂移**，所以同一页第 k 行的 y 天生对不上，逐行比 y 没有意义。
真正可比的是与换行无关的三项：

1. **行距**：同一段内相邻基线差。双方都应是「20 磅」，但两侧单位定义不同 ——
   Word/Typst 的 1 磅 = 1/72 in，LaTeX 的 1 pt = 1/72.27 in，
   所以官方应得 19.93bp、本模板应得 20.00bp，比值 1.00375。
2. **章标题基线**：与内容流无关（章首页页顶固定），应逐页对上。
3. **章标题 → 正文首行**：反映段后间距，已知双方引擎行盒模型不同（见 格式规格 §1 裁定），
   本模板按规范标称值实现，允许约 2mm 差异。

用法: python3 dev/compare-lines.py <官方pdf> <本模板pdf> <官方起始页> --map=23,24,25,...

判定：
- 行距比值落在 1.00375 ± 0.002（即双方都在各自单位下精确 20 磅）
- 章标题基线 Δ ≤ 0.5mm
- 章标题→正文首行 Δ ≤ 2.5mm（引擎差异，格式规格 §1 已裁定按标称值实现）
"""
import statistics
import sys
from collections import Counter

import fitz

MM = lambda v: round(v / 72 * 25.4, 2)
# 「20 磅」在两种单位下的理论比值：本模板 20bp / 官方 20 LaTeX-pt
# 1bp = 1/72 in、1 LaTeX pt = 1/72.27 in ⇒ 20bp / 20pt = 72.27/72 = 1.003750
预计比值 = (25.4 / 72) / (25.4 / 72.27)


def lines_of(pdf, pno):
    doc = fitz.open(pdf)
    if pno > doc.page_count:
        return None
    out = []
    for blk in doc[pno - 1].get_text("dict")["blocks"]:
        if blk.get("type"):
            continue
        for ln in blk["lines"]:
            spans = [s for s in ln["spans"] if s["text"].strip()]
            if not spans:
                continue
            y = MM(spans[0]["origin"][1])
            if y < 30 or y > 250:            # 页眉 / 页码
                continue
            out.append({
                "y": y,
                "size": round(max(s["size"] for s in spans), 2),
                "t": "".join(s["text"] for s in spans).strip(),
            })
    # 同一基线上的多个 span（标题被拆成两块）合并成一行
    out.sort(key=lambda s: s["y"])
    merged = []
    for s in out:
        if merged and abs(s["y"] - merged[-1]["y"]) < 0.5:
            merged[-1]["t"] += s["t"]
            merged[-1]["size"] = max(merged[-1]["size"], s["size"])
        else:
            merged.append(dict(s))
    return merged


def 行距行(lines):
    """取段内相邻基线差中**出现次数最多**的那档作为行距。

    ⚠️ 不能用中位数：节标题的段前/段后会产生 11pt 以上的大间隔，在未排满的页上
    样本少时会把中位数整个带偏（实测末页 11 行时中位数算成 6.9mm，误判为不合格）。
    行距是全文恒定的一档，用众数才对。
    """
    ds = [round(lines[i + 1]["y"] - lines[i]["y"], 3) for i in range(len(lines) - 1)]
    ds = [d for d in ds if d > 3.0]
    if not ds:
        return None, 0
    buckets = Counter(round(d * 20) / 20 for d in ds)      # 归到 0.05mm 一档
    top = max(buckets.values())
    众数档 = {k for k, v in buckets.items() if v == top}
    vals = [d for d in ds if round(d * 20) / 20 in 众数档]
    return round(sum(vals) / len(vals), 3), len(ds)


def main(official, ours, start, tol标题=0.5, tol首行=2.5, mapping=None):
    docs = fitz.open(ours)
    页表 = ([int(x) for x in mapping.split(",")] if mapping
            else [int(start) + k for k in range(docs.page_count)])
    print(f"官方 {fitz.open(official).page_count} 页 / 本模板 {docs.page_count} 页")
    print(f"配对（本模板页 → 官方页）：{dict(enumerate(页表, 1))}")
    print(f"行距理论比值（LaTeX pt / Word pt）= {预计比值:.5f}\n")
    print(f"{'本页':>4}{'官页':>5}{'官方行距':>10}{'本行距':>9}{'比值':>9}"
          f"{'章标题Δ':>10}{'首行Δ':>8}{'行数官/本':>11}  判定")
    print("-" * 92)
    bad = tot = 0
    池a, 池b = [], []          # 全文汇总的行，用于算行距（行距是全文恒定值，不该逐页判）
    for k in range(1, docs.page_count + 1):
        if k > len(页表):
            break
        opage = 页表[k - 1]
        a, b = lines_of(official, opage), lines_of(ours, k)
        if a is None:
            break
        tot += 1
        if not a and not b:
            print(f"{k:>4}{opage:>5}{'空页':>10}{'空页':>9}{'':>9}{'':>10}{'':>8}"
                  f"{'0/0':>11}  ✅")
            continue
        池a += a
        池b += b
        sa, _ = 行距行(a)
        sb, _ = 行距行(b)

        # 章标题与「章标题→正文首行」只在**章首页**上有确定期望值：
        # 判据是页面最上面一行本身就是 ≥15.5pt 的标题（其余页的首行位置由换行漂移决定，无意义）。
        章首页 = (a and b and a[0]["size"] >= 15.5 and b[0]["size"] >= 15.5)
        标Δ = 首Δ = None
        if 章首页:
            标a, 标b = a[0], b[0]
            标Δ = round(标b["y"] - 标a["y"], 2)
            首a = next((s for s in a[1:] if s["y"] > 标a["y"] + 1), None)
            首b = next((s for s in b[1:] if s["y"] > 标b["y"] + 1), None)
            首Δ = (round(首b["y"] - 首a["y"], 2) if (首a and 首b) else None)

        ok = ((标Δ is None or abs(标Δ) <= tol标题)
              and (首Δ is None or abs(首Δ) <= tol首行))
        bad += 0 if ok else 1
        print(f"{k:>4}{opage:>5}"
              f"{(f'{sa:.3f}' if sa else '—'):>10}{(f'{sb:.3f}' if sb else '—'):>9}"
              f"{'':>9}"
              f"{(f'{标Δ:+.2f}' if 标Δ is not None else '—'):>10}"
              f"{(f'{首Δ:+.2f}' if 首Δ is not None else '—'):>8}"
              f"{f'{len(a)}/{len(b)}':>11}  {'✅' if ok else '❌'}")
    print("-" * 92)

    # 行距：全文汇总后取众数。逐页判会被「未排满的页 + 节标题大间隔」带偏，
    # 而且官方某些页（如 p31 含列表/表格）自身众数就不是行距。
    全文a, _ = 行距行(池a)
    全文b, _ = 行距行(池b)
    比值 = round(全文b / 全文a, 5) if (全文a and 全文b) else None
    比值ok = (比值 is None) or abs(比值 - 预计比值) <= 0.002
    if not 比值ok:
        bad += 1
    print(f"行距（全文众数）：官方 {全文a} mm / 本模板 {全文b} mm → 比值 {比值}"
          f"（理论 {预计比值:.5f}） {'✅' if 比值ok else '❌'}")
    print(f"不合格页：{bad} / {tot + 1}"
          f"（章标题 Δ≤{tol标题}mm，章标题→正文首行 Δ≤{tol首行}mm，行距比值 ±0.002）")
    print("\n注 1：逐行 y 不逐行比对 —— 字体度量不同导致换行点漂移，"
          "同页第 k 行的 y 天生对不上。")
    print("注 2：行距是全文恒定值，只按全文众数判一次，不逐页判。")
    return 1 if bad else 0


if __name__ == "__main__":
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    mapping = None
    for a in sys.argv[1:]:
        if a.startswith("--map"):
            mapping = a.split("=", 1)[1]
    sys.exit(main(*args[:3], mapping=mapping))
