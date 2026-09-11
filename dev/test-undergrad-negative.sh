#!/usr/bin/env bash
# 本科 PDF 验收脚本的负向测试：故意造回两类版式错误，确认会报红。
set -euo pipefail

REPO="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
TMP="$(mktemp -d)"
trap 'rm -rf "$TMP"' EXIT

make_case() {
  local name="$1"
  mkdir -p "$TMP/$name/dev"
  cp "$REPO/bachelor.typ" "$TMP/$name/"
  cp -R "$REPO/bachelor" "$REPO/utils" "$TMP/$name/"
  cp "$REPO/dev/test-bachelor.typ" "$TMP/$name/dev/"
}

make_case leading
python3 - "$TMP/leading/bachelor/layout.typ" <<'PY'
import pathlib, sys
path = pathlib.Path(sys.argv[1])
text = path.read_text()
text = text.replace("#let 行距 = 23.4pt", "#let 行距 = 20pt")
path.write_text(text)
PY
typst compile --root "$TMP/leading" "$TMP/leading/dev/test-bachelor.typ" "$TMP/leading.pdf" >/dev/null 2>&1
if python3 "$REPO/dev/verify-undergrad.py" "$TMP/leading.pdf" >"$TMP/leading.log" 2>&1; then
  echo "负向测试失败：20pt 错误行距未被验收脚本发现" >&2
  exit 1
fi
grep -q "正文 1.5 倍行距" "$TMP/leading.log"

make_case header
python3 - "$TMP/header/bachelor/layout.typ" <<'PY'
import pathlib, sys
path = pathlib.Path(sys.argv[1])
text = path.read_text()
text = text.replace("line(length: 100%, stroke: 0.75pt)", "line(length: 100%, stroke: 1.5pt)")
path.write_text(text)
PY
typst compile --root "$TMP/header" "$TMP/header/dev/test-bachelor.typ" "$TMP/header.pdf" >/dev/null 2>&1
if python3 "$REPO/dev/verify-undergrad.py" "$TMP/header.pdf" >"$TMP/header.log" 2>&1; then
  echo "负向测试失败：1.5pt 错误页眉线未被验收脚本发现" >&2
  exit 1
fi
grep -q "页眉线 0.75pt 实线" "$TMP/header.log"

printf '本科验收负向测试通过：错误行距与错误页眉线均被检出\n'
