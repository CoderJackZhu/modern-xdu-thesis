// P1-2 验证：页眉双横线 / 页码（前置罗马 → 正文阿拉伯）/ 每章奇数页起 / 四级标题不进目录
// 参照：docs/格式规格.md §2.3 页眉页脚、§2.4 结构顺序、§4.3 技术点 3~6

#let 行距 = 20pt
#let 上伸 = (行距 - 12pt) / 2 + 0.88 * 12pt
#let 行隙 = 行距 - 上伸

// 页眉：五号居中 + 双横线（各 0.5pt，中心距 1pt，宽度=正文宽）
#let 页眉(文字) = {
  set text(size: 10.5pt, font: ("Times New Roman", "Songti SC"),
    top-edge: "baseline", bottom-edge: "baseline")
  align(center, text(文字))
  v(1pt)
  line(length: 100%, stroke: 0.5pt)
  v(0.5pt)
  line(length: 100%, stroke: 0.5pt)
}

#set page(
  paper: "a4",
  margin: (top: 30mm, bottom: 20mm, inside: 30mm, outside: 25mm),
  numbering: "I",
  header: context {
    if here().page() == 1 { none } else if calc.odd(here().page()) {
      页眉("第一章 绪论")
    } else {
      页眉("西安电子科技大学硕士学位论文")
    }
  },
  footer: context {
    set text(size: 9pt, font: ("Times New Roman", "Songti SC"))
    align(center, counter(page).display())
  },
)

#set text(font: ("Times New Roman", "Songti SC"), size: 12pt, lang: "zh")

// ---- 前置部分（罗马数字）----
#counter(page).update(1)
= 摘要 <pre>

#set text(top-edge: 上伸, bottom-edge: "baseline")
#set par(leading: 行隙, spacing: 行隙, justify: true, first-line-indent: 2em)
#lorem(60)

#pagebreak(to: "odd")
#counter(page).update(3)
= ABSTRACT <abs-en>

#lorem(30)

// ---- 正文（阿拉伯数字，重新从 1 开始）----
#pagebreak(to: "odd")
#set page(numbering: "1")
#counter(page).update(1)
#show heading.where(level: 1): it => block(above: 24pt, below: 18pt)[
  #set align(center)
  #set text(size: 16pt, font: ("Times New Roman", "SimHei", "Heiti SC", "STHeiti"), weight: "regular")
  #it.body
]

= 第一章 绪论 <ch1>

#set par(first-line-indent: 2em)
#lorem(80)

== 1.1 研究背景 <sec11>

#lorem(50)

=== 1.1.1 国内现状 <sec111>

#lorem(40)

// 四级标题用「（1）」形式，不进目录
#block(above: 6pt, below: 6pt)[*（1）第一个要点。* 这是四级标题的写法，采用「（1）」形式，不进入目录。]

#lorem(30)

#pagebreak(to: "odd")
= 第二章 方法 <ch2>

#lorem(60)

// ---- 目录 ----
#pagebreak(to: "odd")
#set page(numbering: "I")
#counter(page).update(1)
#outline(title: [目录], depth: 3)
