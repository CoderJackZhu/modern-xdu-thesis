#!/usr/bin/env bash
# 验证总入口确实执行新回归，并把失败传递为非零退出码。
set -euo pipefail
REPO="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
TMP="$(mktemp -d)"
trap 'rm -rf "$TMP"' EXIT
mkdir -p "$TMP/repo/dev" "$TMP/repo/examples" "$TMP/bin"
cp "$REPO/dev/check-all.sh" "$TMP/repo/dev/"
touch "$TMP/repo/examples/bachelor-thesis.typ" "$TMP/reference.pdf"
cat > "$TMP/bin/typst" <<'STUB'
#!/usr/bin/env bash
if [ "$1" = init ]; then
  mkdir -p "$3"
  touch "$3/thesis.typ" "$3/ref.bib"
else
  touch "${@: -1}"
fi
STUB
cat > "$TMP/bin/python3" <<'STUB'
#!/usr/bin/env bash
case "$1" in
  *verify-review-regressions.py) echo '回归故意失败'; exit 1 ;;
  -c) echo 33 ;;
  *) echo '不合格 0' ;;
esac
STUB
cat > "$TMP/repo/dev/test-undergrad-negative.sh" <<'STUB'
exit 0
STUB
chmod +x "$TMP/bin/typst" "$TMP/bin/python3"
if LC_ALL=C PATH="$TMP/bin:$PATH" OFFICIAL_PDF="$TMP/absent" STRESS_SRC="$TMP/absent" \
    UNDERGRAD_STRESS_SRC="$TMP/absent" UNDERGRAD_REFERENCE="$TMP/reference.pdf" \
    bash "$TMP/repo/dev/check-all.sh" > "$TMP/log" 2>&1; then
  echo '失败：总入口没有传递新回归的失败'
  exit 1
fi
if ! grep -q '回归故意失败' "$TMP/log"; then
  cat "$TMP/log"
  echo '失败：总入口未执行新回归'
  exit 1
fi
echo '通过：总入口执行新回归并传递失败'
