// 测试：参考文献走 .bib + GB/T 7714-2015（Typst 内置 CSL 样式）
#import "../lib.typ": documentclass

#let (doc, mainmatter, references, 引用) = documentclass(
  degree: "academic",
  info: (
    title: ("参考文献 .bib 测试",),
    author: "张三",
    discipline: "电子科学与技术", supervisor: ("李四", "教授"),
    department: "电子工程学院", submit-date: (year: 2025, month: 6),
    school-code: "10701", clc: "TN82", student-id: "21011201234", secret-level: "公开",
  ),
)
#show: doc

// 正文里的引用：走 .bib 模式时必须用 #cite(<key>)，否则 bibliography() 不收录条目
#show: mainmatter.with(header-title: "西安电子科技大学硕士学位论文")

正文引用示例：#cite(<gb1>)、#cite(<gb3>)、#cite(<gb4>)、#cite(<en4>)。

#pagebreak(to: "odd")
#references(bib: "/dev/refs-demo.bib")
