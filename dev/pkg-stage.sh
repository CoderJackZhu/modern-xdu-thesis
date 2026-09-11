#!/usr/bin/env bash
# 把本仓库软链进 Typst 的本地包目录，使 `@preview/<name>:<version>` 能解析到当前工作区。
#
# 为什么需要它
# ------------
# `template/thesis.typ` 用 `@preview/modern-xdu-thesis:0.1.0` 引用包，而不是 `../lib.typ`。
# 这是 Typst 模板的硬性要求：`typst init` 只复制 template/ 目录，任何 `../` 引用都会
# 让初始化出来的项目报 `path would escape the project root`。
#
# 挂上软链后这些命令都能直接用，不需要额外参数：
#   typst compile --root . template/thesis.typ out.pdf      # 编译本仓库的示例论文
#   typst init @preview/modern-xdu-thesis:0.1.0 ../my-thesis  # 生成一份新的论文项目
#
# 用软链而不是复制，是为了让仓库里的改动立刻生效。
#
# 用法: bash dev/pkg-stage.sh          挂上（幂等，可重复跑）
#       bash dev/pkg-stage.sh --remove 解除
set -euo pipefail

REPO="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
NAME="$(sed -n 's/^name *= *"\(.*\)"/\1/p' "$REPO/typst.toml")"
VERSION="$(sed -n 's/^version *= *"\(.*\)"/\1/p' "$REPO/typst.toml")"

if [[ -z "$NAME" || -z "$VERSION" ]]; then
  echo "无法从 typst.toml 读出 name / version" >&2
  exit 1
fi

# Typst 的包目录：macOS/Linux 都是 XDG 数据目录下 typst/packages
DATA_HOME="${XDG_DATA_HOME:-$HOME/.local/share}"
if [[ "$(uname)" == "Darwin" ]]; then
  DATA_HOME="$HOME/Library/Application Support"
fi
PKG_DIR="$DATA_HOME/typst/packages/preview/$NAME/$VERSION"

if [[ "${1:-}" == "--remove" ]]; then
  rm -rf "$PKG_DIR"
  echo "已解除：$PKG_DIR"
  exit 0
fi

mkdir -p "$(dirname "$PKG_DIR")"
rm -rf "$PKG_DIR"
ln -s "$REPO" "$PKG_DIR"

echo "已挂上本地包："
echo "  $PKG_DIR"
echo "  -> $REPO"
echo
echo "包名：$NAME  版本：$VERSION"
echo "现在可以直接跑："
echo "  typst compile --root . template/thesis.typ out.pdf"
echo "  typst init @preview/$NAME:$VERSION ../my-thesis"
