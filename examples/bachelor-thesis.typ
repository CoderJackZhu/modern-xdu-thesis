// 西安电子科技大学本科毕业设计（论文）完整示例
#import "@preview/modern-xdu-thesis:0.1.0": bachelor

#let (doc, cover, abstract, abstract-en, outline-page, mainmatter,
  appendix, acknowledgement, references, 引用) = bachelor.documentclass(
  info: (
    title: ("基于视频的人体动作识别", "算法研究"),
    author: "张三",
    department: "人工智能学院",
    major: "智能科学与技术",
    supervisor: ("李四", "王五"),
    class-id: "2101011",
    student-id: "21010100001",
    abstract: [
      基于视频的人体动作识别是人工智能领域的重要研究课题，其目的在于设计智能算法预测视频中
      发生的人体动作类别，使计算机能够理解人的行为。本文围绕动作识别模型展开研究，分析模型
      的基本原理、实现方法和实验结果，并总结后续可以改进的方向。本段用于演示本科模板的摘要
      版式，实际使用时应替换为不少于三百字的真实摘要内容。
    ],
    abstract-en: [
      Video-based human action recognition is an important research topic in artificial
      intelligence. Replace this sample with the complete English abstract when writing
      the thesis.
    ],
    keywords: ("动作识别", "三维卷积神经网络", "注意力机制"),
    keywords-en: ("action recognition", "3D convolution", "attention mechanism"),
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

== 研究目的及意义

目前我们处于信息快速增长的时代，视频已经成为重要的信息载体。人体动作识别是视频理解的
基础任务，在智能安防、人机交互和智能家居等领域具有应用价值。

=== 国内外研究现状

传统方法依赖手工特征，深度学习方法可以自动学习视频中的时空表示#引用(1)。

= 方法与实验

本章介绍模型结构和实验配置。

== 模型结构

#figure(rect(width: 55mm, height: 25mm), caption: [动作识别模型结构]) <fig:model>

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
