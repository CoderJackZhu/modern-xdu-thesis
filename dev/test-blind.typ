// 测试：盲审模式（封面/题名页隐去姓名、致谢删除正文、作者简介保留成果排序）
#import "../lib.typ": documentclass

#let (
  doc, cover, title-cn, title-en, declaration, abstract, abstract-en,
  list-of-figures, list-of-tables, notation, abbreviations, outline-page,
  mainmatter, references, acknowledgement, bio, 引用,
) = documentclass(
  degree: "professional",
  blind: true,                       // ← 盲审模式
  info: (
    title: ("基于深度学习的毫米波大规模 MIMO", "信道估计研究"),
    title-en: ("Deep Learning based Channel Estimation", "for mmWave Massive MIMO Systems"),
    author: "张三", author-en: "Zhang San",
    discipline: "电子科学与技术", discipline-en: "Electronic Science and Technology",
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
    notation: (("α", "路径损耗指数"),),
    abbreviations: (("MIMO", "Multiple-Input Multiple-Output", "多输入多输出"),),
    acknowledgement: [这里是一段很长的致谢文字，盲审模式下不应该出现。],
    references: ("张三, 李四. 论文题目[J]. 期刊名, 2025, 12(3): 45-52.",),
    bio: (
      ("基本情况", "张三，男，陕西西安人，西安电子科技大学 XX 学院 XX 专业 2008 级硕士研究生。"),
      ("攻读硕士学位期间的研究成果", "1. 发表学术论文（第一作者）：张三, 王六. 论文题目[J]. 期刊名, 2025."),
    ),
  ),
)
#show: doc

#cover()
#pagebreak(to: "odd")
#title-cn()
#pagebreak(to: "odd")
#title-en()
#pagebreak(to: "odd")
#abstract()
#pagebreak(to: "odd")
#acknowledgement()
#pagebreak(to: "odd")
#bio()
