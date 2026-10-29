#!/usr/bin/env bash
# 一条命令跑完全部验收 —— 改动模板后必跑。
#
# 覆盖：
#   0) 发布包载荷隐私扫描及其负向测试
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

# 命令行环境优先于本机配置，避免有效基准被旧路径覆盖后静默跳过。
EXPLICIT_NAMES=()
EXPLICIT_VALUES=()
for config_name in OFFICIAL_PDF STRESS_SRC UNDERGRAD_STRESS_SRC UNDERGRAD_REFERENCE \
    UNDERGRAD_HANDBOOK UNDERGRAD_WORD DOCTOR_ACADEMIC_WORD DOCTOR_PROFESSIONAL_WORD; do
  if printenv "$config_name" >/dev/null; then
    EXPLICIT_NAMES+=("$config_name")
    EXPLICIT_VALUES+=("${!config_name}")
  fi
done
[ -f dev/local-paths.sh ] && . dev/local-paths.sh
for ((i=0; i<${#EXPLICIT_NAMES[@]}; i++)); do
  export "${EXPLICIT_NAMES[$i]}=${EXPLICIT_VALUES[$i]}"
done
unset EXPLICIT_NAMES EXPLICIT_VALUES config_name

OFFICIAL_PDF="${OFFICIAL_PDF:-$HOME/xdu-thesis-official/templet.pdf}"
STRESS_SRC="${STRESS_SRC:-$HOME/xdu-thesis-stress}"
UNDERGRAD_STRESS_SRC="${UNDERGRAD_STRESS_SRC:-}"
UNDERGRAD_REFERENCE="${UNDERGRAD_REFERENCE:-$UNDERGRAD_STRESS_SRC/main.pdf}"
UNDERGRAD_HANDBOOK="${UNDERGRAD_HANDBOOK:-$HOME/.hermes/assets/xdu-thesis-official/undergrad/jwc-handbook-2019.pdf}"
UNDERGRAD_WORD="${UNDERGRAD_WORD:-$HOME/.hermes/assets/xdu-thesis-official/undergrad/official-word-template.doc}"
export OFFICIAL_PDF
# 博士原始 Word 是可选外部基准；缺失时子检查会明确报告跳过。
export DOCTOR_ACADEMIC_WORD="${DOCTOR_ACADEMIC_WORD:-}"
export DOCTOR_PROFESSIONAL_WORD="${DOCTOR_PROFESSIONAL_WORD:-}"
TMP="$(mktemp -d)"
trap 'rm -rf "$TMP"' EXIT
# 包注册和子检查产物均限制在本次临时目录，避免调用 pkg-stage 改写用户环境。
export TMPDIR="$TMP"
export PYTHONPYCACHEPREFIX="$TMP/pycache"
export TYPST_PACKAGE_PATH="$TMP/packages"
mkdir -p "$TYPST_PACKAGE_PATH/preview/modern-xdu-thesis"
ln -s "$REPO" "$TYPST_PACKAGE_PATH/preview/modern-xdu-thesis/0.1.0"

PASS=0
FAIL=0
ok()  { printf '  ✅ %s\n' "$1"; PASS=$((PASS + 1)); }
bad() { printf '  ❌ %s\n' "$1"; FAIL=$((FAIL + 1)); }
sec() { printf '\n== %s ==\n' "$1"; }
last() { grep -o '不合格[^|]*' | tail -1; }

compile_one() {   # $1=源文件 $2=输出
  if typst compile --root . "$1" "$2" >"$TMP/compile.log" 2>&1; then
    ok "编译 $1"
  else
    cat "$TMP/compile.log"
    bad "编译 $1"; return 1
  fi
}

verify_one() {  # 标题后跟完整命令；失败不能只打印而不计入汇总。
  local label="$1"
  shift
  if "$@" >"$TMP/verify.log" 2>&1; then
    ok "$label"
  else
    cat "$TMP/verify.log"
    bad "$label"
  fi
}

sec "0) 发布包载荷隐私扫描"
if python3 dev/check-release-payload.py && python3 dev/test-release-payload.py; then
  ok "发布包排除规则、隐私扫描与负向测试通过"
else
  bad "发布包隐私扫描失败"
fi

sec "1) 编译所有入口"
ENTRIES=(
  template/thesis.typ dev/test-all.typ dev/test-academic.typ dev/test-index.typ
  dev/test-body.typ dev/test-backmatter.typ dev/test-blind.typ dev/test-bib.typ
  dev/test-official-body.typ dev/test-bachelor.typ examples/bachelor-thesis.typ
  examples/doctor-thesis.typ
)
# 压力测试骨架依赖临时生成素材，统一在第3节生成后编译，不要求私有生成物留在仓库。
for f in "${ENTRIES[@]}"; do compile_one "$f" "$TMP/$(basename "$f").pdf" || true; done

sec "2) 各部分验收"
typst compile --root . template/thesis.typ "$TMP/main.pdf" 2>/dev/null
typst compile --root . dev/test-all.typ "$TMP/pro.pdf" 2>/dev/null
typst compile --root . dev/test-academic.typ "$TMP/aca.pdf" 2>/dev/null
typst compile --root . dev/test-index.typ "$TMP/p3.pdf" 2>/dev/null
typst compile --root . dev/test-official-body.typ "$TMP/ob.pdf" 2>/dev/null

for pair in "$TMP/pro.pdf professional" "$TMP/aca.pdf academic" "$TMP/main.pdf professional"; do
  set -- $pair
  verify_one "前置纵向 $1" python3 dev/verify-front.py "$1" --degree "$2"
  verify_one "前置横向 $1" python3 dev/verify-front-x.py "$1" "$2"
done
for f in "$TMP/p3.pdf" "$TMP/main.pdf" "$TMP/aca.pdf"; do
  verify_one "索引 $f" python3 dev/verify-index.py "$f"
done
for f in "$TMP/main.pdf" "$TMP/aca.pdf"; do
  verify_one "正文 $f" python3 dev/verify-body.py "$f"
done
if [ -f "$OFFICIAL_PDF" ] && [ -f "$TMP/ob.pdf" ]; then
  verify_one "官方逐行对照" python3 dev/compare-lines.py "$OFFICIAL_PDF" "$TMP/ob.pdf" 23 \
    --map=23,24,25,26,27,28,29,30,31,32
else
  echo "  逐行对照：跳过（缺官方 templet.pdf）"
fi

sec "2a) 评审缺陷回归"
if python3 dev/verify-review-regressions.py; then
  ok "匿名、跨页、页码与参考文献 API 回归通过"
else
  bad "评审缺陷回归失败"
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
if bash dev/test-bachelor-cover-assets.sh >/dev/null 2>&1; then
  ok "本科封面用户素材与占位符回归通过"
else
  bad "本科封面用户素材与占位符回归失败"
fi
[ -f "$UNDERGRAD_HANDBOOK" ] \
  && echo "  官方手册：已找到" || echo "  官方手册：未找到（${UNDERGRAD_HANDBOOK}）"
[ -f "$UNDERGRAD_WORD" ] \
  && echo "  官方 Word 样例：已找到" || echo "  官方 Word 样例：未找到（${UNDERGRAD_WORD}）"

sec "2c) 博士版式与失败注入"
verify_one "验收总入口退出码负向测试" bash dev/test-check-all.sh
verify_one "博士学术/专业/盲审/可选导师、包外入口与负向测试" python3 dev/test-doctor.py
verify_one "本科摘要标题、后置顺序与两种引用及负向测试" python3 dev/test-bachelor-adjustments.py

sec "3) 压力测试（真实 112 页论文）"
if [ -d "$STRESS_SRC" ] && [ -f "$STRESS_SRC/main.pdf" ]; then
  # 在临时目录里生成素材并编译。压测输入是私有论文的正文，不放进仓库；
  # 验收脚本也不应改写工作区（曾因此把真实姓名与正文带进过提交）。
  MS_OUT="$TMP/stress"
  mkdir -p "$MS_OUT"
  cp dev/stress/thesis.typ "$MS_OUT/thesis.typ"
  if python3 dev/stress/port.py "$STRESS_SRC" "$MS_OUT" >/dev/null 2>&1; then
    python3 dev/stress/front-data.py "$STRESS_SRC/chapter" "$MS_OUT/front-data.typ" >/dev/null 2>&1
    if typst compile --root "$MS_OUT" "$MS_OUT/thesis.typ" "$TMP/stress.pdf" >/dev/null 2>&1; then
      A=$(python3 -c "import fitz;print(len(fitz.open('$TMP/stress.pdf')))" 2>/dev/null)
      B=$(python3 -c "import fitz;print(len(fitz.open('$STRESS_SRC/main.pdf')))" 2>/dev/null)
      if [ "$A" = "$B" ]; then
        ok "压力测试页数一致（本模板 ${A} = 源论文 ${B}）"
      else
        bad "压力测试页数不一致（本模板 ${A} / 源论文 ${B}）"
      fi
    else
      bad "压力测试稿编译失败"
    fi
  else
    bad "压力测试 LaTeX → Typst 转换失败"
  fi
else
  echo "  跳过（未找到 ${STRESS_SRC}，可用 STRESS_SRC=… 指定）"
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
  echo "  跳过（未找到 ${UNDERGRAD_STRESS_SRC}，可用 UNDERGRAD_STRESS_SRC=… 指定）"
fi

sec "4) 分发验收（typst init 产物自包含且可编译）"
if typst init @preview/modern-xdu-thesis:0.1.0 "$TMP/init" >/dev/null 2>&1; then
  CNT=$(find "$TMP/init" -type f | wc -l | tr -d ' ')
  if typst compile "$TMP/init/thesis.typ" "$TMP/init/out.pdf" >"$TMP/init.log" 2>&1; then
    PAGES=$(python3 -c "import fitz; print(len(fitz.open('$TMP/init/out.pdf')))")
    if [ "$PAGES" = 33 ]; then ok "typst init 产物可编译为33页"; else bad "初始化页数错误（$PAGES）"; fi
  else
    cat "$TMP/init.log"
    bad "typst init 产物编译失败"
  fi
  if [ "$CNT" -eq 2 ]; then ok "产物自包含（$CNT 个文件）"; else bad "初始化应恰有2个文件，实际$CNT个"; fi
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
