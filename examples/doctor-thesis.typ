// 博士完整示例；编译参数示例：--input degree=professional --input blind=true。
#import "@preview/modern-xdu-thesis:0.3.1": doctor-documentclass

#let 专业 = sys.inputs.at("degree", default: "academic") == "professional"
#let 匿名 = sys.inputs.at("blind", default: "false") == "true"
#let 企业导师 = sys.inputs.at("enterprise", default: "true") == "true"
#let (doc, cover, title-cn, title-en, declaration, abstract, abstract-en,
  list-of-figures, list-of-tables, notation, abbreviations, outline-page,
  mainmatter, appendix, references, acknowledgement, bio) = doctor-documentclass(
  degree: if 专业 { "professional" } else { "academic" },
  blind: 匿名,
  info: (
    title: ("复杂系统的可靠建模", "与验证方法研究"),
    title-en: ("Reliable Modeling and Verification", "of Complex Systems"),
    author: "张三",
    author-en: "Zhang San",
    student-id: "20261029001",
    department: "电子工程学院",
    discipline: "电子科学与技术",
    discipline-en: "Electronic Science and Technology",
    subdiscipline: "电路与系统",
    domain: "电子信息",
    category-en: "Electronic Information",
    supervisor: ("李四", "教授"),
    supervisor-en: ("Li Si", "Professor"),
    enterprise-supervisor: if 专业 and 企业导师 { ("王五", "高级工程师") } else { (none, none) },
    enterprise-supervisor-en: if 专业 and 企业导师 { ("Wang Wu", "Senior Engineer") } else { (none, none) },
    submit-date: (year: 2026, month: 10),
    abstract: [
      本文围绕复杂系统的可靠建模与验证开展研究。本示例展示博士论文的排版结构，
      其中全部作者、导师和研究内容均为虚构。正式论文中文摘要约一千五百字，
      应陈述研究目的、方法、成果和结论，重点突出创新贡献。
    ],
    abstract-en: [
      This example demonstrates the structure of a doctoral dissertation. All names
      and research content are fictional. Replace this paragraph with the English
      abstract corresponding to the complete Chinese abstract.
    ],
    keywords: ("复杂系统", "可靠建模", "形式化验证"),
    keywords-en: ("complex systems", "reliable modeling", "formal verification"),
    acknowledgement: [感谢导师和同学在研究期间给予的指导和帮助。],
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
#abstract-en()
#pagebreak(to: "odd")
#list-of-figures()
#pagebreak(to: "odd")
#list-of-tables()
#pagebreak(to: "odd")
#notation()
#pagebreak(to: "odd")
#abbreviations()
#pagebreak(to: "odd")
#outline-page()

#show: mainmatter

= 第一章 绪论

复杂系统在电子信息领域具有广泛应用。可靠建模需要明确假设、定义边界，并使用可以复核的
实验或证明验证结论。正文采用研究生论文固定二十磅行距，首行缩进两个汉字。

#for i in range(3) [
  本段用于演示连续正文的行距与分页。研究应清楚说明问题、方法和结果，使独立读者能够
  理解模型的适用范围，并在同样的条件下重复实验。论文中的图表、公式和参考文献均应与
  正文建立明确联系。

]

#pagebreak()
本页用于检查偶数页固定博士页眉。正文页码应连续，正文部分从阿拉伯数字一开始。

= 第二章 方法与实验

#figure(rect(width: 50mm, height: 20mm), caption: [系统模型]) <fig:model>
#figure(table(columns: 2, [方法], [指标], [示例模型], [0.95]), caption: [实验结果]) <tab:result>
$ y = a x + b $ <eq:model>

图 @fig:model、表 @tab:result 和式 @eq:model 按章编号。引文示例#cite(<example>)。

#appendix(title: "补充材料", body: [这里填写补充实验与推导。])
#pagebreak(to: "odd")
#references(body: bibliography("doctor-ref.bib", style: "gb-7714-2015-numeric", title: none))
#pagebreak(to: "odd")
#acknowledgement()
#pagebreak(to: "odd")
#bio()
