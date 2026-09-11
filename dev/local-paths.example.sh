#!/usr/bin/env bash
# 本地素材路径配置（示例）
#
# 用法：复制成 dev/local-paths.sh 并填入本机路径。
# dev/local-paths.sh 已被 .gitignore 忽略，不会提交，也不会出现在发布包中。
# 也可以在命令行用同名环境变量临时覆盖。

# 官方 templet.pdf —— 前置部分对照与逐行对照的基准（学校分发，仓库不含）
export OFFICIAL_PDF="$HOME/xdu-thesis-official/templet.pdf"

# 硕士真实论文仓库目录 —— 压力测试用，需含 main.pdf 与 LaTeX 源码
export STRESS_SRC="$HOME/xdu-thesis-stress"

# 本科论文仓库目录 —— 本科压力测试用，需含 main.pdf、references.bib 与 LaTeX 源码。
# 不设默认值（这类素材通常不公开）：未指定时 dev/check-all.sh 会跳过本科压测一节。
export UNDERGRAD_STRESS_SRC="$HOME/xdu-undergrad-thesis"
export UNDERGRAD_REFERENCE="$UNDERGRAD_STRESS_SRC/main.pdf"
