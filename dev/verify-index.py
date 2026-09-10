#!/usr/bin/env python3
"""P3 验收：把测得的 PDF 与 docs/索引部分规格.md 的官方数值逐项对照。

用法: python3 dev/verify-index.py <pdf>

设计：
  - 先按「16pt 标题」定位每个页面的页码，再在该页内检查元素，
    因此不依赖页面顺序（前置页面数量变化不会影响验收）。
  - 同时比 y（基线）与 x（左边界）；y 传 None 表示该项不校 y。
  - 条目类检查（插图/表格索引）在无图表时自动跳过。
"""
import re
import sys
import fitz

mm = lambda v: round(v / 72 * 25.4, 2)

# 目标页：标题文字 → 该页的检查项列表
# (标签, 关键字, 期望基线 y, 期望字号, 期望 x, 容差y, 容差x)
页定义 = {
    "插图索引": [
        ("页眉", "插图索引", 25.82, 10.5, 100.09, 1.0, 2.0),
        ("标题", "插图索引", 44.25, 16.0, 96.21, 1.0, 2.0),
        # 无插图时跳过条目检查
        ("条目前缀", "图", 61.12, 12.0, 30.00, 1.0, 2.0, True),
        ("条目页码", "1", 61.12, 12.0, 36.35, 1.0, 2.0, True),
    ],
    "表格索引": [
        ("页眉", "表格索引", 25.82, 10.5, 100.09, 1.0, 2.0),
        ("标题", "表格索引", 44.25, 16.0, 96.21, 1.0, 2.0),
        ("条目前缀", "表", 61.12, 12.0, 30.00, 1.0, 2.0, True),
    ],
    "符号对照表": [
        ("页眉", "符号对照表", 25.82, 10.5, 98.24, 1.0, 2.0),
        ("标题", "符号对照表", 44.25, 16.0, 93.39, 1.0, 2.0),
        ("表头1", "符号", 57.61, 12.0, 35.19, 1.0, 2.0),
        ("表头2", "符号名称", 57.61, 12.0, 95.54, 1.0, 2.0),
        # 数据首行第 2 列：官方 x = 98.36
        ("数据首行2列", None, 64.64, 12.0, 98.36, 1.0, 2.0),
    ],
    "缩略语对照表": [
        ("页眉", "缩略语对照表", 25.82, 10.5, 96.39, 1.0, 2.0),
        ("标题", "缩略语对照表", 44.25, 16.0, 90.57, 1.0, 2.0),
        ("表头1", "缩略语", 57.61, 12.0, 34.13, 1.0, 2.0),
        ("表头2", "英文全称", 57.61, 12.0, 72.25, 1.0, 2.0),
        ("表头3", "中文对照", 57.61, 12.0, 114.60, 1.0, 2.0),
        ("数据首行3列", None, 64.64, 12.0, 119.18, 1.0, 2.0),
    ],
    "目录": [
        ("页眉", "目录", 25.82, 10.5, 103.79, 1.0, 2.0),
        ("标题", "目录", 44.25, 16.0, 101.85, 1.0, 2.0),
        # 首条目 y 固定；后续条目数不定，二/三级只校 x
        ("一级条目", None, 57.76, 12.0, 30.00, 1.0, 2.0),
        # 二/三级条目仅当正文存在编号标题时才检查
        ("二级条目", "1.1", None, 12.0, 36.22, None, 2.0, True),
        ("三级条目", "1.1.1", None, 12.0, 45.76, None, 2.0, True),
    ],
}


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
    print(f"{'项目':<24}{'页':>4}{'期望y':>8}{'实测y':>8}{'Δy':>7}"
          f"{'期望x':>8}{'实测x':>8}{'Δx':>7} 判定")
    print("-" * 92)
    bad = checked = 0
    for 标题, 项列表 in 页定义.items():
        # 用 16pt 标题定位页面
        页 = next((s["p"] for s in spans if s["t"] == 标题 and abs(s["size"] - 16) < 0.6), None)
        if 页 is None:
            print(f"{标题:<24}{'--':>4}  ❌ 整页缺失（找不到 16pt 标题）")
            bad += len(项列表)
            checked += len(项列表)
            continue
        页内 = [s for s in spans if s["p"] == 页]
        for 项 in 项列表:
            if len(项) == 8:
                标签, kw, ey, es, ex, ty, tx, 可选 = 项
            else:
                标签, kw, ey, es, ex, ty, tx = 项
                可选 = False
            if 可选:
                # 无对应内容时跳过：目录的二/三级条目需要正文编号标题，
                # 索引条目需要正文里真的有图/表
                if 标题 == "目录":
                    有内容 = any(s["t"].startswith("1.") and s["size"] == 12 for s in 页内)
                    原因 = "该 PDF 无编号标题"
                else:
                    有内容 = any(abs(s["y"] - 61.12) <= 1.0 and s["size"] == 12 for s in 页内)
                    原因 = "该 PDF 无图/表条目"
                if not 有内容:
                    print(f"{标题}-{标签:<18}{页:>4}  ⏭ 跳过（{原因}）")
                    continue
            checked += 1
            def 命中(s):
                if abs(s["size"] - es) > 0.6:
                    return False
                if kw is not None and s["t"] != kw:
                    return False
                if ey is not None and abs(s["y"] - ey) > ty:
                    return False
                return True
            if kw is None:
                # 无关键字时取该行内 x 最接近期望值的 span
                候选 = [s for s in 页内 if 命中(s)]
                hit = min(候选, key=lambda s: abs(s["x"] - ex)) if 候选 else None
            else:
                hit = next((s for s in 页内 if 命中(s)), None)
                if hit is None:
                    hit = next((s for s in 页内 if kw in s["t"]
                                and (ey is None or abs(s["y"] - ey) <= ty)), None)
            if hit is None:
                print(f"{标题}-{标签:<18}{页:>4}"
                      f"{(ey if ey is not None else float('nan')):>8.2f}{'未找到':>8}{'':>7}"
                      f"{ex:>8.2f}{'':>8}{'':>7} ❌")
                bad += 1
                continue
            dy = None if ey is None else hit["y"] - ey
            dx = hit["x"] - ex
            ok = (dy is None or abs(dy) <= ty) and abs(dx) <= tx
            bad += 0 if ok else 1
            print(f"{标题}-{标签:<18}{页:>4}"
                  f"{(ey if ey is not None else hit['y']):>8.2f}{hit['y']:>8.2f}"
                  f"{(dy if dy is not None else 0):>+7.2f}"
                  f"{ex:>8.2f}{hit['x']:>8.2f}{dx:>+7.2f} {'✅' if ok else '❌'}")

    # 目录页码右边界（官方 185.00）
    print("-" * 92)
    目录页 = next((s["p"] for s in spans if s["t"] == "目录" and abs(s["size"] - 16) < 0.6), None)
    if 目录页:
        页码列 = [s for s in spans if s["p"] == 目录页 and s["size"] == 12
                  and re.fullmatch(r"[0-9IVXLC]+", s["t"])]
        右界 = [s["x1"] for s in 页码列]
        if 右界:
            print(f"目录页码右边界：官方 185.00，实测 max={max(右界):.2f} "
                  f"{'✅' if abs(max(右界) - 185.0) <= 2 else '❌'}")
            bad += 0 if abs(max(右界) - 185.0) <= 2 else 1
            checked += 1
    print(f"\n不合格：{bad} / {checked}")
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1]))
