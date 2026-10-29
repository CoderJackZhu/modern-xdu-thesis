#!/usr/bin/env python3
"""核对手动引用和真实 cite 的8pt及基线上移，并对新增本科验收项注入错误。"""
from pathlib import Path
import shutil
import subprocess
import tempfile

import fitz

ROOT = Path(__file__).resolve().parents[1]


def main():
    with tempfile.TemporaryDirectory(prefix="xdu-bachelor-adjust-") as temp:
        tmp = Path(temp)
        for name in ("bachelor", "utils"):
            shutil.copytree(ROOT / name, tmp / name)
        shutil.copy2(ROOT / "bachelor.typ", tmp / "bachelor.typ")
        (tmp / "dev").mkdir()
        source = tmp / "dev/test-bachelor.typ"
        source.write_text((ROOT / "dev/test-bachelor.typ").read_text())
        pdf = tmp / "test.pdf"

        def compile_source():
            result = subprocess.run(["typst", "compile", "--root", str(tmp), str(source), str(pdf)],
                                    capture_output=True, text=True)
            assert result.returncode == 0, result.stderr

        for file, old, new, expected in (
            ("bachelor/pages.typ", '页面标题("ABSTRACT", english: true)',
             '页面标题("ABSTRACT")', "英文摘要标题16pt加粗TNR"),
            ("bachelor/mainmatter.typ", "size: 8pt", "size: 7pt", "正文手动引用8pt"),
            ("dev/test-bachelor.typ", "#acknowledgement()", "#references(entries: ())", "后置顺序致谢参考文献附录"),
        ):
            path = tmp / file
            original = path.read_text()
            assert old in original
            path.write_text(original.replace(old, new))
            try:
                compile_source()
                result = subprocess.run(["python3", str(ROOT / "dev/verify-undergrad.py"), str(pdf)],
                                        capture_output=True, text=True)
                assert result.returncode != 0 and f"- {expected}:" in result.stderr, result.stdout
            finally:
                path.write_text(original)
            print("检出：" + expected)

        # 两种引用均须实测，不用实现中的字号常量代替 PDF 结果。
        source.write_text(
            '#import "../bachelor.typ": documentclass\n#let t = documentclass()\n#show: t.doc\n'
            '#show: t.mainmatter\n= 引用测量\n'
            'Manual#(t.引用)(1) Mark\n\nAuto#cite(<example>) Mark\n'
            '#(t.references)(body: bibliography("ref.bib", style: "gb-7714-2015-numeric", title: none))')
        shutil.copy2(ROOT / "examples/doctor-ref.bib", tmp / "dev/ref.bib")

        def assert_citations():
            compile_source()
            spans = [s for p in fitz.open(pdf) for b in p.get_text("dict")["blocks"]
                     for line in b.get("lines", []) for s in line["spans"]]
            body = [s for s in spans if s["text"] in ("Manual", "Auto")]
            assert len(body) == 2
            for marker in body:
                citations = [s for s in spans if s["text"].strip() in ("[1]", "[", "1", "]")
                             and abs(s["size"] - 8) < .05
                             and 0 < marker["origin"][1] - s["origin"][1] < 12
                             and -.05 <= s["origin"][0] - marker["bbox"][2] < 18]
                assert citations, (marker, spans)

        assert_citations()
        path = tmp / "bachelor/mainmatter.typ"
        saved = path.read_text()
        old = "set super(typographic: false, size: 8pt)"
        assert old in saved
        path.write_text(saved.replace(old, "set super(typographic: false, size: 7pt)"))
        try:
            try:
                assert_citations()
            except AssertionError:
                pass
            else:
                raise AssertionError("真实 cite 错误字号未被检出")
        finally:
            path.write_text(saved)
        print("通过：手动/真实cite均为8pt、基线上移，真实cite错误字号被检出")


if __name__ == "__main__":
    main()
