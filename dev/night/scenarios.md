# 虚构用户写法压测矩阵

基准：origin/main（建立 worktree 时锁定提交，见 results.json）。所有输入、日志和代码只写 dev/night；PDF 与临时包解析目录写忽略的 out/。禁止修改模板、现有验收尺、规格或全局包软链。

## 入口

| 入口 | 参数组合 |
|---|---|
| bachelor.typ | 本科论文；无盲审参数，不虚构该能力 |
| lib.typ | 硕士 academic / professional × blind false / true |
| doctor.typ | 博士 academic / professional × blind false / true |
| supporting/proposal.typ | master / doctor × academic / professional |
| supporting/interim.typ | master / doctor × academic / professional |
| supporting/bachelor-forms.typ | 本科开题 / 本科中期 |
| supporting/course-report.typ | 课程实验报告 |

合计 20 个配置。论文有独立中英文摘要、关键词、图表索引及后置页；行政表没有这些 API，相关内容写进其真实 body 字段，以检验富内容/分页，报告明确区分“不提供独立页面”。

## 每个配置的场景

1. baseline：短字段、单章、图表公式引用的正向基线。
2. long_titles：超长中英文题目（单字符串需自动折行；博士的显式分行限制按规格判断）。
3. long_fields：长姓名、导师、学院、专业/学科，观察溢出与覆盖。
4. multiple_supervisors：本科多人，研究生姓名/职称二元组中多姓名，行政表多人字符串。
5. optional_empty：企业导师、可选学科/单位信息空值。
6. required_empty：标题/作者/学号空字符串，核查提示或静默遗漏。
7. required_none：标题/作者空值，核查错误是否定位字段。
8. mixed：中英混排、全半角标点。
9. long_abstract：中英文摘要均超过一页。
10. many_keywords：60 个关键词。
11. abstract_math：英文摘要包含公式、特殊字符与数学符号。
12. heading4：四级标题及多条括号编号。
13. heading5：五级标题。
14. one_chapter：仅一章。
15. twenty_chapters：二十章。
16. long_chapter：长章名与页眉。
17. heading_math：标题内公式。
18. heading_footnote：标题内脚注。
19. many_figures：70 张图、70 张表，图表索引跨页。
20. long_table：可分割 block 中 150 行 table（真实跨页长表）。
21. sub_parallel：两张并排子图与总图题。
22. equations：多条编号公式、交叉引用与多行对齐公式。
23. code_notes_lists：代码块、脚注、嵌套列表及相邻正文行距。
24. long_indexes：各 140 行符号与缩略语表。
25. bib0：0 条参考文献。
26. bib1：1 条参考文献。
27. bib300：300 条真实 cite 的 BibTeX 参考文献。
28. bib_types：中英期刊、会议、学位论文、专利、标准、网页、书籍章节；多作者“等”/“et al.”。
29. appendices：三个附录，各含图表、公式与引用。
30. long_back：多页致谢、作者简介和成果列表。

## 轮次与判定

首轮全矩阵 600 份；后续每轮至少 40 份，变化文本长度/数量，轮换场景。发现新 A/B/C 后连续无新问题轮数归零；全部场景完成且连续两轮无新问题才停止。编译错误的输入先排除生成器写法错误，模板明确拒绝的合法限制不算 A。

现有验收尺逐 PDF 调用，保留原始退出码及输出。固定示例假设（物理页码、固定姓名、短字段坐标）对动态输入不适用时记作 D 候选，由通用检查和最小复现复核，绝不把验收尺退出码直接等同模板缺陷。

通用检查：栅格墨迹边界（stride）、页眉/页码与切换、未解析引用、章前缀编号连续、目录文字/目的页、正文固定行距与空白填充页；每项先做正负向故障注入，覆盖后续页。额外记录文本完整性与盲审身份信息，已知内容块不自动匿名不算新问题。

已知边界不计新问题：逐行 y 无法对齐官方、附录缺官方实测、本科封面标识占位、README 已保留差异。课程报告无校级统一规范；行政表无页眉页码是预期行为。
