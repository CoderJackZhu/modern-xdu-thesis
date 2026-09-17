// 西安电子科技大学本科毕业设计（论文）完整示例
#import "@preview/modern-xdu-thesis:0.1.0": bachelor

#let (doc, cover, abstract, abstract-en, outline-page, mainmatter,
  appendix, acknowledgement, references, 引用) = bachelor.documentclass(
  // 官方标识不随包分发。下载并放入项目的 assets/ 后，取消下面两行注释：
  // cover-wordmark: path("assets/xdu-wordmark.jpeg"),
  // cover-emblem: path("assets/xdu-emblem.png"),
  info: (
    title: ("基于深度学习的城市交通流量预测", "方法研究"),
    author: "张三",
    department: "电子工程学院",
    major: "电子信息工程",
    supervisor: ("李四", "王五"),
    class-id: "2101011",
    student-id: "21010100001",
    abstract: [
      城市交通流量预测是智能交通系统的基础问题之一，其目标是依据历史观测数据推断未来一段时间
      内的路段流量，为信号配时、出行诱导和路网调度提供依据。本文以某城市的线圈检测数据为对象，
      构建了融合时间卷积与注意力机制的预测模型，并通过对比实验分析了不同输入窗口和损失函数
      对预测精度的影响。本文用于演示本科模板的摘要版式，实际使用时应替换为不少于三百字的
      真实摘要内容。
    ],
    abstract-en: [
      Urban traffic flow prediction is a fundamental problem in intelligent transportation
      systems. Replace this sample with the complete English abstract when writing the
      thesis.
    ],
    keywords: ("交通流量预测", "时空序列建模", "注意力机制"),
    keywords-en: ("traffic flow prediction", "spatio-temporal modeling", "attention mechanism"),
    acknowledgement: [感谢导师在本科毕业设计期间给予的指导和帮助。],
  ),
)

#show: doc

#cover()
#pagebreak(to: "odd")
#counter(page).update(1)
#abstract()
#pagebreak(to: "odd")
#abstract-en()
#pagebreak(to: "odd")
#outline-page()

#show: mainmatter

= 引言

== 研究背景与意义

城市路网的通行状态受通勤、天气与节假日等因素影响，具有明显的周期性与突发性。交通流量
预测是智能交通系统的基础任务，在信号配时、出行诱导和路网调度等场景中具有应用价值。

=== 国内外研究现状

早期方法多依赖时间序列模型或统计学习模型，难以刻画路网的空间相关性；近年基于深度学习的
方法可以同时学习时间依赖与空间结构#引用(1)。

= 方法与实验

本章介绍模型结构和实验配置。

== 模型结构

#figure(rect(width: 55mm, height: 25mm), caption: [交通流量预测模型结构]) <fig:model>

#figure(table(columns: 2, [参数], [取值], [学习率], [0.001]), caption: [实验参数]) <tab:params>

$ bold(y) = bold(W) bold(x) + bold(b) $ <eq:model>

图 @fig:model、表 @tab:params 和式 @eq:model 均按章编号。

#appendix(title: "补充实验", body: [
  附录中的图、表和公式与正文分开编号。

  #figure(rect(width: 45mm, height: 20mm), caption: [附录实验结果]) <fig:appendix>

  $ y = a x + b $ <eq:appendix>
])

#pagebreak(to: "odd")
#acknowledgement()

#pagebreak(to: "odd")
#references(entries: (
  "作者. 本科毕业设计参考文献示例[J]. 示例期刊, 2025, 1(1): 1-8.",
  "AUTHOR A. An undergraduate thesis reference example[J]. Journal, 2024, 2(1): 9-16.",
))
