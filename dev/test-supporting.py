#!/usr/bin/env python3
"""编译并验收全部配套材料入口，同时做两项失败注入。"""

from __future__ import annotations

import importlib.util
import os
import re
import subprocess
import sys
import tempfile
from pathlib import Path

import fitz


ROOT = Path(__file__).resolve().parent.parent
PYTHON = sys.executable
payload_spec = importlib.util.spec_from_file_location(
    "release_payload", ROOT / "dev/check-release-payload.py"
)
assert payload_spec is not None and payload_spec.loader is not None
release_payload = importlib.util.module_from_spec(payload_spec)
payload_spec.loader.exec_module(release_payload)


def run(command: list[str], *, env: dict[str, str] | None = None) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        command,
        cwd=ROOT,
        env=env,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )


def compile_pdf(
    example: str,
    output: Path,
    env: dict[str, str],
    *inputs: tuple[str, str],
) -> None:
    command = ["typst", "compile", "--root", ".", example, os.fspath(output)]
    for key, value in inputs:
        command.extend(("--input", f"{key}={value}"))
    result = run(command, env=env)
    if result.returncode != 0:
        raise RuntimeError(f"编译失败：{example}\n{result.stdout}\n{result.stderr[-4000:]}")


def verify(
    pdf: Path,
    kind: str,
    env: dict[str, str],
    graduate: str = "master",
    degree: str = "academic",
) -> None:
    result = run(
        [PYTHON, "dev/verify-supporting.py", os.fspath(pdf), "--kind", kind,
         "--graduate", graduate, "--degree", degree],
        env=env,
    )
    if result.returncode != 0:
        raise RuntimeError(result.stdout + result.stderr)
    print(result.stdout.strip())


def page_count(pdf: Path) -> int:
    with fitz.open(pdf) as document:
        return len(document)


def main() -> int:
    with tempfile.TemporaryDirectory(prefix="modern-xdu-supporting-") as temporary:
        temp = Path(temporary)
        packages = temp / "packages"
        manifest = (ROOT / "typst.toml").read_text(encoding="utf-8")
        match = re.search(r'(?m)^version\s*=\s*"([^"]+)"', manifest)
        if match is None:
            raise RuntimeError("typst.toml 缺少 version")
        version = match.group(1)
        payload = temp / "payload"
        files = release_payload.build_release_tree(ROOT, payload)
        required = {
            Path("lib.typ"),
            Path("supporting/layout.typ"),
            Path("supporting/proposal.typ"),
            Path("supporting/interim.typ"),
            Path("supporting/bachelor-forms.typ"),
            Path("supporting/course-report.typ"),
        }
        if missing := sorted(required - set(files), key=str):
            raise RuntimeError("发布载荷缺少配套材料文件：" + "、".join(map(str, missing)))
        package_root = packages / "preview" / "modern-xdu-thesis"
        package_root.mkdir(parents=True)
        (package_root / version).symlink_to(payload, target_is_directory=True)
        env = os.environ.copy()
        env["TYPST_PACKAGE_PATH"] = os.fspath(packages)
        env["PYTHONPYCACHEPREFIX"] = os.fspath(temp / "pycache")

        outputs: dict[str, Path] = {}
        for graduate in ("master", "doctor"):
            for degree in ("academic", "professional"):
                for kind, example in (("proposal", "examples/proposal-thesis.typ"),
                                      ("interim", "examples/interim-thesis.typ")):
                    output = temp / f"{kind}-{graduate}-{degree}.pdf"
                    compile_pdf(example, output, env, ("graduate", graduate), ("degree", degree))
                    verify(output, kind, env, graduate, degree)
                    outputs[f"{kind}-{graduate}-{degree}"] = output

        for kind, example in (
            ("bachelor-proposal", "examples/bachelor-proposal.typ"),
            ("bachelor-interim", "examples/bachelor-interim.typ"),
            ("course-report", "examples/course-report.typ"),
        ):
            output = temp / f"{kind}.pdf"
            compile_pdf(example, output, env)
            verify(output, kind, env)
            outputs[kind] = output

        expected_pages = {
            "proposal-master-academic": (4, 6),
            "proposal-master-professional": (4, 6),
            "proposal-doctor-academic": (4, 6),
            "proposal-doctor-professional": (4, 6),
            "interim-master-academic": (3, 5),
            "interim-master-professional": (3, 5),
            "interim-doctor-academic": (3, 5),
            "interim-doctor-professional": (3, 5),
            "bachelor-proposal": (2, 3),
            "bachelor-interim": (3, 5),
            "course-report": (1, 3),
        }
        for key, (minimum, maximum) in expected_pages.items():
            pages = page_count(outputs[key])
            if not minimum <= pages <= maximum:
                raise RuntimeError(f"{key} 页数越界：{pages}，期望 {minimum}～{maximum}")

        wrong_kind = run(
            [PYTHON, "dev/verify-supporting.py", os.fspath(outputs["bachelor-proposal"]),
             "--kind", "proposal", "--graduate", "master", "--degree", "academic"],
            env=env,
        )
        if wrong_kind.returncode == 0:
            raise RuntimeError("负向测试失败：把本科开题表当成研究生开题表仍然通过")
        print("负向测试：错误 kind 被拒绝")

        wrong_size_source = temp / "wrong-size.typ"
        wrong_size_source.write_text(
            """
#set page(paper: "a5", margin: 1cm)
#set text(size: 12pt)
1 实验目的
本文件为通用课程实验报告示例，不是学校统一模板。
2 实验环境
3 实验原理
4 实验步骤
5 实验结果
6 分析与结论
提交前自查
""".strip()
            + "\n",
            encoding="utf-8",
        )
        wrong_size_pdf = temp / "wrong-size.pdf"
        result = run(["typst", "compile", os.fspath(wrong_size_source), os.fspath(wrong_size_pdf)], env=env)
        if result.returncode != 0:
            raise RuntimeError(f"负向测试稿编译失败：{result.stderr}")
        wrong_size = run(
            [PYTHON, "dev/verify-supporting.py", os.fspath(wrong_size_pdf),
             "--kind", "course-report"],
            env=env,
        )
        if wrong_size.returncode == 0:
            raise RuntimeError("负向测试失败：A5 页面仍然通过")
        print("负向测试：错误 A4 页面尺寸被拒绝")

        wrong_margin_source = temp / "wrong-margin.typ"
        wrong_margin_source.write_text(
            """
#set page(paper: "a4", margin: 1cm)
#set text(size: 12pt, font: "STSongti SC")
#set par(leading: 8pt)
1实验目的
本文件为通用课程实验报告示例，不是学校统一模板。
2实验环境
3实验原理
4实验步骤
5实验结果
6分析与结论
提交前自查
""".strip()
            + "\n",
            encoding="utf-8",
        )
        wrong_margin_pdf = temp / "wrong-margin.pdf"
        result = run(
            ["typst", "compile", os.fspath(wrong_margin_source), os.fspath(wrong_margin_pdf)],
            env=env,
        )
        if result.returncode != 0:
            raise RuntimeError(f"页边距负向测试稿编译失败：{result.stderr}")
        wrong_margin = run(
            [PYTHON, "dev/verify-supporting.py", os.fspath(wrong_margin_pdf),
             "--kind", "course-report"],
            env=env,
        )
        if wrong_margin.returncode == 0:
            raise RuntimeError("负向测试失败：越过 A4 页边距仍然通过")
        print("负向测试：A4 页边距越界被拒绝")
    print("配套材料验收通过：四类研究生 × 开题/中期、两类本科表、课程报告及失败注入全部通过")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except Exception as error:
        print(f"配套材料验收失败：{error}", file=sys.stderr)
        raise SystemExit(1)
