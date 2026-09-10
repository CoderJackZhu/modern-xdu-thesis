// 测试：渲染 P3 五个索引类页面（专业学位字段）
#import "../lib.typ": documentclass

#let (
  doc, cover, title-cn, title-en, declaration, abstract, abstract-en,
  list-of-figures, list-of-tables, notation, abbreviations, outline-page,
) = documentclass(
  degree: "professional",
  info: (
    title: ("基于深度学习的毫米波大规模 MIMO", "信道估计研究"),
    title-en: ("Deep Learning based Channel Estimation", "for mmWave Massive MIMO Systems"),
    author: "张三", author-en: "Zhang San",
    discipline: "电子科学与技术",
    discipline-en: "Electronic Science and Technology",
    domain: "人工智能", domain-en: "Artificial Intelligence",
    degree-name: "电子信息硕士",
    supervisor: ("李四", "教授"), supervisor-en: ("Li Si", "Professor"),
    enterprise-supervisor: ("王五", "高级工程师"),
    enterprise-supervisor-en: ("Wang Wu", "Senior Engineer"),
    department: "电子工程学院", submit-date: (year: 2025, month: 6),
    school-code: "10701", clc: "TN82", student-id: "21011201234", secret-level: "公开",
    abstract: [摘要是学位论文内容不加注释和评论的简短陈述。],
    abstract-en: [The Abstract is a brief description of the content.],
    keywords: ("深度学习", "毫米波"), keywords-en: ("deep learning", "millimeter wave"),
    notation: (("α", "衰减系数"), ("λ", "波长"), ("f", "频率"), ("T", "周期")),
    abbreviations: (("MIMO", "Multiple-Input Multiple-Output", "多输入多输出"),
      ("OFDM", "Orthogonal Frequency Division Multiplexing", "正交频分复用"),
      ("SNR", "Signal-to-Noise Ratio", "信噪比")),
  ),
)
#show: doc

#counter(page).update(1)
#list-of-figures()

#pagebreak(to: "odd")
#counter(page).update(3)
#list-of-tables()

#pagebreak(to: "odd")
#counter(page).update(5)
#notation()

#pagebreak(to: "odd")
#counter(page).update(7)
#abbreviations()

#pagebreak(to: "odd")
#counter(page).update(9)
// 先造几个 heading 供目录收录（P4 的正文会自然提供）
= 第一章 绪论
== 1.1 研究背景
=== 1.1.1 国内研究现状

#figure(rect(width: 4cm, height: 2cm), caption: [系统框图])
#figure(rect(width: 4cm, height: 2cm), caption: [信道模型])
#figure(table(columns: 2, [参数], [取值]), caption: [仿真参数])

= 第二章 方法
#pagebreak(to: "odd")
#outline-page()
