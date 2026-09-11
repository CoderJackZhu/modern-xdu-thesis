#!/usr/bin/env python3
"""测量工具：编译 .typ 并用 PyMuPDF 读取文字基线与字号。

用法: python3 dev/measure.py <file.typ> [--pages N]
"""
import subprocess
import sys
import os

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def compile_typ(src: str, extra_args=None) -> str:
    """编译 typst 文件到 PDF，返回 PDF 路径。"""
    pdf = os.path.splitext(src)[0] + ".pdf"
    cmd = ["typst", "compile", "--root", REPO, src, pdf]
    if extra_args:
        cmd += extra_args
    r = subprocess.run(cmd, capture_output=True, text=True)
    if r.returncode != 0:
        print("编译失败:\n" + r.stderr[-4000:])
        sys.exit(1)
    if r.stderr.strip():
        print("[typst 警告] " + r.stderr.strip()[:2000])
    return pdf


def report_lines(pdf: str, pages=None):
    import fitz
    doc = fitz.open(pdf)
    print(f"PDF: {pdf}  页数={len(doc)}  尺寸={doc[0].rect.width:.2f}x{doc[0].rect.height:.2f}bp")
    rng = range(len(doc)) if pages is None else range(min(pages, len(doc)))
    for pno in rng:
        page = doc[pno]
        d = page.get_text("dict")
        rows = []
        for blk in d["blocks"]:
            if blk.get("type") != 0:
                continue
            for ln in blk["lines"]:
                for sp in ln["spans"]:
                    if not sp["text"].strip():
                        continue
                    x0, y0, x1, y1 = sp["bbox"]
                    rows.append({
                        "y_base": round(sp["origin"][1], 3),
                        "x0": round(x0, 3),
                        "x1": round(x1, 3),
                        "size": round(sp["size"], 3),
                        "font": sp["font"],
                        "text": sp["text"][:28],
                    })
        rows.sort(key=lambda r: (r["y_base"], r["x0"]))
        print(f"\n===== 第 {pno + 1} 页  共 {len(rows)} 个 span =====")
        prev = None
        for r in rows:
            dy = "" if prev is None else f"  Δ={r['y_base'] - prev:+.3f}"
            print(f"  y={r['y_base']:8.3f} x={r['x0']:7.2f}~{r['x1']:7.2f} "
                  f"{r['size']:5.2f}pt {r['font'][:22]:22s} | {r['text']}{dy}")
            prev = r["y_base"]
    doc.close()


if __name__ == "__main__":
    src = sys.argv[1]
    pages = None
    if "--pages" in sys.argv:
        pages = int(sys.argv[sys.argv.index("--pages") + 1])
    p = compile_typ(src)
    report_lines(p, pages)
