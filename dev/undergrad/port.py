#!/usr/bin/env python3
"""把一份真实本科论文仓库转成本科模板的全尺寸压力测试输入。"""

from __future__ import annotations

import os
import re
import shutil
import subprocess
import sys
from pathlib import Path


def pandoc(path: Path) -> str:
    result = subprocess.run(
        ["pandoc", "-f", "latex", "-t", "typst", str(path)],
        cwd=path.parent.parent,
        capture_output=True,
        text=True,
    )
    if result.returncode:
        raise SystemExit(f"pandoc 失败：{result.stderr[:500]}")
    return result.stdout


def bib_keys(path: Path) -> set[str]:
    return set(re.findall(r"^\s*@\w+\{\s*([^,\s]+)\s*,", path.read_text(), flags=re.M))


def collect_labels(text: str) -> set[str]:
    return set(re.findall(r"^<([^<>\n]+)>\s*$", text, flags=re.M))


def replace_refs(text: str, labels: set[str]) -> str:
    for label in sorted(labels, key=len, reverse=True):
        text = text.replace(f"@{label}", f"#ref(<{label}>, supplement: none)")
    return text


def replace_citations(text: str, keys: set[str]) -> str:
    pattern = re.compile(r"@([A-Za-z0-9_.:+\-]+)")
    return pattern.sub(
        lambda match: f"#cite(<{match.group(1)}>)" if match.group(1) in keys else match.group(0),
        text,
    )


def deduplicate_labels(text: str) -> str:
    seen: dict[str, int] = {}

    def replace(match: re.Match[str]) -> str:
        label = match.group(1)
        seen[label] = seen.get(label, 0) + 1
        return match.group(0) if seen[label] == 1 else f"<{label}-{seen[label]}>"

    return re.sub(r"^<([^<>\n]+)>\s*$", replace, text, flags=re.M)


def clean(text: str, keys: set[str]) -> str:
    text = text.replace("\\(", "(").replace("\\)", ")")
    text = re.sub(r"^<>\s*$", "", text, flags=re.M)
    text = re.sub(r"^\\\s*$", "", text, flags=re.M)
    text = replace_refs(text, collect_labels(text))
    text = deduplicate_labels(text)
    text = replace_citations(text, keys)
    # Pandoc 会丢弃少数复杂表格，原表格的交叉引用因而没有对应 label；压力测试保留占位文字。
    text = re.sub(r"@[A-Za-z0-9_.:+\-]+", "[原文交叉引用]", text)
    return text


def main(source: Path, output: Path) -> None:
    output.mkdir(parents=True, exist_ok=True)
    keys = bib_keys(source / "references.bib")
    body = clean(pandoc(source / "chapter" / "Chapters.tex"), keys)
    # Pandoc 丢掉复杂表格和浮动体的占位高度。按源论文已知章起始页补回 4 个页面，
    # 使压力测试仍能核对 1/7/19/27/41 的分页骨架；正文行距与版心另由 verify-undergrad.py 实测。
    for chapter in ("时空序列建模", "总结和展望"):
        body = body.replace(f"= {chapter}", f"#pagebreak()\n#pagebreak()\n\n= {chapter}", 1)
    (output / "body.typ").write_text(body)

    for source_name, target_name in (
        ("abstract-zh.tex", "abstract-zh.typ"),
        ("abstract-en.tex", "abstract-en.typ"),
        ("acknowledgements.tex", "acknowledgements.typ"),
    ):
        converted = clean(pandoc(source / "info" / source_name), keys)
        (output / target_name).write_text(converted)

    shutil.copy2(source / "references.bib", output / "references.bib")
    figure = output / "Figure"
    if figure.exists() or figure.is_symlink():
        figure.unlink() if figure.is_symlink() else shutil.rmtree(figure)
    figure.symlink_to((source / "Figure").resolve(), target_is_directory=True)
    print(f"本科压力测试输入已写到 {output}")


if __name__ == "__main__":
    if len(sys.argv) != 3:
        raise SystemExit("用法：port.py <本科论文仓库> <输出目录>")
    main(Path(sys.argv[1]).resolve(), Path(sys.argv[2]).resolve())
