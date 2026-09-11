#!/usr/bin/env bash
# 一条命令跑完全部验收 —— 改动模板后必跑。
#
# 覆盖：
#   1) 所有入口文件能否编译
#   2) 各部分验收脚本（前置 / 索引 / 正文 / 逐行对照）
#   3) 压力测试（需一份真实论文的 LaTeX 源 + main.pdf；缺失则跳过）
#   4) 分发验收（typst init 产物自包含且可编译）
#
# 用法: bash dev/check-all.sh
#
# 两项需要外部素材的检查：
#   OFFICIAL_PDF  官方 templet.pdf —— 用于前置部分对照与逐行对照
#   STRESS_SRC    真实论文仓库目录 —— 用于压力测试（含 main.pdf）
# 两者都不在仓库内（官方材料由学校分发，真实论文为第三方作品），需要自备。
# 把路径写进 dev/local-paths.sh（已 gitignore，见同目录的 .example.sh），
# 或用环境变量临时覆盖。缺失时对应检查会明确标注「跳过」，其余照常。
#
# 注意：变量名只能用 ASCII —— bash 不支持中文标识符。
set -uo pipefail

REPO="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$REPO"

[ -f dev/local-paths.sh ] && . dev/local-paths.sh

OFFICIAL_PDF="${OFFICIAL_PDF:-$HOME/xdu-thesis-official/templet.pdf}"
STRESS_SRC="${STRESS_SRC:-$HOME/xdu-thesis-stress}"
UNDERGRAD_STRESS_SRC="${UNDERGRAD_STRESS_SRC:-$HOME/xdu-undergrad-thesis}"
UNDERGRAD_REFERENCE="${UNDERGRAD_REFERENCE:-$UNDERGRAD_STRESS_SRC/main.pdf}"
UNDERGRAD_HANDBOOK="${UNDERGRAD_HANDBOOK:-$HOME/.hermes/assets/xdu-thesis-official/undergrad/jwc-handbook-2019.pdf}"
UNDERGRAD_WORD="${UNDERGRAD_WORD:-$HOME/.hermes/assets/xdu-thesis-official/undergrad/official-word-template.doc}"
export OFFICIAL_PDF
TMP="$(mktemp -d)"
trap 'rm -rf "$TMP"' EXIT

PASS=0
FAIL=0
ok()  { printf '  ✅ %s\n' "$1"; PASS=$((PASS + 1)); }
bad() { printf '  ❌ %s\n' "$1"; FAIL=$((FAIL + 1)); }
sec() { printf '\n== %s ==\n' "$1"; }
last() { grep -o '不合格[^|]*' | tail -1; }

compile_one() {   # $1=源文件 $2=输出
  if typst compile --root . "$1" "$2" 2>&1 | grep -q '^error'; then
    bad "编译 $1"; return 1
  fi
  ok "编译 $1"; return 0
}

sec "1) 编译所有入口"
ENTRIES=(
  template/thesis.typ dev/test-all.typ dev/test-academic.typ dev/test-index.typ
  dev/test-body.typ dev/test-backmatter.typ dev/test-blind.typ dev/test-bib.typ
  dev/test-official-body.typ dev/stress/thesis.typ dev/test-bachelor.typ
  examples/bachelor-thesis.typ
)
for f in "${ENTRIES[@]}"; do compile_one "$f" "$TMP/$(basename "$f").pdf" || true; done

sec "2) 各部分验收"
typst compile --root . template/thesis.typ "$TMP/main.pdf" 2>/dev/null
typst compile --root . dev/test-all.typ "$TMP/pro.pdf" 2>/dev/null
typst compile --root . dev/test-academic.typ "$TMP/aca.pdf" 2>/dev/null
typst compile --root . dev/test-index.typ "$TMP/p3.pdf" 2>/dev/null
typst compile --root . dev/test-official-body.typ "$TMP/ob.pdf" 2>/dev/null

printf '  前置纵向 专/学/主 : '
for pair in "$TMP/pro.pdf professional" "$TMP/aca.pdf academic" "$TMP/main.pdf professional"; do
  set -- $pair
  if [ -f "$1" ]; then printf '%s | ' "$(python3 dev/verify-front.py "$1" --degree "$2" 2>&1 | last)"; else printf '(缺) | '; fi
done; echo
printf '  前置横向 专/学/主 : '
for pair in "$TMP/pro.pdf professional" "$TMP/aca.pdf academic" "$TMP/main.pdf professional"; do
  set -- $pair
  if [ -f "$1" ]; then printf '%s | ' "$(python3 dev/verify-front-x.py "$1" "$2" 2>&1 | last)"; else printf '(缺) | '; fi
done; echo
printf '  索引 专测/主/学硕 : '
for f in "$TMP/p3.pdf" "$TMP/main.pdf" "$TMP/aca.pdf"; do
  if [ -f "$f" ]; then printf '%s | ' "$(python3 dev/verify-index.py "$f" 2>&1 | last)"; else printf '(缺) | '; fi
done; echo
for pair in "$TMP/main.pdf 主模板" "$TMP/aca.pdf 学硕档"; do
  set -- $pair
  if [ -f "$1" ]; then
    printf '  正文 %-8s     : %s\n' "$2" "$(python3 dev/verify-body.py "$1" 2>&1 | last)"
  fi
done
if [ -f "$OFFICIAL_PDF" ] && [ -f "$TMP/ob.pdf" ]; then
  printf '  逐行对照         : %s\n' \
    "$(python3 dev/compare-lines.py "$OFFICIAL_PDF" "$TMP/ob.pdf" 23 \
        --map=23,24,25,26,27,28,29,30,31,32 2>&1 | last)"
else
  echo "  逐行对照      : 跳过（缺官方 templet.pdf）"
fi

sec "2b) 本科版式验收"
if typst compile --root . dev/test-bachelor.typ "$TMP/undergrad.pdf" >/dev/null 2>&1 \
    && python3 dev/verify-undergrad.py "$TMP/undergrad.pdf" >/dev/null 2>&1; then
  ok "本科示例 PDF 版式通过"
else
  bad "本科示例 PDF 版式失败"
fi
if [ -f "$UNDERGRAD_REFERENCE" ]; then
  if python3 dev/verify-undergrad.py "$UNDERGRAD_REFERENCE" --reference >/dev/null 2>&1; then
    ok "本科验收尺在 55 页实物论文上自检通过"
  else
    bad "本科验收尺未通过实物论文自检"
  fi
else
  echo "  跳过实物论文自检（未找到 $UNDERGRAD_REFERENCE）"
fi
if bash dev/test-undergrad-negative.sh >/dev/null 2>&1; then
  ok "本科验收负向测试通过"
else
  bad "本科验收负向测试失败"
fi
[ -f "$UNDERGRAD_HANDBOOK" ] \
  && echo "  官方手册：已找到" || echo "  官方手册：未找到（$UNDERGRAD_HANDBOOK）"
[ -f "$UNDERGRAD_WORD" ] \
  && echo "  官方 Word 样例：已找到" || echo "  官方 Word 样例：未找到（$UNDERGRAD_WORD）"

sec "3) 压力测试（真实 112 页论文）"
if [ -d "$STRESS_SRC" ] && [ -f "$STRESS_SRC/main.pdf" ]; then
  python3 dev/stress/port.py "$STRESS_SRC" dev/stress >/dev/null 2>&1
  python3 dev/stress/front-data.py "$STRESS_SRC/chapter" dev/stress/front-data.typ >/dev/null 2>&1
  if compile_one dev/stress/thesis.typ "$TMP/stress.pdf" >/dev/null 2>&1; then
    python3 - "$TMP/stress.pdf" "$STRESS_SRC/main.pdf" <<'PY'
import sys, fitz
a, b = len(fitz.open(sys.argv[1])), len(fitz.open(sys.argv[2]))
print(f"  {'✅' if a == b else '❌'} 页数：本模板 {a} / 源论文 {b}")
PY
  fi
else
  echo "  跳过（未找到 $STRESS_SRC，可用 STRESS_SRC=… 指定）"
fi

sec "3b) 压力测试（真实 55 页本科论文）"
if [ -d "$UNDERGRAD_STRESS_SRC" ] && [ -f "$UNDERGRAD_STRESS_SRC/main.pdf" ]; then
  UG_OUT="$TMP/undergrad-stress"
  if python3 dev/undergrad/port.py "$UNDERGRAD_STRESS_SRC" "$UG_OUT" >/dev/null 2>&1; then
    cp dev/undergrad/stress.typ "$UG_OUT/thesis.typ"
    if typst compile --root "$UG_OUT" "$UG_OUT/thesis.typ" "$UG_OUT/thesis.pdf" >/dev/null 2>&1 \
        && python3 dev/verify-undergrad.py "$UG_OUT/thesis.pdf" --stress >/dev/null 2>&1; then
      ok "本科 55 页压力测试通过（章起始页与 27 条文献一致）"
    else
      bad "本科 55 页压力测试编译或验收失败"
    fi
  else
    bad "本科压力测试 LaTeX → Typst 转换失败"
  fi
else
  echo "  跳过（未找到 $UNDERGRAD_STRESS_SRC，可用 UNDERGRAD_STRESS_SRC=… 指定）"
fi

sec "4) 分发验收（typst init 产物自包含且可编译）"
PKG="$HOME/Library/Application Support/typst/packages/preview/modern-xdu-thesis/0.1.0"
[ -e "$PKG" ] || PKG="$HOME/.local/share/typst/packages/preview/modern-xdu-thesis/0.1.0"
[ -e "$PKG" ] || bash dev/pkg-stage.sh >/dev/null 2>&1
if typst init @preview/modern-xdu-thesis:0.1.0 "$TMP/init" >/dev/null 2>&1; then
  CNT=$(find "$TMP/init" -type f | wc -l | tr -d ' ')
  if typst compile "$TMP/init/thesis.typ" "$TMP/init/out.pdf" 2>&1 | grep -q '^error'; then
    bad "typst init 产物编译失败"
  else
    ok "typst init 产物可编译"
  fi
  if [ "$CNT" -le 6 ]; then ok "产物自包含（$CNT 个文件）"; else bad "产物混入库文件（$CNT 个）"; fi
else
  bad "typst init 失败"
fi
cp examples/bachelor-thesis.typ "$TMP/bachelor-thesis.typ"
if typst compile --root "$TMP" "$TMP/bachelor-thesis.typ" "$TMP/bachelor-out.pdf" >/dev/null 2>&1; then
  ok "本科独立入口可在包外编译"
else
  bad "本科独立入口包外编译失败"
fi

sec "汇总"
printf '  通过 %d 项，失败 %d 项\n' "$PASS" "$FAIL"
[ "$FAIL" -eq 0 ] && echo "  全部通过" || echo "  有失败项"
exit $((FAIL > 0))
