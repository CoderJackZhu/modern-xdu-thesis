#!/usr/bin/env python3
"""博士学术/专业/盲审/可选导师与失败注入；所有产物在临时目录。"""
import importlib.util
import os
from pathlib import Path
import shutil
import subprocess
import tempfile

import fitz

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location("doctor_verifier", ROOT / "dev/verify-doctor.py")
verifier = importlib.util.module_from_spec(spec)
spec.loader.exec_module(verifier)
word_spec = importlib.util.spec_from_file_location("doctor_word", ROOT / "dev/verify-doctor-word.py")
word_verifier = importlib.util.module_from_spec(word_spec)
word_spec.loader.exec_module(word_verifier)


def main():
    with tempfile.TemporaryDirectory(prefix="xdu-doctor-") as temp:
        tmp = Path(temp)
        package = tmp / "packages/preview/modern-xdu-thesis/0.3.0"
        package.mkdir(parents=True)
        for name in ("lib.typ", "bachelor.typ", "doctor.typ", "typst.toml"):
            shutil.copy2(ROOT / name, package / name)
        for name in ("layouts", "pages", "utils", "bachelor", "supporting"):
            shutil.copytree(ROOT / name, package / name)
        project = tmp / "project"
        project.mkdir()
        source = project / "thesis.typ"
        source.write_text((ROOT / "examples/doctor-thesis.typ").read_text())
        shutil.copy2(ROOT / "examples/doctor-ref.bib", project / "doctor-ref.bib")
        env = dict(os.environ, TYPST_PACKAGE_PATH=str(tmp / "packages"))

        for degree, variable, needle in (
            ("academic", "DOCTOR_ACADEMIC_WORD", "439.45pt"),
            ("professional", "DOCTOR_PROFESSIONAL_WORD", "411.1pt"),
        ):
            path = Path(os.environ.get(variable, ""))
            if not path.is_file():
                print(f"跳过原始Word自检：未设置有效的{variable}")
                continue
            implementation = package / "pages/doctor-front.typ"
            assert not word_verifier.verify(path, degree, implementation)
            saved = implementation.read_text()
            implementation.write_text(saved.replace(needle, "499pt"))
            try:
                errors = word_verifier.verify(path, degree, implementation)
                assert any("cover-title" in error for error in errors), errors
            finally:
                implementation.write_text(saved)
            print("通过：原始Word锚点与其失败注入 " + degree)

        def compile_pdf(name, degree="academic", blind=False, enterprise=True):
            pdf = tmp / f"{name}.pdf"
            result = subprocess.run(
                ["typst", "compile", "--root", str(tmp),
                 "--input", f"degree={degree}", "--input", f"blind={str(blind).lower()}",
                 "--input", f"enterprise={str(enterprise).lower()}", str(source), str(pdf)],
                capture_output=True, text=True, env=env)
            return result, pdf

        for degree in ("academic", "professional"):
            for blind in (False, True):
                for enterprise in ((False, True) if degree == "professional" else (False,)):
                    name = f"{degree}-{blind}-{enterprise}"
                    result, pdf = compile_pdf(name, degree, blind, enterprise)
                    assert result.returncode == 0, result.stderr
                    errors = verifier.verify(pdf, degree, blind, enterprise)
                    assert not errors, (name, errors)
                    print("通过：" + name)

        # 横向尺过去没有退出码；给它确定不符合硕士前置页的博士PDF，须非零退出。
        if os.environ.get("OFFICIAL_PDF"):
            result = subprocess.run(["python3", str(ROOT / "dev/verify-front-x.py"), str(pdf)],
                                    capture_output=True, text=True)
            assert result.returncode == 1 and "不合格" in result.stdout, result.stdout
        else:
            print("跳过硕士横向尺退出码自检：未设置OFFICIAL_PDF（总验收会提供）")

        # 每项都恢复源文件；要求具体错误命中，不能靠无关检查失败冒充负向通过。
        mutations = (
            ("题目纵坐标", "pages/doctor-front.typ", "411.1pt", "421.1pt", "p1 复杂系统的可靠建模"),
            ("英文标题字号", "pages/doctor-front.typ", "size: 22pt", "size: 20pt", "p5 Reliable"),
            ("英文学位误用", "lib.typ", '"Doctor of Engineering"', '"Doctor of Philosophy"', "for the degree"),
            ("正文偶页页眉", "layouts/mainmatter.typ", "学位论文固定标题(graduate)", '学位论文固定标题("master")', "p24"),
            ("前置填充页页眉", "layouts/doc.typ", "页眉(学位论文固定标题(graduate))", '页眉(学位论文固定标题("master"))', "p10"),
            ("身份泄漏", "pages/doctor-front.typ", 'if blind and 标签.contains("姓名")', 'if false and 标签.contains("姓名")', "内置身份字段"),
            ("元数据泄漏", "layouts/doc.typ", "if not blind and", "if true and", "PDF作者元数据隐去"),
            ("博士成果栏", "lib.typ", "攻读博士学位期间的研究成果", "攻读硕士学位期间的研究成果", "博士成果栏"),
        )
        for name, file, old, new, expected in mutations:
            path = package / file
            original = path.read_text()
            assert old in original, (name, "失效的失败注入")
            path.write_text(original.replace(old, new))
            try:
                result, pdf = compile_pdf("negative", "professional", blind=True)
                assert result.returncode == 0, (name, result.stderr)
                errors = verifier.verify(pdf, "professional", True)
                assert any(expected in error for error in errors), (name, errors)
            finally:
                path.write_text(original)
            print("检出：" + name)

        original = source.read_text()
        for part, args in (
            ("acknowledgement", "body: text"),
            ("appendix", "body: text"),
            ("references", 'entries: range(80).map(i => "Author. Reference example. 2026.")'),
            ("bio", 'items: (("攻读博士学位期间的研究成果", text),)'),
        ):
            source.write_text(
                '#import "@preview/modern-xdu-thesis:0.3.0": doctor-documentclass\n'
                '#let t = doctor-documentclass()\n#show: t.doc\n'
                '#let text = [#for i in range(80) [这是一段检查跨页页眉的测试文字。\n\n]]\n'
                f'#(t.{part})({args})')
            result, pdf = compile_pdf("back")
            assert result.returncode == 0, result.stderr
            d = fitz.open(pdf)
            assert len(d) >= 2 and "西安电子科技大学博士学位论文" in d[1].get_text(), part
            path = package / f"pages/{part}.typ"
            saved = path.read_text()
            path.write_text(saved.replace("学位论文固定标题(graduate)", '学位论文固定标题("master")'))
            try:
                result, pdf = compile_pdf("back-negative")
                assert result.returncode == 0, result.stderr
                assert "西安电子科技大学硕士学位论文" in fitz.open(pdf)[1].get_text(), part
            finally:
                path.write_text(saved)
            print("通过并检出故意错误：跨页 " + part)
        # 覆盖两个公开入口、可覆盖的英文学位名称，以及前置页超宽明确拒绝。
        for entry in (
            '#import "@preview/modern-xdu-thesis:0.3.0": documentclass\n#let cls = documentclass.with(graduate: "doctor")',
            '#import "../packages/preview/modern-xdu-thesis/0.3.0/doctor.typ": documentclass as cls',
        ):
            source.write_text(entry + '\n#let t = cls(info: (degree-name-en: "Doctor of Science",))\n'
                              '#show: t.doc\n#(t.cover)()\n#pagebreak(to: "odd")\n#(t.title-en)()')
            result, pdf = compile_pdf("entry")
            assert result.returncode == 0, result.stderr
            assert "Doctor of Science" in "".join(p.get_text() for p in fitz.open(pdf))
        source.write_text('#import "@preview/modern-xdu-thesis:0.3.0": documentclass\n'
                          '#let t = documentclass(graduate: "invalid")\n#show: t.doc\nx')
        result, _ = compile_pdf("invalid")
        assert result.returncode != 0 and "graduate" in result.stderr
        source.write_text('#import "@preview/modern-xdu-thesis:0.3.0": doctor-documentclass\n'
                          '#let t = doctor-documentclass(info: (title: ("长" * 60,),))\n'
                          '#show: t.doc\n#(t.cover)()')
        result, _ = compile_pdf("overflow")
        assert result.returncode != 0 and "超宽" in result.stderr
        source.write_text(original.replace('("Wang Wu", "Senior Engineer")', '(none, none)'))
        result, _ = compile_pdf("bilingual", "professional")
        assert result.returncode != 0 and "同时填写" in result.stderr
        print("通过：包外入口、自定义学位名、参数/超宽/中英文导师校验")


if __name__ == "__main__":
    main()
