#!/usr/bin/env python3
"""复核 2026-11-02 压测报告中的 A/B/C 类修复。

测试全部在临时目录和已忽略的 dev/night/out/ 下运行，不修改源码或提交 PDF。
"""

from __future__ import annotations

import os
import json
from pathlib import Path
import shutil
import subprocess
import tempfile

import fitz


ROOT = Path(__file__).resolve().parents[2]
REPRO = ROOT / "dev/night/repro"
OUT = ROOT / "dev/night/out"


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(prefix="xdu-night-fixes-") as temp:
        temp = Path(temp)
        package = temp / "packages/preview/modern-xdu-thesis"
        package.mkdir(parents=True)
        os.symlink(ROOT, package / "0.3.1")
        env = dict(os.environ, TYPST_PACKAGE_PATH=str(temp / "packages"))

        def compile_source(source: Path, output_name: str) -> tuple[subprocess.CompletedProcess[str], Path]:
            output = temp / output_name
            result = subprocess.run(
                ["typst", "compile", "--root", str(ROOT), str(source), str(output)],
                capture_output=True,
                text=True,
                env=env,
            )
            return result, output

        def compile_repro(name: str) -> tuple[subprocess.CompletedProcess[str], Path]:
            return compile_source(REPRO / f"{name}.typ", f"{name}.pdf")

        def expect_ok(result: subprocess.CompletedProcess[str]) -> None:
            assert result.returncode == 0, result.stderr

        def expect_error(result: subprocess.CompletedProcess[str], text: str) -> None:
            assert result.returncode != 0, "预期编译失败，实际通过"
            assert text in result.stderr, result.stderr

        def lines(pdf: Path) -> list[tuple[str, list[dict], float]]:
            rows = []
            for page in fitz.open(pdf):
                for block in page.get_text("dict")["blocks"]:
                    for line in block.get("lines", []):
                        value = "".join(span["text"] for span in line["spans"])
                        if value.strip():
                            rows.append((value, line["spans"], line["spans"][0]["origin"][1]))
            return rows

        # A1：研究生表格内容必须是五号 10.5pt。
        result, pdf = compile_repro("A1-table-font")
        expect_ok(result)
        table_spans = [
            span
            for value, spans, _ in lines(pdf)
            if value in {"参数", "数值", "样本"}
            for span in spans
        ]
        assert table_spans and all(abs(span["size"] - 10.5) < 0.01 for span in table_spans), table_spans
        print("通过 A1：研究生表格内容为 10.5pt")

        # A2：中文自动折行保持 30pt；超出题名页物理空间时给出明确诊断。
        result, pdf = compile_repro("A2-wrapped-title")
        expect_ok(result)
        title_ys = [
            y
            for _, spans, y in lines(pdf)
            if any(abs(span["size"] - 22) < 0.01 for span in spans)
        ]
        assert len(title_ys) >= 2, title_ys
        assert all(abs((b - a) - 30) < 0.01 for a, b in zip(title_ys, title_ys[1:])), title_ys
        result, _ = compile_repro("A2-title-overlap")
        expect_error(result, "中文题名页题目折行后过高")
        print("通过 A2：中文题目自动折行基线差 30pt，超界输入被明确拒绝")

        english_name = "english-title.pdf"
        english_source = OUT / "regression-english-title.typ"
        english_title = "Reliable Modeling and Verification for Complex Systems " * 3
        english_source.write_text(
            '#import "../../../lib.typ": documentclass\n'
            f"#let t = documentclass(info: (title-en: (\"{english_title}\",)))\n"
            "#show: t.doc\n#(t.title-en)()\n"
        )
        try:
            result, pdf = compile_source(english_source, english_name)
            expect_ok(result)
            english_ys = [
                y
                for _, spans, y in lines(pdf)
                if any(abs(span["size"] - 22) < 0.01 for span in spans)
            ]
            assert len(english_ys) >= 2, english_ys
            assert all(abs((b - a) - 30) < 0.01 for a, b in zip(english_ys, english_ys[1:])), english_ys
        finally:
            english_source.unlink(missing_ok=True)
        print("通过 A2：英文题目自动折行基线差 30pt")

        # A3：多行公式编号与最后一行同基线。
        result, pdf = compile_repro("A3-multiline-equation")
        expect_ok(result)
        equation_y = next(y for value, _, y in lines(pdf) if value.startswith("𝑧"))
        number_y = next(y for value, _, y in lines(pdf) if value == "(1-1)")
        assert abs(equation_y - number_y) < 0.01, (equation_y, number_y)
        print("通过 A3：多行公式编号对齐最后一行")

        # A4：本科 body 模式参考文献按条目语言选择“等”/“et al.”。
        result, pdf = compile_repro("A4-bachelor-bilingual")
        expect_ok(result)
        text = "\n".join(page.get_text() for page in fitz.open(pdf))
        assert "et al." in text and "等" not in text, text
        print("通过 A4：本科英文多作者使用 et al.")

        # B1/C2：所有公开入口的 title/author/student-id 使用同一语义校验。
        for name in ("B1-none-title", "B1-bachelor-none-title", "B1-doctor-none-title"):
            result, _ = compile_repro(name)
            expect_error(result, "必填字段 `title`（题目）不能为空")

        entrances = {
            "master": '#import "../../../lib.typ": documentclass\n#let t = documentclass(info: ({field},))\n',
            "bachelor": '#import "../../../bachelor.typ": documentclass\n#let t = documentclass(info: ({field},))\n',
            "proposal": '#import "../../../lib.typ": proposal-documentclass\n#let t = proposal-documentclass(info: ({field},))\n',
            "interim": '#import "../../../lib.typ": interim-documentclass\n#let t = interim-documentclass(info: ({field},))\n',
            "bachelor-proposal": '#import "../../../lib.typ": bachelor-proposal-documentclass\n#let t = bachelor-proposal-documentclass(info: ({field},))\n',
            "bachelor-interim": '#import "../../../lib.typ": bachelor-interim-documentclass\n#let t = bachelor-interim-documentclass(info: ({field},))\n',
            "course-report": '#import "../../../lib.typ": course-report-documentclass\n#let t = course-report-documentclass(info: ({field},))\n',
        }
        checks = {
            "title": ("", "必填字段 `title`（题目）不能为空"),
            "author": ("", "必填字段 `author`（作者姓名）不能为空"),
            "student-id": ("", "必填字段 `student-id`（学号）不能为空"),
        }
        for entrance, template in entrances.items():
            source = OUT / f"regression-validation-{entrance}.typ"
            try:
                for field, (value, message) in checks.items():
                    source.write_text(template.format(field=f"{field}: {json.dumps(value)}"))
                    result, _ = compile_source(source, f"validation-{entrance}-{field}.pdf")
                    expect_error(result, message)
            finally:
                source.unlink(missing_ok=True)
        print("通过 B1/C2：7 个公开入口的题目、作者、学号空值均有中文诊断")

        # C1：固定单行槽位和页眉不再静默折行覆盖。
        result, _ = compile_repro("C1-long-cover-fields")
        expect_error(result, "作者姓名过长")
        result, _ = compile_repro("C1-long-chapter-header")
        expect_error(result, "页眉中的章节名过长")

        bachelor_sources = {
            "author": (
                '#import "../../../bachelor.typ": documentclass\n'
                '#let t = documentclass(info: (author: "'
                + "阿卜杜拉复杂系统联合实验中心研究者姓名很长" * 3
                + '",))\n#show: t.doc\n#(t.cover)()\n',
                "本科封面字段 学生姓名过长",
            ),
            "title": (
                '#import "../../../bachelor.typ": documentclass\n'
                '#let t = documentclass(info: (title: "'
                + "超长本科题目" * 12
                + '",))\n#show: t.doc\n#(t.cover)()\n',
                "本科封面题目折行后过高",
            ),
            "header": (
                '#import "../../../bachelor.typ": documentclass\n'
                '#let t = documentclass()\n#show: t.doc\n#show: t.mainmatter\n= '
                + "复杂系统的鲁棒建模方法与验证" * 5
                + "\n正文\n",
                "本科页眉内容过长",
            ),
        }
        for name, (text, message) in bachelor_sources.items():
            source = OUT / f"regression-bachelor-{name}.typ"
            source.write_text(text)
            try:
                result, _ = compile_source(source, f"bachelor-{name}.pdf")
                expect_error(result, message)
            finally:
                source.unlink(missing_ok=True)
        print("通过 C1：研究生与本科长字段、长题、长章名均不再静默覆盖")

        # C3：五级标题在本科和研究生入口均明确拒绝。
        result, _ = compile_repro("C3-five-level-heading")
        expect_error(result, "标题最多支持四级")
        bachelor_heading = OUT / "regression-bachelor-heading5.typ"
        bachelor_heading.write_text(
            '#import "../../../bachelor.typ": documentclass\n'
            "#let t = documentclass()\n#show: t.doc\n#show: t.mainmatter\n"
            "= 第一章 测试\n== 节\n=== 小节\n==== 四级\n===== 五级\n正文\n"
        )
        try:
            result, _ = compile_source(bachelor_heading, "bachelor-heading5.pdf")
            expect_error(result, "标题最多支持四级")
        finally:
            bachelor_heading.unlink(missing_ok=True)
        print("通过 C3：本科与研究生五级标题均有明确诊断")

        # C4：标题脚注只在正文标题处生成一次。
        result, pdf = compile_repro("C4-heading-footnote")
        expect_ok(result)
        text = "\n".join(page.get_text() for page in fitz.open(pdf))
        assert text.count("唯一的标题说明") == 1, text
        print("通过 C4：标题脚注在目录和页眉中不再重复生成")

        rich_heading = OUT / "regression-rich-heading-footnote.typ"
        rich_heading.write_text(
            '#import "../../../lib.typ": documentclass\n'
            "#let t = documentclass()\n#show: t.doc\n#(t.outline-page)()\n"
            "#show: t.mainmatter\n"
            '= 绪论 #text(fill: rgb("#ff0000"), weight: "bold")[强调#footnote[富文本标题说明]] '
            '#link("https://example.com")[链接#footnote[链接标题说明]] $x^2$\n'
            "#for i in range(70) [测试正文。\n\n]\n"
        )
        try:
            result, pdf = compile_source(rich_heading, "rich-heading-footnote.pdf")
            expect_ok(result)
            rich_lines = lines(pdf)
            text = "\n".join(value for value, _, _ in rich_lines)
            assert text.count("富文本标题说明") == 1, text
            assert text.count("链接标题说明") == 1, text
            emphasized = [
                span
                for _, spans, _ in rich_lines
                for span in spans
                if "强调" in span["text"]
            ]
            assert emphasized and all(span["color"] == 0xFF0000 for span in emphasized), emphasized
        finally:
            rich_heading.unlink(missing_ok=True)
        print("通过 C4：富文本与链接内脚注只生成一次，标题颜色保持不变")

        shutil.rmtree(temp, ignore_errors=True)


if __name__ == "__main__":
    main()
