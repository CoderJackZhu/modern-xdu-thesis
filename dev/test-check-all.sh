#!/usr/bin/env bash
# 总入口退出码负向测试：隔离外部素材，逐项注入失败，避免无关失败造成假绿。
set -euo pipefail
REPO="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
TMP="$(mktemp -d)"
trap 'rm -rf "$TMP"' EXIT
mkdir -p "$TMP/repo/dev" "$TMP/repo/examples" "$TMP/bin"
cp "$REPO/dev/check-all.sh" "$TMP/repo/dev/"
touch "$TMP/repo/examples/bachelor-thesis.typ" "$TMP/reference.pdf"
for name in test-undergrad-negative test-bachelor-cover-assets test-check-all; do
  echo 'exit 0' > "$TMP/repo/dev/$name.sh"
done
cat > "$TMP/bin/typst" <<'STUB'
#!/usr/bin/env bash
if [ "$1" = init ]; then
  mkdir -p "$3"
  touch "$3/thesis.typ" "$3/ref.bib"
elif [ "${FAIL_TOOL:-}" = compile ]; then
  echo '故意失败但没有error前缀' >&2
  exit 7
else
  touch "${@: -1}"
fi
STUB
cat > "$TMP/bin/python3" <<'STUB'
#!/usr/bin/env bash
if [ "$1" = -c ]; then echo 33; exit 0; fi
if [ "$(basename "$1")" = "${FAIL_TOOL:-}" ]; then
  echo "故意失败:$FAIL_TOOL"
  exit 1
fi
echo '不合格 0'
STUB
chmod +x "$TMP/bin/typst" "$TMP/bin/python3"
run_check() {
  LC_ALL=C PATH="$TMP/bin:$PATH" FAIL_TOOL="$1" OFFICIAL_PDF="${2:-$TMP/absent}" \
    STRESS_SRC="$TMP/absent" UNDERGRAD_STRESS_SRC="$TMP/absent" \
    UNDERGRAD_REFERENCE="$TMP/reference.pdf" \
    bash "$TMP/repo/dev/check-all.sh" > "$TMP/log" 2>&1
}
if ! run_check ''; then
  cat "$TMP/log"
  echo '失败：隔离基线本身不通过'
  exit 1
fi
for gate in compile verify-review-regressions.py verify-front.py verify-front-x.py \
    verify-index.py verify-body.py test-doctor.py test-bachelor-adjustments.py; do
  if run_check "$gate"; then
    cat "$TMP/log"
    echo "失败：总入口未传递$gate的失败"
    exit 1
  fi
  if ! grep -q '故意失败' "$TMP/log"; then
    cat "$TMP/log"
    echo "失败：未执行$gate"
    exit 1
  fi
done
# 本机配置中的失效路径不能盖掉命令行指定的有效 PDF。
printf 'export OFFICIAL_PDF="%s"\n' "$TMP/absent" > "$TMP/repo/dev/local-paths.sh"
if ! run_check '' "$TMP/reference.pdf" || ! grep -q '✅ 官方逐行对照' "$TMP/log"; then
  cat "$TMP/log"
  echo '失败：命令行官方PDF被本机配置覆盖'
  exit 1
fi
if run_check compare-lines.py "$TMP/reference.pdf" \
    || ! grep -q '故意失败:compare-lines.py' "$TMP/log"; then
  cat "$TMP/log"
  echo '失败：官方逐行对照未执行或失败未传递'
  exit 1
fi
echo '通过：隔离基线、命令行路径优先级及各项失败传播'
