#!/usr/bin/env python3
"""发布载荷扫描器的负向测试。"""

from __future__ import annotations

import importlib.util
import subprocess
import tempfile
from pathlib import Path


CHECKER_PATH = Path(__file__).with_name("check-release-payload.py")
SPEC = importlib.util.spec_from_file_location("check_release_payload", CHECKER_PATH)
assert SPEC is not None and SPEC.loader is not None
CHECKER = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(CHECKER)


def write(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")


def git(root: Path, *args: str) -> None:
    subprocess.run(("git", "-C", str(root), *args), check=True,
                   stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)


def main() -> int:
    with tempfile.TemporaryDirectory(prefix="modern-xdu-release-test-") as temporary:
        root = Path(temporary)
        git(root, "init", "-q")
        write(root / "typst.toml", """\
[package]
name = "release-scan-test"
version = "0.1.0"
entrypoint = "lib.typ"
exclude = ["docs", "dev"]
""")
        write(root / "README.md", "公开包说明。\n")
        write(root / "pages/declaration.typ", "本人声明所呈交的论文符合学校声明原文。\n")
        write(root / "docs/private.md", "真实论文、实物论文、55 页、112 页、压力测试。\n")
        write(root / "dev/private.txt", "作者本人、私有论文、本人本科论文。\n")
        git(root, "add", ".")

        files, _, hits = CHECKER.scan_repository(root)
        assert Path("docs/private.md") not in files
        assert Path("dev/private.txt") not in files
        assert not hits, f"排除目录或声明正文被误报：{hits}"

        write(root / "lib.typ", "// 私有论文：112 页压力测试\n")
        _, _, hits = CHECKER.scan_repository(root)
        assert hits, "发布载荷中的未跟踪禁用引用未被拦截"
        assert all(relative == Path("lib.typ") for relative, _, _ in hits)

    print("通过：发布包扫描忽略排除目录和声明正文，并能拦截发布载荷中的禁用引用")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
