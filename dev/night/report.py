#!/usr/bin/env python3
"""汇总经人工分类的证据，报告只写到用户指定的仓库外目录。"""
from collections import defaultdict
from datetime import datetime, timezone, timedelta
import hashlib
import json
from pathlib import Path
import re
import subprocess
import time

HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[1]
REPORT=ROOT.parent/'night-reports/xdu-thesis-stress-20261102.md'
START=1793558906

def main():
    rounds=[json.loads((HERE/f'results-r{r:02}.json').read_text()) for r in (1,2,3)]
    cases=[c for r in rounds for c in r['cases']]
    # 将现有验收尺的真实失败文本收进可提交JSON，PDF和完整输出继续留在忽略目录。
    for batch in rounds:
        for c in batch['cases']:
            for old in c['legacy']:
                log=HERE/'out'/(c['name']+'.'+old['script']+'.log')
                if log.exists() and old['rc']:
                    old['failures']=[line.strip() for line in log.read_text().splitlines() if '❌' in line or line.startswith('不合格：') or line.startswith('  - ')]
        (HERE/f'results-r{batch["round"]:02}.json').write_text(json.dumps(batch,ensure_ascii=False,indent=2)+'\n')
    by=defaultdict(list)
    for c in cases:by[c['id']].append(c)
    coverage=[]
    for profile,items in by.items():
        fail=sum(c['compile_rc']!=0 for c in items)
        legacy=sum(any(x['rc'] for x in c['legacy']) for c in items)
        generic=sum(bool((c.get('general') or {}).get('issues')) for c in items)
        coverage.append(f'| `{profile}` | {len(items)} | {fail} | {legacy} / {generic} |')
    passed=[c for c in cases if c['compile_rc']==0]
    pages=sum(c['general']['pages'] for c in passed)
    log=(HERE/'out/check-all.log').read_text()
    status=json.loads((HERE/'check-all-status.json').read_text())
    assert status['exit_code']==0 and '通过 38 项，失败 0 项' in log
    blind=json.loads((HERE/'blind-results.json').read_text())
    assert not blind['failed']
    package_link=Path.home()/'Library/Application Support/typst/packages/preview/modern-xdu-thesis/0.3.1'
    assert package_link.is_symlink() and package_link.resolve()==ROOT.parent/'modern-xdu-thesis'
    skips=[line.strip() for line in log.splitlines() if '跳过' in line or '未找到' in line]
    elapsed=int(time.time()-START)
    base=rounds[0]['base']
    matched=all(hashlib.sha256((ROOT/c['source']).read_bytes()).hexdigest()==c['source_sha256'] for c in cases)
    body=f'''# modern-xdu-thesis 压测报告（2026-11-02）

## 结论

发现 **4 条 A 类、1 条 B 类、4 条 C 类**；毕业季前建议先修 **A1：研究生表格字号默认为12pt，而规格要求10.5pt**，它影响普通写法，无需极端输入即可出现。共测20个入口配置、680份文档，第二、三轮各40份均无新增问题；官网发现较新的本科工作通知与表格发布入口，研究生页面附件版本与仓库记录一致，未下载附件核查正文差异。

模板、既有验收脚本和规格均未修改；以下问题均在 `origin/main` 的 `{base}` 上复现。最终源码和该基准的差异仅有 `dev/night/`；复现不是在修补后的模板上进行。

## A 类：模板缺陷

### A1 研究生表格内容未采用五号

- 入口与场景：`lib.typ` 学术/专业硕士及 `doctor.typ` 学术/专业博士；普通表格、长表。
- 现象：零编译错误，表题10.500pt，但“参数”“数值”“样本”单元格文字为 **12.000pt**；四个非盲审基线配置均测得12pt。最小复现第1页表题基线157.109bp，单元格首行188.109bp。
- 违反的规格：`docs/格式规格.md` §2.2 字体字号，原文表项“表格内容 | 宋体 | TNR | 五号 | 居中”；同节定义“五号10.5pt”。博士未另列主体差异，继承该要求。这里不把表格内边距当成正文行距缺陷。
- 判断：A；仅写标准 `figure(table(...))` 即可出现，用户没有覆盖字号。
- 最小复现：`dev/night/repro/A1-table-font.typ`。
- 复现命令：`typst compile --root . dev/night/repro/A1-table-font.typ dev/night/out/A1-table-font.pdf`。

### A2 硕士题目自动折行后不再保持30pt，过长时覆盖字段

- 入口与场景：`lib.typ`，中英文长题目；学术/专业，盲审开/关。
- 现象：最小封面题目三行基线 **488.608、517.408、546.208bp**，相邻差 **28.800bp**，不是30pt。另一份六行中文题名页复现的题目末行569.764bp，与作者字段568.885bp仅差 **0.879bp**，PNG可见文字覆盖；长英文题目也进入固定中部说明区。
- 违反的规格：`docs/前置部分规格.md` §1，原文“题目若超过2行，行距同30pt”；§2.3 题目“固定30pt”；§3 英文题名页题目“固定30pt”。这些是 `docs/格式规格.md` 对题名页行距例外的具体页面规格，不套用正文20pt。
- 判断：A；入口明确接受字符串题目，自动折行分支没有维持该行距，也未对覆盖给出提示。博士按专用规格明确拒绝超宽题目，未把该拒绝算作新缺陷。
- 最小复现：`dev/night/repro/A2-wrapped-title.typ`；覆盖问题另见 `dev/night/repro/A2-title-overlap.typ`。
- 复现命令：`typst compile --root . dev/night/repro/A2-wrapped-title.typ dev/night/out/A2-wrapped-title.pdf`；将文件名改为 `A2-title-overlap` 可复现覆盖。

### A3 多行公式编号没有对齐最后一行

- 入口与场景：研究生正文，多行对齐公式及引用。
- 现象：两行公式基线 **151.447、167.675bp**，编号 `(1-1)` 基线 **163.175bp**，比最后一行高 **4.500bp**；引用能解析，编译没有错误，PNG显示编号位于两行之间。
- 违反的规格：`docs/格式规格.md` §2.5 要求公式分章编号、置于最右；`docs/正文与后置部分规格.md` §5 原文“序号置于该式所在行（有续行时置于最后一行）的最右边”。
- 判断：A；编号横向位置和引用正确，但续行时纵向位置违反明文要求。
- 最小复现：`dev/night/repro/A3-multiline-equation.typ`。
- 复现命令：`typst compile --root . dev/night/repro/A3-multiline-equation.typ dev/night/out/A3-multiline-equation.pdf`。

### A4 本科双语参考文献开关未生效

- 入口与场景：`bachelor.typ`，BibTeX英文文献四位作者，`references(双语: true)`。
- 现象：参考文献实际输出 `ALPHA A, BETA B, GAMMA C, 等.`，没有 `et al.`。300条中英混合文献样本中，本科输出300处“等”、0处“et al”；同一文献数据经研究生入口得到150处“et al”。
- 违反的规格：`docs/本科规格.md` §七原文“本科采用GB/T 7714-2015”；`README.md` “特性”原文“中文文献‘等’与英文文献‘et al.’自动区分”。本科 `references` 也提供默认开启的 `双语` 参数，实际正文直接输出 `body`，没有应用该开关。
- 判断：A；是公开参数和承诺功能无效，未扩展为行政表对裸 `bibliography()` 的语言保证。
- 最小复现：`dev/night/repro/A4-bachelor-bilingual.typ` 与同目录 `A4-english.bib`。
- 复现命令：`typst compile --root . dev/night/repro/A4-bachelor-bilingual.typ dev/night/out/A4-bachelor-bilingual.pdf`。

## B 类：报错不友好

### B1 空值题目暴露内部方法错误，未指出应填写哪个字段

- 入口与场景：本科、硕士、博士；显式将必填题目设为 `none`。
- 现象：本科和硕士报 `type none has no method enumerate`；博士报 `type none has no method len`。硕士最小复现定位到 `pages/cover.typ` 的 `题目列表.enumerate()`，用户调用处只显示 `(t.cover)()`；没有“title/题目不可为空”的解释。行政表相同空值测试报通用的 `expected string or array, found none`。
- 对应规格：`docs/前置部分规格.md` §1、`docs/本科规格.md` §六、`docs/博士规格.md` “字段及内容”均列出题目字段；没有规定 `none` 为合法题目。本任务要求“必填字段留空应给出清楚的报错”。
- 判断：B；输入无效，不将其编译失败计作A。这里仅指出诊断缺少字段语义，不要求模板接受空题目。
- 最小复现：`dev/night/repro/B1-none-title.typ`、`B1-bachelor-none-title.typ`、`B1-doctor-none-title.typ`。
- 复现命令：`typst compile --root . dev/night/repro/B1-none-title.typ dev/night/out/B1-none-title.pdf`（预期非零退出）；其它入口替换文件名。

## C 类：规格没覆盖

### C1 长字段和长章名缺少溢出处理策略

- 入口与场景：硕士封面长姓名、导师等字段；本科长题目/字段；长章名页眉。
- 现象：最小长姓名复现中，姓名自动折为5行，基线678.444～781.484bp，行距25.760bp；导师栏固定基线708.444bp，姓名第二行704.204bp与其重叠。首轮两份长字段文档的可见墨迹到 **839bp**，接近纸底。长章名页眉折行后进入双横线以下，与正文标题区相接。
- 对应规格与空白：`docs/前置部分规格.md` §1规定字段固定行基线，`docs/格式规格.md` §2.3规定页眉位置，`docs/本科规格.md` §六规定封面字段位置；均未规定这些输入的最大长度、缩排、缩小、截断或拒绝规则。博士已有明确超宽诊断，未混入本项。
- 判断：C；可见覆盖成立，但尚无依据替用户决定应该自动缩字还是报错。题目30pt行距违反明文的部分单列A2。
- 最小复现：`dev/night/repro/C1-long-cover-fields.typ`；页眉补充复现 `dev/night/repro/C1-long-chapter-header.typ`。
- 复现命令：`typst compile --root . dev/night/repro/C1-long-cover-fields.typ dev/night/out/C1-long-cover-fields.pdf`；页眉样本替换文件名。

### C2 空字符串必填字段静默通过

- 入口与场景：20个配置均输入空题目、空作者、空学号；本科/研究生及行政表。
- 现象：空字符串均能编译，没有缺字段诊断。最小复现的封面没有22pt题目文字，作者/学号只剩标签或空横线。本科空题目还使6张编号区填充页没有页眉文字；页码仍在。
- 对应规格与空白：上述各入口规格列出了这些字段，但没有区分“可先留白的草稿”与“可交付论文”，没有必填校验时机/严重程度约定。
- 判断：C；不把缺少空字符串校验擅自提升为数值违规，建议明确草稿/定稿策略。`none` 报错的信息质量另列B1。
- 最小复现：`dev/night/repro/C2-empty-required.typ`。
- 复现命令：`typst compile --root . dev/night/repro/C2-empty-required.typ dev/night/out/C2-empty-required.pdf`。

### C3 五级标题与四级采用相同编号形式

- 入口与场景：硕士四级标题下面继续写五级标题。
- 现象：四级甲和五级子项均显示为 `（1）`，字号均12pt；最小复现编号起点分别约79.039和85.039bp，没有明确的第五级样式或错误提示。目录仍只列三级。
- 对应规格与空白：`docs/格式规格.md` §2.2、§2.4、§2.5定义到四级，原文“四级标题用（1）形式，不进目录”；没有第五级排版/是否应拒绝的规定。
- 判断：C；不是声称目录深度违规，而是更深层级的可辨识性与支持范围未定义。
- 最小复现：`dev/night/repro/C3-five-level-heading.typ`。
- 复现命令：`typst compile --root . dev/night/repro/C3-five-level-heading.typ dev/night/out/C3-five-level-heading.pdf`。

### C4 标题脚注在目录和正文重复生成

- 入口与场景：研究生章标题带一个 `footnote`，并生成目录。
- 现象：源文件只有一次“唯一的标题说明”，最小复现的PDF在物理第1页目录、第3页正文各出现一次脚注正文，分别以1和3标记；章标题被页眉复用时还参与脚注计数。
- 对应规格与空白：`docs/格式规格.md` §2.3、§2.4要求页眉复用章名、目录收录标题，但未规定脚注在标题、目录和页眉中的保留/抑制规则。
- 判断：C；需先确定只在正文出注，还是禁止标题脚注，不能用普通目录文字比对证明此场景已正确。
- 最小复现：`dev/night/repro/C4-heading-footnote.typ`。
- 复现命令：`typst compile --root . dev/night/repro/C4-heading-footnote.typ dev/night/out/C4-heading-footnote.pdf`。

## 官方要求核查

2026-11-02使用curl访问15个官方HTML页面，全部成功；收集指定4份文档中的官方来源链接，另查看研究生院资料目录及本科生院首页相关通知。未下载附件，也未修改规格。页面初始发布日期与附件更新版本分列判断，避免把2016/2019年的页面发布日期误当附件版本。

| 来源 | 仓库记录版本 | 官网当前版本 / 日期 | 是否更新 |
|---|---|---|---|
| [学术硕士资料](https://gr.xidian.edu.cn/info/1047/5087.htm) | Word 2025.01；LaTeX 2024.04 | 页面2016-03-21；附件名仍为2025.01、2024.04 | 未发现附件名版本更新 |
| [专业硕士资料](https://gr.xidian.edu.cn/info/1047/5086.htm) | 专硕独立封面2022.11；资料包2025.01 | 页面2016-03-21；当前资料包名2025.01 | 外层版本未更新；未解包复核内部2022.11封面 |
| [学术博士资料](https://gr.xidian.edu.cn/info/1047/7160.htm) | 2025.01资料包 | 页面2019-02-24；附件“2025年1月更新” | 未发现附件名版本更新 |
| [专业博士资料](https://gr.xidian.edu.cn/info/1047/7803.htm) | 2026.09资料包，内部2026.5前置页 | 页面2019-07-02；附件仍为2026.09 | 外层版本未更新；未解包复核内部2026.5 |
| [研究生院资料目录](https://gr.xidian.edu.cn/xwsy/zlxz.htm) | 同上四类入口 | 当前目录仍指向上述四页，提醒区分学位论文与毕业论文模板 | 未发现更高版本入口 |
| [本科全套表格](https://jwc.xidian.edu.cn/info/1022/12943.htm) | 同一下载页，配套材料规格未写明包版本；本科论文格式以2019手册为据 | 页标题明确“2025版”；页面日期2023-10-19，正文“更新于2025年10月9日” | 官网有明确的较新版本标识；不能仅凭标识断言2019论文格式已改变 |
| [2023级本科毕业设计工作通知](https://jwc.xidian.edu.cn/info/1012/23423.htm) | 导航未记录此通知 | **2026-09-29**，附“毕业设计表格—全套.zip” | **有较新通知和表格发布入口**；附件内容是否变化未核验 |
| [2022级工作通知](https://jwc.xidian.edu.cn/info/1025/20353.htm) / [2026盲审通知](https://jwc.xidian.edu.cn/info/1025/22113.htm) | 未逐条记录 | 2025-10-09 / 2026-04-27，均附表格包 | 补充发布证据；不等同新增格式规范 |

官方检索限公开页面，未声称逐个学院、所有历史分页或附件正文均已排除更新。详细URL、附件链接文字和日期片段保存在 `dev/night/official-results.json`。

## 覆盖情况

“检查失败”分别列**现有脚本非零退出的文档数 / 通用检查候选文档数**，不等于A/B/C问题数量；输入错与检查尺固定示例假设均另外复核。每个配置34份：首轮30类，第二轮长题目/长索引变体，第三轮长摘要/长表变体。

| 入口配置 | 场景文档数 | 编译失败 | 检查失败（现有 / 通用） |
|---|---:|---:|---:|
{chr(10).join(coverage)}

- 总计 **680份**，成功输出 **{len(passed)}份PDF、{pages}页**。34次编译失败包含博士按规格拒绝超宽输入14次，以及显式 `none` 题目的20次无效输入；没有将它们全部计作模板A类。
- 7类通用检查逐PDF执行：按stride读取栅格墨迹；分版式的页眉/页码、罗马到阿拉伯切换；未解析/空引用；图表公式的章前缀和序列；目录内部链接的文字与目的页码；正文连续基线；编号区空白填充页。本科正文按23.4pt实现的1.5倍口径，研究生/行政表按20pt；前置页、表格行内边距、公式高度不能混作普通正文行距。
- 通用检查15个故障注入样本全部检出，正常多页、正确目录和表格内边距对照均通过，含第二页缺陷、缺章前缀、跳号、错误目录文字/页码、本科行距错误。脚注/公式附近的连续普通正文行亦进入检查；不声称含复杂公式的行盒或表格行高也应恒为20pt。
- 对140份长内容样本额外记录实际条目数：长表150/160行均完整；70图和70表均可提取；研究生符号/缩略语表140/143条均完整；300条文献标签1～300均存在。中英期刊、会议、学位论文、专利、标准、网页、书籍章节均经过真实cite。此项记录内容存在性，不是对所有文献著录细节逐条作国家标准全文验收。
- 另以输入中实际虚构姓名、导师名、学号及PDF Author元数据复核126份成功的盲审PDF，零泄漏；专门注入文字/元数据泄漏的负向样本能检出。没有用现有尺里固定的“张三”代替本轮身份字段。
- 20章、单章、四/五级标题、公式/脚注标题、并排子图、代码/脚注/嵌套列表、多附录及附录内图表公式、多页致谢/简介/成果、盲审开关均已生成并实际编译。长题目、表格字号、多行公式、空字段等另做最小复现和PNG复核，未对全部PDF逐页肉眼审读。
- 本科没有盲审、图/表索引、符号/缩略语对照表或作者简介的独立API；对应场景不构成这些页面的验收，长后置场景只测试其致谢，不能声称本科有作者简介。本科附录字母编号按《本科规格》单独检查并做正/负向验证。行政表和课程报告没有独立英文题目页、论文摘要/关键词页、图表目录、作者简介、附录API，也没有盲审参数；相关富内容放入其现有body字段，测试其流式分页，不声称提供这些论文页面。课程报告没有校级统一模板。
- **总回归 `bash dev/check-all.sh`：38项通过，0失败**；真实硕士112页、本科55页压力测试通过，默认init产物2个文件、33页。不可把退出码0理解成全部外部基准均已校验。
- 本地外部基准缺失/跳过：{'; '.join(skips)}。原始博士Word路径也未提供，专用前置页未进行本次原始Word锚点再自检。未下载附件补入仓库。
- 已知局限/保留差异未计为新问题：逐行y不可与官方逐行对应、附录缺官方实测、本科标识占位、README已裁定页眉/页码等差异。正文和目录自动抽取不能覆盖任意用户自定义show规则、外部图片、特殊字体或所有富内容组合。

## 统计

- 批量场景文档：**680份**；最小复现：**13份.typ**及1份.bib；无PDF提交。
- 三轮最终批量运行耗时：{sum(r['elapsed'] for r in rounds):.2f}秒；从任务启动至本次报告生成约 **{elapsed//60}分{elapsed%60}秒**，包含读规格、校准、重跑、复核和总回归。前期校准的重复编译不计作新的场景文档。
- 三轮新增A/B/C问题数：9、0、0；已覆盖全部矩阵，满足连续两轮无新问题的停止条件。
- D类（检查脚本误报）修正：**4次**。保留原始现有验收尺退出码，不改现有脚本；固定内容/页码的差异不直接计入A/B/C。修正及重跑记录见 `dev/night/triage.json`。
- 源文件SHA256与最终编译记录逐一一致：**{matched}**；结果与现有尺失败文本见 `results-r01.json`～`results-r03.json`，复现坐标见 `repro-results.json`。
- 包软链：最终在主仓库目录执行 `bash dev/pkg-stage.sh`，全局 `preview/modern-xdu-thesis/0.3.1` 已指回主仓库；本次批量测试全程使用 `out/packages` 的进程局部路径。主工作区git状态干净。
- 本地分支：`night/stress-20261102`；worktree：`{ROOT}`。写入范围仅 `dev/night/`（另有用户指定的本机路径配置复制与仓库外报告）；未修改模板、规格、现有脚本、元数据，未引入字体或preview依赖，未push、开PR或发布。
'''
    REPORT.parent.mkdir(parents=True,exist_ok=True);REPORT.write_text(body)
    summary=dict(report=str(REPORT),base=base,documents=len(cases),pdfs=len(passed),pages=pages,compile_fail=sum(c['compile_rc']!=0 for c in cases),legacy_failed_documents=sum(any(x['rc'] for x in c['legacy']) for c in cases),general_failed_documents=sum(bool((c.get('general') or {}).get('issues')) for c in cases),negative_tests=16,blind_pdfs=len(blind['cases']),global_package_target=str(package_link.resolve()),findings=dict(A=4,B=1,C=4),source_hashes_match=matched,check_all=dict(passed=38,failed=0,skips=skips),elapsed_seconds=elapsed)
    (HERE/'summary.json').write_text(json.dumps(summary,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps(summary,ensure_ascii=False,indent=2))
if __name__=='__main__':main()
