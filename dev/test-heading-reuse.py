#!/usr/bin/env python3
"""标题复用、作者数组与本科页眉碰撞的 PDF 回归；产物仅写临时目录。"""

import os
from pathlib import Path
import subprocess
import tempfile

import fitz


ROOT = Path(__file__).resolve().parents[1]


def main():
    failures = []
    with tempfile.TemporaryDirectory(prefix="xdu-heading-reuse-") as directory:
        work = Path(directory)
        package = work / "packages/preview/modern-xdu-thesis"
        package.mkdir(parents=True)
        (package / "0.3.2").symlink_to(ROOT, target_is_directory=True)
        env = dict(os.environ, TYPST_PACKAGE_PATH=str(work / "packages"))

        def compile_pdf(name, source, error=None):
            path = work / (name + ".typ")
            path.write_text(source)
            result = subprocess.run(
                ["typst", "compile", "--root", str(work), str(path), str(path.with_suffix(".pdf"))],
                capture_output=True, text=True, env=env,
            )
            if error is not None:
                assert result.returncode != 0, "预期拒绝页眉碰撞，实际编译成功"
                assert error in result.stderr, result.stderr
                return None
            assert result.returncode == 0, result.stderr
            return fitz.open(path.with_suffix(".pdf"))

        def entrance(kind, info="(:)", blind=False, degree="academic"):
            if kind == "bachelor":
                setup = '#import "@preview/modern-xdu-thesis:0.3.2": bachelor\n#let documentclass = bachelor.documentclass\n'
                options = ""
            else:
                name = "doctor-documentclass" if kind == "doctor" else "documentclass"
                setup = f'#import "@preview/modern-xdu-thesis:0.3.2": {name} as documentclass\n'
                options = f', blind: {str(blind).lower()}, degree: "{degree}"'
            return setup + f"#let t = documentclass(info: {info}{options})\n#show: t.doc\n"

        def check(name, fn):
            try:
                fn()
                print("通过：" + name, flush=True)
            except AssertionError as error:
                failures.append(name)
                print("失败：" + name + "：" + str(error), flush=True)

        # 没有脚注时，复用过程不应改造元素构造参数或丢掉其样式。
        def constructors():
            headings = (
                "$vec(delim: \"[\", a,b)$",
                "$cases(a,b)$",
                "#align(center)[对齐标题]",
                "#rotate(2deg)[旋转标题]",
                "#stack(dir: ltr, spacing: 2pt, [甲], [乙])",
                "#grid(columns: (auto, auto), [丙], [丁])",
            )
            for kind in ("master", "bachelor"):
                for index, heading in enumerate(headings):
                    with compile_pdf(
                        f"constructors-{kind}-{index}",
                        entrance(kind) + "#(t.outline-page)()\n#show: t.mainmatter\n"
                        + "= " + heading + "\n正文\n",
                    ) as doc:
                        text = "".join(page.get_text() for page in doc)
                        assert "正文" in text
                        if "vec" in heading:
                            assert "[" in text and "]" in text, text

        check("本科与研究生的向量、分段公式及排版元素标题可复用", constructors)

        def authors():
            for kind in ("master", "bachelor", "doctor"):
                for degree in (("academic",) if kind == "bachelor" else ("academic", "professional")):
                    for rich in (False, True):
                        value = '("张三", [#text(fill: rgb("#ff0000"))[李四]])' if rich else '("张三", "李四")'
                        source = entrance(kind, f"(author: {value},)", degree=degree)
                        source += "#(t.cover)()\n"
                        if kind != "bachelor":
                            source += '#pagebreak(to: "odd")\n#(t.title-cn)()\n'
                        with compile_pdf(f"authors-{kind}-{degree}-{rich}", source) as doc:
                            text = "".join(page.get_text() for page in doc)
                            assert "张三" in text and "李四" in text, text
                            assert '("张三"' not in text, text
                            assert (doc.metadata.get("author") or "") == ("" if rich else "张三, 李四"), doc.metadata
                            if rich:
                                colored = [
                                    span for page in doc for block in page.get_text("dict")["blocks"]
                                    for line in block.get("lines", []) for span in line["spans"]
                                    if "李四" in span["text"] and span["color"] == 0xFF0000
                                ]
                                assert colored, "作者数组中的富文本颜色丢失"
            with compile_pdf(
                "authors-blind", entrance("master", '(author: ("甲甲", "乙乙"),)', blind=True)
                + "#(t.cover)()\n#pagebreak(to: \"odd\")\n#(t.title-cn)()\n",
            ) as doc:
                text = "".join(page.get_text() for page in doc)
                assert "甲甲" not in text and "乙乙" not in text
                assert not doc.metadata.get("author")

        check("作者数组在页面、元数据、富文本及盲审中保持一致", authors)

        def footnotes():
            headings = (
                "绪论#footnote[唯一说明]",
                "#context [绪论#footnote[唯一说明]]",
                '#context [#text(fill: rgb("#ff0000"))[绪论#footnote[唯一说明]]]',
                '$frac(a,#text[绪论#footnote[唯一说明]])$',
                '绪论#[#footnote[唯一说明]<heading-note>]',
                '#context [绪论#footnote(<body-note>)]',
            )
            for kind in ("master", "bachelor"):
                for index, heading in enumerate(headings):
                    with compile_pdf(
                        f"footnotes-{kind}-{index}",
                        entrance(kind) + "#(t.outline-page)()\n#show: t.mainmatter\n= " + heading
                        + ("\n补充说明#footnote[唯一说明]<body-note>\n" if index == 5 else "\n")
                        + "后续说明#footnote[正文说明]\n"
                        + ("再次引用#footnote(<heading-note>)\n" if index == 4 else "")
                        + "#for i in range(90) [测试正文。\n\n]\n"
                        + '#context [最终脚注数：#counter(footnote).final().first()]\n',
                    ) as doc:
                        text = "".join(page.get_text() for page in doc)
                        assert text.count("唯一说明") == 1, text
                        assert text.count("正文说明") == 1, text
                        assert "最终脚注数：2" in text.replace(" ", "").replace("\n", ""), text
                        assert "唯一说明" not in doc[0].get_text(), "目录仍输出脚注"
                        # 允许标题公式中的分数线，但页底不应残留脚注分隔线。
                        assert all(drawing["rect"].y0 < doc[0].rect.height / 2
                                   for drawing in doc[0].get_drawings()), (
                            kind, index, doc[0].get_drawings()
                        )
                        for page in doc:
                            for block in page.get_text("dict")["blocks"]:
                                for line in block.get("lines", []):
                                    for span in line["spans"]:
                                        if span["origin"][1] < 80 and "绪论" in span["text"]:
                                            expected = 7.35 if index == 3 else 10.5
                                            assert abs(span["size"] - expected) < 0.01, span
                                            if index == 2:
                                                assert span["color"] == 0xFF0000, span
                                    header_superscripts = [
                                        span for span in line["spans"]
                                        if span["origin"][1] < 80 and span["size"] < 9
                                        and span["text"].strip().isdigit()
                                    ]
                                    assert not header_superscripts, header_superscripts
                sections = "".join(f"== 第{i}节\n节内正文。\n" for i in range(70))
                with compile_pdf(
                    f"footnotes-multipage-{kind}",
                    entrance(kind)
                    + "#(t.abstract)(body: [摘要内容#footnote[摘要唯一说明]])\n"
                    + '#pagebreak(to: "odd")\n#(t.outline-page)()\n#show: t.mainmatter\n'
                    + "= #context [绪论#footnote[章内唯一说明]]\n正文开始标记。\n"
                    + sections + "== #context [末节#footnote[末节唯一说明]]\n末节正文。\n"
                    + '#context [最终脚注数：#counter(footnote).final().first()]\n',
                ) as doc:
                    text = "".join(page.get_text() for page in doc)
                    for note in ("摘要唯一说明", "章内唯一说明", "末节唯一说明"):
                        assert text.count(note) == 1, (kind, note, text)
                    assert "最终脚注数：3" in text.replace(" ", "").replace("\n", ""), text
                    body_page = next(page.number for page in doc if "正文开始标记" in page.get_text())
                    assert body_page >= 5, (kind, body_page)
                    for page in list(doc)[2:body_page]:
                        assert "唯一说明" not in page.get_text(), (kind, page.number)
                        assert all(drawing["rect"].y0 < page.rect.height / 2
                                   for drawing in page.get_drawings()), (kind, page.number)

        check("直接、延迟、富文本与公式脚注只在正文出现且不跳号", footnotes)

        def headers():
            def check_header(page, expected, odd):
                spans = [
                    span for block in page.get_text("dict")["blocks"]
                    for line in block.get("lines", []) for span in line["spans"]
                    if span["origin"][1] < 70
                ]
                numbers = [span for span in spans if abs(span["size"] - 9) < 0.01]
                titles = [span for span in spans if abs(span["size"] - 10.5) < 0.01]
                assert "".join(span["text"] for span in numbers) == expected, spans
                assert titles, spans
                number_left = min(span["bbox"][0] for span in numbers)
                number_right = max(span["bbox"][2] for span in numbers)
                title_left = min(span["bbox"][0] for span in titles)
                title_right = max(span["bbox"][2] for span in titles)
                assert (title_right <= number_left if odd else number_right <= title_left), spans
                left, right = (40, 20) if odd else (20, 40)
                assert abs((title_left + title_right) / 2
                           - (left + (210 - left - right) / 2) * 72 / 25.4) < 0.1, spans
                assert abs((number_right if odd else number_left)
                           - (210 - right if odd else left) * 72 / 25.4) < 0.1, spans

            # 实际输出覆盖罗马页码、物理奇偶页和跨位数的阿拉伯页码。
            with compile_pdf(
                "header-roman",
                entrance("bachelor", '(title: "' + "题" * 35 + '",)')
                + "#(t.abstract)(body: [摘要。#pagebreak()后续摘要。])\n",
            ) as doc:
                assert len(doc) == 2
                check_header(doc[0], "i", True)
                check_header(doc[1], "ii", False)
            for start in (9, 99):
                with compile_pdf(
                    f"header-arabic-{start}",
                    entrance("bachelor", '(title: "' + "题" * 35 + '",)')
                    + "#show: t.mainmatter\n#counter(page).update(" + str(start) + ")\n= "
                    + "测" * 34 + "\n正文。#pagebreak()续页。#pagebreak()再次续页。\n",
                ) as doc:
                    assert len(doc) == 3
                    for index, page in enumerate(doc):
                        check_header(page, str(start + index), index % 2 == 0)

            # 触发碰撞的宽度必须被拒绝，而不是只在示例 PDF 上碰巧留有余量。
            for size, error in (
                (37, "本科页眉内容过长"),
                (39, "本科页眉内容过长"),
            ):
                source = entrance("bachelor", '(title: "短题目",)') + "#show: t.mainmatter\n= " + "测" * size + "\n正文\n"
                compile_pdf(f"header-reject-{size}", source, error=error)
            # 同一标题在一位页码下容得下，升至三位后必须重新校验。
            source = entrance("bachelor") + "#show: t.mainmatter\n= " + "测" * 35
            with compile_pdf("header-single-digit", source + "\n正文\n") as doc:
                check_header(doc[0], "1", True)
            compile_pdf(
                "header-three-digits",
                entrance("bachelor") + "#show: t.mainmatter\n#counter(page).update(99)\n= "
                + "测" * 35 + "\n正文#pagebreak()续页#pagebreak()再次续页",
                error="本科页眉内容过长",
            )
            compile_pdf(
                "header-even-double-digits",
                entrance("bachelor", '(title: "' + "题" * 39 + '",)')
                + "#show: t.mainmatter\n#counter(page).update(9)\n= 短章名\n正文#pagebreak()续页",
                error="本科页眉内容过长",
            )

        check("本科页眉按实际页码测量并在临界处拒绝碰撞", headers)

    print(f"标题复用回归：通过 {4 - len(failures)} 项，失败 {len(failures)} 项")
    return bool(failures)


if __name__ == "__main__":
    raise SystemExit(main())
