#!/usr/bin/env bash
# 本科封面素材回归：默认占位符、包外素材路径、逐次覆盖与关闭封面。
set -euo pipefail

REPO="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
TMP="$(mktemp -d)"
trap 'rm -rf "$TMP"' EXIT

export TYPST_PACKAGE_PATH="$TMP/packages"
mkdir -p "$TYPST_PACKAGE_PATH/preview/modern-xdu-thesis" "$TMP/project/assets"
ln -s "$REPO" "$TYPST_PACKAGE_PATH/preview/modern-xdu-thesis/0.1.0"

# 测试素材仅为纯色矩形，用来证明两个包外 path(...) 都由封面实际渲染。
printf '%s\n' '<svg xmlns="http://www.w3.org/2000/svg" width="1463" height="273"><rect width="1463" height="273" fill="#e60000"/></svg>' > "$TMP/project/assets/wordmark.svg"
printf '%s\n' '<svg xmlns="http://www.w3.org/2000/svg" width="100" height="100"><rect width="100" height="100" fill="#0057e7"/></svg>' > "$TMP/project/assets/emblem.svg"

printf '%s\n' \
  '#import "@preview/modern-xdu-thesis:0.1.0": bachelor' \
  '#let cls = bachelor.documentclass()' \
  '#(cls.cover)()' > "$TMP/project/default.typ"
typst compile --root "$TMP/project" "$TMP/project/default.typ" "$TMP/default.pdf" >/dev/null 2>&1
python3 "$REPO/dev/verify-bachelor-cover-assets.py" "$TMP/default.pdf" --mode placeholders

printf '%s\n' \
  '#import "@preview/modern-xdu-thesis:0.1.0": bachelor' \
  '#let cls = bachelor.documentclass(' \
  '  cover-wordmark: path("assets/wordmark.svg"),' \
  '  cover-emblem: path("assets/emblem.svg"),' \
  ')' \
  '#(cls.cover)()' > "$TMP/project/assets-from-class.typ"
typst compile --root "$TMP/project" "$TMP/project/assets-from-class.typ" "$TMP/assets-from-class.pdf" >/dev/null 2>&1
python3 "$REPO/dev/verify-bachelor-cover-assets.py" "$TMP/assets-from-class.pdf" --mode assets

printf '%s\n' \
  '#import "@preview/modern-xdu-thesis:0.1.0": bachelor' \
  '#let cls = bachelor.documentclass()' \
  '#(cls.cover)(' \
  '  cover-wordmark: path("assets/wordmark.svg"),' \
  '  cover-emblem: path("assets/emblem.svg"),' \
  ')' > "$TMP/project/assets-per-call.typ"
typst compile --root "$TMP/project" "$TMP/project/assets-per-call.typ" "$TMP/assets-per-call.pdf" >/dev/null 2>&1
python3 "$REPO/dev/verify-bachelor-cover-assets.py" "$TMP/assets-per-call.pdf" --mode assets

printf '%s\n' \
  '#import "@preview/modern-xdu-thesis:0.1.0": bachelor' \
  '#let cls = bachelor.documentclass(' \
  '  cover-enabled: false,' \
  '  cover-wordmark: path("assets/wordmark.svg"),' \
  '  cover-emblem: path("assets/emblem.svg"),' \
  ')' \
  '#(cls.cover)()' \
  '#page[封面已关闭测试]' > "$TMP/project/disabled.typ"
typst compile --root "$TMP/project" "$TMP/project/disabled.typ" "$TMP/disabled.pdf" >/dev/null 2>&1
python3 "$REPO/dev/verify-bachelor-cover-assets.py" "$TMP/disabled.pdf" --mode disabled

# 当前树不得保留或引用无再分发许可的学校标识图片。
test ! -e "$REPO/bachelor/assets/xdu-name.png"
test ! -e "$REPO/bachelor/assets/xdu-emblem.png"
if rg -n 'xdu-(name|emblem)\.png' \
    "$REPO/bachelor.typ" "$REPO/bachelor" "$REPO/lib.typ" \
    "$REPO/layouts" "$REPO/pages" "$REPO/utils" "$REPO/template"; then
  echo "封面素材回归失败：包文件仍引用已移除图片" >&2
  exit 1
fi

# 负向自测：只替换校名标准字时，占位符验收必须检出缺少一个占位框/标签。
printf '%s\n' \
  '#import "@preview/modern-xdu-thesis:0.1.0": bachelor' \
  '#let cls = bachelor.documentclass()' \
  '#(cls.cover)(cover-wordmark: path("assets/wordmark.svg"))' > "$TMP/project/broken-placeholder.typ"
typst compile --root "$TMP/project" "$TMP/project/broken-placeholder.typ" "$TMP/broken-placeholder.pdf" >/dev/null 2>&1
if python3 "$REPO/dev/verify-bachelor-cover-assets.py" "$TMP/broken-placeholder.pdf" --mode placeholders > "$TMP/broken.log" 2>&1; then
  echo "封面素材负向测试失败：缺少校名标准字占位符未被发现" >&2
  exit 1
fi
grep -q "校名标准字占位" "$TMP/broken.log"

echo "本科封面素材回归通过：默认占位、包外素材、逐次覆盖、关闭封面与负向自测"
