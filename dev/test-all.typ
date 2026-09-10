// 测试：渲染 6 个前置页面（专业学位字段）
#import "../lib.typ": documentclass

#let (cover, title-cn, title-en, declaration, abstract, abstract-en, doc) = documentclass(
  degree: "professional",
  info: (
    title: ("基于深度学习的毫米波大规模 MIMO", "信道估计研究"),
    title-en: ("Deep Learning based Channel Estimation", "for mmWave Massive MIMO Systems"),
    author: "张三",
    author-en: "Zhang San",
    discipline: "电子科学与技术",
    subdiscipline: "电磁场与微波技术",
    domain: "人工智能",
    degree-name: "电子信息硕士",
    degree-name-en: "Master of Electronic Information",
    supervisor: ("李四", "教授"),
    supervisor-en: ("Li Si", "Professor"),
    enterprise-supervisor: ("王五", "高级工程师"),
    enterprise-supervisor-en: ("Wang Wu", "Senior Engineer"),
    school-code: "10701",
    clc: "TN82",
    student-id: "21011201234",
    secret-level: "公开",
    submit-date: (year: 2025, month: 6),
    keywords: ("深度学习", "毫米波", "大规模 MIMO", "信道估计"),
    keywords-en: ("deep learning", "millimeter wave", "massive MIMO", "channel estimation"),
    abstract: [摘要是学位论文内容不加注释和评论的简短陈述，应简明扼要地陈述研究的目的、内容、方法、成果和结论，重点突出学位论文的创造性成果。硕士学位论文中文摘要字数一般为 1000 字左右，博士学位论文中文摘要字数一般为 1500 字左右。英文摘要内容与中文摘要内容保持一致，翻译力求简明精准。摘要正文下方需注明论文的关键词，关键词一般 3 到 8 个，关键词之间用逗号并空一格。],
    abstract-en: [The Abstract is a brief description of the content of the dissertation without notes or comments. It represents concisely the research purpose, content, method, results and conclusion of the thesis or dissertation, with emphasis on the creative achievements. The Abstract consists of both the Chinese and English versions. The Chinese abstract should have the length of approximately 1000 characters for a Master's thesis, and 1500 for a Ph.D. dissertation. The English abstract should be consistent with the Chinese one in content. The keywords of the abstract are placed below the body of the abstract, separated by commas, typically 3 to 5.],
  ),
)
#show: doc

#cover()

#pagebreak(to: "odd")
#title-cn()

#pagebreak(to: "odd")
#title-en()

#pagebreak(to: "odd")
#declaration()

#pagebreak(to: "odd")
#counter(page).update(1)
#abstract()

#pagebreak(to: "odd")
#counter(page).update(3)
#abstract-en()
