# AGENTS.md — 西安电子科技大学学位论文 Typst 模板

本文件是本仓库的开发与验收规约，供在本仓库工作的开发者参考。
硕士格式数值只认 [docs/格式规格.md](docs/格式规格.md)，本科格式数值只认
[docs/本科规格.md](docs/本科规格.md)。

## 先读这个

1. [docs/格式规格.md](docs/格式规格.md) —— 权威来源、冲突裁定、硬约束（**格式数值只认这里**）
2. [docs/官方要求摘录.md](docs/官方要求摘录.md) —— 官方《撰写要求》原文
3. [docs/版式实现.md](docs/版式实现.md) —— 固定行距等底层机制的实测数据
4. [docs/前置部分规格.md](docs/前置部分规格.md)、[docs/索引部分规格.md](docs/索引部分规格.md)、
   [docs/正文与后置部分规格.md](docs/正文与后置部分规格.md) —— 各部分页面的精确规格与验收结果
5. [写作要求.md](写作要求.md) —— 官方对各部分的要求对照表 + 提交前自查清单

## 项目现状

用 Typst 排版西电本科毕业设计（论文）与硕士学位论文，目标是输出可直接送审的 PDF。

- 包名 `modern-xdu-thesis`，仓库 <https://github.com/CoderJackZhu/modern-xdu-thesis>
- `lib.typ` 是硕士入口；`bachelor.typ` 是本科实现入口，`lib.typ` 仅导出 `bachelor` 模块命名空间
- `typst.toml` 的 `[template]` 保持硕士 `template/thesis.typ`；本科完整示例在 `examples/bachelor-thesis.typ`
- 硕士支持学术/专业学位与盲审；本科支持可开关封面、中英文摘要、目录、正文、附录、参考文献与致谢

硕士用 112 页论文压测；本科用 55 页论文压测。两者的章起始页、参考文献数量与行距均与源论文一致；
本科的分页骨架是在转换脚本补过填充页之后对齐的，「55 页一致」不等于逐页复现（原因见验收报告）。
本科测量与限制见 [docs/本科验收报告.md](docs/本科验收报告.md)。

**改动后先跑 `bash dev/check-all.sh`。**

两处限制不要掩盖：① 字体度量不同导致换行点漂移，逐行 y 无法与官方逐行比对（约束下不可达，
不是待办）；② 附录页缺官方实测依据。另有已确认保留的规格差异（符号对照表字号、
封面/声明跟官方 2024.04 + Word 2025.01），见 README 的「与官方模板的差异」。

## 单源真值（最重要的一条）

**硕士格式数值只认 [格式规格](docs/格式规格.md)，本科格式数值只认
[本科规格](docs/本科规格.md)；两套实现不得互相套用数值。**

- 不得凭记忆、推测或「网上常见做法」填写任何字号 / 间距 / 页边距。
- 不得直接照抄上游 NJU 代码的数值。
- 官方 Word、官方 LaTeX、xduts 三者互相冲突处已逐条裁定，以格式规格为准，不要重新发明。
- 格式规格里的**实现约束**章节是实现层的唯一可行写法（固定行距、章标题段前、页眉页脚定位），
  换写法会导致版式偏差，动手前必读。
- 写页面前先读 `docs/` 下对应的规格。

## 文档地图

| 文件 | 内容 |
|---|---|
| [docs/格式规格.md](docs/格式规格.md) | 权威来源 / 冲突裁定 / 硬约束 / 技术方案 / 验收标准 / 决策记录 |
| [docs/官方要求摘录.md](docs/官方要求摘录.md) | 官方《撰写要求》原文（内容要求） |
| [docs/版式实现.md](docs/版式实现.md) | 固定行距、字体、页眉页脚定位的实测数据与对照 |
| [docs/前置部分规格.md](docs/前置部分规格.md) | 六个前置页面的精确规格 + 验收结果 + 已知偏差 |
| [docs/索引部分规格.md](docs/索引部分规格.md) | 五个索引类页面的精确规格 + 验收结果 + 已知偏差 |
| [docs/正文与后置部分规格.md](docs/正文与后置部分规格.md) | 正文与后置部分的精确规格 + 验收结果 |
| [docs/验收报告.md](docs/验收报告.md) | 验收方法与结果、**已知局限**（逐行 y 不可比等） |
| [docs/与真实论文对照.md](docs/与真实论文对照.md) | 与一份已过检真实论文的逐项对照；官方 LaTeX 有两代 |
| [docs/压力测试报告.md](docs/压力测试报告.md) | 用 112 页真实论文压模板的结果与发现的问题 |
| [写作要求.md](写作要求.md) | 官方要求对照表 + 提交前自查清单（面向使用者） |
| [docs/实现笔记.md](docs/实现笔记.md) | Typst 层面的坑与验证过的写法（实现新页面前必读） |
| [docs/本科规格.md](docs/本科规格.md) | 本科版式规格与每项数值来源 |
| [docs/本科验收报告.md](docs/本科验收报告.md) | 本科 PDF 反向测量、55 页压测、负向测试与已知限制 |
| [docs/本科模块调研.md](docs/本科模块调研.md) | 本科模块的可行性调研、材料清单、许可盘点 |
| `dev/` | 验收与维护工具（不进发布包，`typst.toml` 已 exclude） |
| `README.md` | 面向使用者的说明 |

### 验收工具

**改完模板先跑这一条**，它把硕士回归、本科版式与负向测试、两份真实论文压力测试和分发验收串起来：

```bash
bash dev/check-all.sh
```

单项工具：

```bash
python3 dev/verify-front.py <pdf> --degree <professional|academic>   # 前置部分纵向
python3 dev/verify-front-x.py <pdf> <professional|academic>          # 前置部分横向
python3 dev/verify-index.py <pdf>                                    # 索引类页面
python3 dev/verify-body.py <pdf>                                     # 硕士正文与后置部分
python3 dev/verify-undergrad.py <pdf>                                # 本科版式
python3 dev/verify-undergrad.py <55页源pdf> --reference               # 本科验收尺自检
bash dev/test-undergrad-negative.sh                                  # 本科负向测试
python3 dev/compare-pages.py <官方pdf> <本模板pdf> <输出目录>          # 逐页并排对照图
python3 dev/compare-lines.py <官方pdf> <本模板pdf> <起始页> --map=…   # 逐行版式对照
```

`dev/compare-lines.py` 需要先有「内容与官方一致」的示例论文：
`python3 dev/extract-official.py <官方pdf> dev/test-official-body.typ`。

**压力测试**（改动涉及长文档 / 图表 / 公式 / 文献时值得跑一遍）：

```bash
python3 dev/stress/port.py <真实论文仓库> dev/stress          # LaTeX → Typst 正文
python3 dev/stress/front-data.py <仓库>/chapter dev/stress/front-data.typ
typst compile --root . dev/stress/thesis.typ /tmp/stress.pdf
```

> 逐行 y 不可逐行比对：字体度量不同导致换行点漂移。该脚本只比与换行无关的三项：
> 行距比值、章标题基线、章标题→正文首行。

## 铁律

1. **先验证再声称完成。** 任何改动必须 `typst compile` 通过；不能只读代码就下结论。
   更重要的是：**编译通过不等于输出正确** —— 本仓库历史上的每个 bug 都是「编译零错误、
   无任何警告、输出是错的」：首行缩进全局失效、正文首页页码错、公式无法引用、
   索引编号丢章前缀、填空横线画成点线、前置空白填充页缺页眉页码。版式改动必须用
   PDF 反向测量（见下）。
2. **版式改动必须对照官方输出**，不接受「看起来差不多」。对照目标是官方 `templet.pdf`。
3. **不碰范围外的文件。** `fonts/` 已移出仓库（商业字体，见格式规格 §2.2），不要重新引入。
4. **不引入不必要的依赖。** 加 `@preview/...` 包前先确认标准库做不到。
5. **`template/` 必须自包含。** `typst init` 只复制该目录，任何从这里引用的文件都必须在目录内。
   它复制的是**磁盘内容**，不是 git 里的内容 —— 所以 `.gitignore` 拦不住残留文件（实测
   `template/thesis.pdf` 这类编译产物会被原样发给用户）。**动过 `template/` 前后都要
   `ls template/`**，确认只有示例论文和它的素材（现为 `thesis.typ` + `ref.bib`）。
   改完必须实测：`bash dev/pkg-stage.sh && typst init @preview/modern-xdu-thesis:0.1.0 /tmp/t
   && cd /tmp/t && typst compile thesis.typ` —— 初始化目录 2 个文件、能编译出 33 页才算通过。
6. **中文文档。** 新增注释与文档用中文，与现有风格一致。
7. **不擅自改元数据。** 包名 / 版本 / 作者 / 许可由人决定。改动需同步三处：
   `typst.toml` 的 `name`、`template/thesis.typ` 的 `@preview/…` 引用串、重新运行
   `dev/pkg-stage.sh`（软链目录名必须与 `name` 一致，否则报
   `package manifest contains mismatched name`）。
8. **新增验收项要做负向测试。** 把它本该抓到的错误造回去，确认脚本会报红 —— 否则容易写出
   永远通过的「假绿」（本项目出现过一次：检查只扫了第 1 页，其余页出问题照样报通过）。

## 环境与命令

```bash
bash dev/pkg-stage.sh                               # 首次必跑：把仓库软链进 Typst 本地包目录
typst compile --root . template/thesis.typ out.pdf   # --root . 仍需要
```

**为什么必须先挂软链**：`template/thesis.typ` 用 `@preview/modern-xdu-thesis:0.1.0` 引用包，
不用 `../lib.typ`。因为 `typst init` 只复制 `template/` 目录，相对引用会让初始化出来的项目报
`path would escape the project root`（已实测）。挂上软链后，`typst compile --root . template/thesis.typ`
与 `typst init @preview/modern-xdu-thesis:0.1.0 <dir>` 都不需要额外参数。

- **不需要 `--font-path`**：模板不内置字体，按系统字体解析（见格式规格 §2.2）。
- `unknown font family: simsun / source han serif sc` 的警告是**预期行为** —— 回退链里本机没有的
  候选，不是错误。
- 本机已装 TeX Live 与 `xduts`，可现场编译官方模板做对照：`xelatex -interaction=nonstopmode <file>.tex`
- `fitz`（PyMuPDF）只在系统 `python3` 里，不在代码执行沙箱里 —— 测量脚本走 `terminal` 跑。
- 本仓库是 Typst 模板而非常规代码库，通用代码索引工具（codebase-memory 之类）对它没有结构价值，
  直接读文件或用 `rg` 更快。

### 版式测量（改版式后必跑）

```bash
python3 dev/measure.py <file.typ> [--pages N]          # 基线 / 字号 / 字体清单
python3 dev/verify-front.py <pdf> --degree professional # 前置部分：页 + 基线 y + 字号
python3 dev/verify-front-x.py <pdf> professional        # 前置部分：左边界 x
python3 dev/verify-index.py <pdf>                       # 索引类页面（按标题定位页面）
```

判定标准：

- 固定行距成立 ⇔ 相邻行 Δ 恒为 `20.000`（段内与跨段落都要满足）
- 版心边界 ⇔ A4 = 595.28 × 841.89 bp，`mm = bp / 72 * 25.4`
- A4 关键参照：正文区顶 85.04bp / 左 85.04bp（奇）/ 70.87bp（偶）

**验收脚本必须先拿官方 `templet.pdf` 自检**：期望值正确时官方自身位移应为 0.00。
自检不过说明是期望值或匹配逻辑写错了，不是被验对象的问题。

现写现用的小工具：

- 栅格化墨迹包围盒 → 查文字是否越出页边距。注意用 `pm.stride` 而非 `pm.n` 切行。
- `page.get_drawings()` → 查横线位置、宽度与**线型**（`it[0] == "l"`，线宽在 `dr["width"]`，
  虚线模式在 `dr["dashes"]`；空即实线）。

### 与官方对照

官方 `templet.pdf` 的关键实测值（本模板应对齐）：

| 项 | 官方值 |
|---|---|
| 正文区顶边 | 85.04bp = 30.00mm |
| 正文首行基线 | 99.53bp |
| 页眉文字基线 | 73.18bp |
| 页眉双横线 | 78.36 / 79.36bp，宽 439.37bp（= 正文宽） |
| 页码基线 | 788.84bp |
| 章首页章标题 / 正文首行 | 125.44bp / 163.29bp |
| 版心宽 | 439.37bp = 155.00mm |

前置部分页码位置：封面 p1 / 中文题名页 p3 / 英文题名页 p5 / 声明 p7 / 摘要 p9 / ABSTRACT p11 /
插图索引 p13 / 表格索引 p15 / 符号对照表 p17 / 缩略语对照表 p19 / 目录 p21。

## 官方素材位置

官方材料（Word 模板、官方 LaTeX 包与其编译产物 `templet.pdf`、xduts 源码）由学校分发，
**不在本仓库内**，需要自备。对照验收的基准是官方 `templet.pdf`。

本地路径写进 `dev/local-paths.sh`（已 gitignore，模板见 `dev/local-paths.example.sh`），
或用环境变量 `OFFICIAL_PDF` / `STRESS_SRC` 覆盖；`dev/check-all.sh` 会自动读取。
缺失时相关检查会明确标注「跳过」，其余照常运行 —— 但**对照验收会因此失去基准**，
所以本地必须有一份。

解 docx 的方法：`unar` 解包后读 `word/document.xml` 的 `w:sectPr/w:pgMar`（twips，÷20 = pt）、
`word/styles.xml` 的 `w:spacing`、`word/header*.xml`。

仓库原有的商业字体（Monotype Arial/TNR、方正仿宋/楷体）已移出仓库，**不要提交回仓库**。

## 明确不做

本科毕业设计、博士学位论文、英文撰写的学位论文、开题报告 / 中期考核 / 答辩表格、详细中文摘要。
