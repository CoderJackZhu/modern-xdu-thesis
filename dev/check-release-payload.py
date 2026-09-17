#!/usr/bin/env python3
"""按 typst.toml 的 exclude 语义构造发布载荷并扫描私有夹具引用。"""

from __future__ import annotations

import argparse
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path


FORBIDDEN = (
    ("55 页", re.compile(r"55[ \t]*页")),
    ("112 页", re.compile(r"112[ \t]*页")),
    ("真实论文", re.compile(r"真实论文")),
    ("实物论文", re.compile(r"实物论文")),
    ("实际论文", re.compile(r"实际论文")),
    ("私有论文", re.compile(r"私有论文")),
    ("私人论文", re.compile(r"私人论文")),
    ("参考论文", re.compile(r"参考论文")),
    ("源论文", re.compile(r"源论文")),
    ("个人本科论文", re.compile(r"个人本科论文|本人本科论文|作者的本科论文")),
    ("作者本人", re.compile(r"作者本人")),
    ("已过检", re.compile(r"已过检")),
    ("私有夹具", re.compile(r"(?:私有|私人)(?:论文)?(?:测试)?夹具")),
    ("论文测试历史", re.compile(r"压力测试|压测|测试论文")),
    ("英文页数声明", re.compile(r"\b(?:55|112)[ -]?pages?\b", re.IGNORECASE)),
    ("英文私有论文声明", re.compile(
        r"\b(?:private|personal|real|actual)\s+"
        r"(?:(?:bachelor(?:'s)?|master(?:'s)?|undergraduate)\s+)?thes(?:is|es)\b",
        re.IGNORECASE,
    )),
    ("英文压力测试", re.compile(r"\bstress[- ]?test(?:s|ing)?\b", re.IGNORECASE)),
)


def _git_paths(root: Path, *args: str) -> list[Path]:
    result = subprocess.run(
        ("git", "-C", os.fspath(root), *args),
        check=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    return [Path(os.fsdecode(item)) for item in result.stdout.split(b"\0") if item]


def manifest_excludes(root: Path) -> list[str]:
    content = (root / "typst.toml").read_text(encoding="utf-8")
    package = re.search(r"(?ms)^\[package\]\s*(.*?)(?=^\[|\Z)", content)
    if package is None:
        raise ValueError("typst.toml 缺少 [package] 段")
    match = re.search(r"(?ms)^\s*exclude\s*=\s*(\[[^\]]*\])", package.group(1))
    excludes = [] if match is None else json.loads(match.group(1))
    if not isinstance(excludes, list) or not all(isinstance(item, str) for item in excludes):
        raise ValueError("typst.toml 的 package.exclude 必须是字符串数组")
    return excludes


def release_files(root: Path) -> list[Path]:
    """返回会进入包载荷的文件，排除规则由 Git 按 gitignore 语义解释。"""
    candidates = set(_git_paths(
        root, "ls-files", "--cached", "--others", "--exclude-standard", "-z",
    ))
    excludes = manifest_excludes(root)
    excluded: set[Path] = set()
    if excludes:
        options = tuple(f"--exclude={pattern}" for pattern in excludes)
        excluded.update(_git_paths(
            root, "ls-files", "--cached", "--ignored", "-z", *options,
        ))
        excluded.update(_git_paths(
            root, "ls-files", "--others", "--ignored", "-z", *options,
        ))
    return sorted(candidates - excluded, key=lambda path: os.fsencode(path))


def build_release_tree(root: Path, destination: Path) -> list[Path]:
    files = release_files(root)
    for relative in files:
        source = root / relative
        target = destination / relative
        target.parent.mkdir(parents=True, exist_ok=True)
        if source.is_symlink():
            target.symlink_to(os.readlink(source))
        else:
            shutil.copy2(source, target)
    return files


def scan_repository(root: Path) -> tuple[list[Path], int, list[tuple[Path, int, str]]]:
    with tempfile.TemporaryDirectory(prefix="modern-xdu-release-") as temporary:
        staging = Path(temporary)
        files = build_release_tree(root, staging)
        text_files = 0
        hits: list[tuple[Path, int, str]] = []
        for relative in files:
            path = staging / relative
            if not path.is_file():
                continue
            try:
                content = path.read_text(encoding="utf-8")
            except UnicodeDecodeError:
                continue
            text_files += 1
            for line_number, line in enumerate(content.splitlines(), start=1):
                for label, pattern in FORBIDDEN:
                    if pattern.search(line):
                        hits.append((relative, line_number, label))
        return files, text_files, hits


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--repo",
        type=Path,
        default=Path(__file__).resolve().parent.parent,
        help="待扫描仓库（默认是脚本所在仓库）",
    )
    parser.add_argument("--list", action="store_true", help="同时列出模拟发布载荷")
    args = parser.parse_args()
    root = args.repo.resolve()

    try:
        files, text_files, hits = scan_repository(root)
    except (OSError, subprocess.CalledProcessError, ValueError, json.JSONDecodeError) as error:
        print(f"发布包扫描失败：{error}", file=sys.stderr)
        return 2

    if args.list:
        for relative in files:
            print(relative.as_posix())

    if hits:
        print("发布包包含私有论文夹具引用：", file=sys.stderr)
        for relative, line_number, label in hits:
            print(f"  {relative.as_posix()}:{line_number}: {label}", file=sys.stderr)
        return 1

    print(f"发布包扫描通过：{len(files)} 个载荷文件，{text_files} 个 UTF-8 文本文件，0 个禁用引用")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
