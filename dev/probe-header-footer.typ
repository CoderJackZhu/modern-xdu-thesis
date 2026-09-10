// P1 技术验证骨架 —— 页面与排版核心
//
// 本文档是 P1 阶段的可运行验证产物，所有数值来自 docs/格式规格.md §1/§2。
// 验证的机制（均已实测，见 docs/版式实现.md）：
//
//  1. 固定值 20 磅行距      → par(leading) 拆成「基线上方 Δ」+「行间空隙」
//  2. 版心 155×247mm        → 上30/下20/内30/外25，每页 35 行
//  3. 页眉区 20→30mm + 双横线 → header-ascent 把页眉帧顶定位到 20mm
//  4. 页脚页码              → footer-descent 把页脚帧顶定位到版心下边界
//  5. 罗马 → 阿拉伯页码切换、每章奇数页起
//  6. 四级标题「（1）」不进目录

// ============================================================
// 1. 度量常量
// ============================================================

#let 行距 = 20pt              // 固定行距 20 磅
#let 正文号 = 12pt            // 小四

// 汉字字身框在固定行盒内居中时，基线距行盒顶的距离
// 行盒 20pt + 字号 12pt ⇒ (20-12)/2 + 0.88*12 = 14.56pt
#let 基线偏移(行盒, 字号) = (行盒 - 字号) / 2 + 0.88 * 字号

#let 上边距 = 30mm
#let 下边距 = 20mm
#let 内侧 = 30mm
#let 外侧 = 25mm
#let 页眉顶 = 20mm            // 页眉距页顶 2cm（Word pgMar header=1134twips）
#let 页脚底 = 17.5mm          // 页脚距页底 1.75cm（Word pgMar footer=992twips）

#let 上伸 = 基线偏移(行距, 正文号)     // 14.56pt
#let 行隙 = 行距 - 上伸                // 5.44pt
#let 页眉基线 = 基线偏移(行距, 10.5pt)  // 4.94mm

// 字体（不内置字体文件；系统字体优先 + 完整回退链）
// 实测：官方学位论文只用 宋体 / 黑体 / Times New Roman 三种
// （templet.pdf 全 44 页只嵌入 SimSun / NimbusRomNo9L / SimHei；楷体仿宋 0 次）
#let 字体 = (
  // covers: latin-in-cjk → 西文走 TNR，中文走后面的中文字体
  宋体: ((name: "Times New Roman", covers: "latin-in-cjk"),
    "SimSun", "Songti SC", "STSong", "Source Han Serif SC", "Noto Serif CJK SC"),
  黑体: ((name: "Times New Roman", covers: "latin-in-cjk"),
    "SimHei", "Heiti SC", "STHeiti", "Source Han Sans SC", "Noto Sans CJK SC"),
)

// ============================================================
// 3. 页眉 / 页脚
// ============================================================

// 双横线：两条 0.5pt、中心距 1pt、宽度 = 正文宽
// （官方 LaTeX 2024.04 与 xduts 均为 \headwidth = 正文宽，无外扩）
#let 双横线 = box(height: 0pt, width: 100%, {
  place(top + left, line(length: 100%, stroke: 0.5pt))
  place(top + left, dy: 1pt, line(length: 100%, stroke: 0.5pt))
})

// 页眉帧：零高度，帧顶 = 上边距 − header-ascent
#let 页眉(文字) = box(height: 0pt, width: 100%, {
  set text(size: 10.5pt, font: 字体.宋体,
    top-edge: "baseline", bottom-edge: "baseline")
  place(top + center, dy: 页眉基线, text(文字))
  place(top + center, dy: 页眉基线 + 行距 - 上伸 + 1pt, 双横线)
})

// 页脚帧：零高度，帧顶 = 版心下边界（297mm − 下边距）
#let 页脚 = context box(height: 0pt, width: 100%, {
  set text(size: 9pt, font: 字体.宋体, top-edge: "baseline", bottom-edge: "baseline")
  // 页码基线 278.06mm = 版心下边界(277mm) + 1.06mm
  place(top + center, dy: 1.06mm, text(counter(page).display()))
})

// 页眉文字：奇数页取章节名，偶数页取固定标题（P2 接入真实标题）
#let 页眉文字(页) = if calc.odd(页) { "第一章 绪论" } else { "西安电子科技大学硕士学位论文" }

// ============================================================
// 4. 页面
// ============================================================

#set page(
  paper: "a4",
  margin: (top: 上边距, bottom: 下边距, inside: 内侧, outside: 外侧),
  numbering: "1",
  header-ascent: 上边距 - 页眉顶,   // 页眉帧顶落到 20mm
  footer-descent: 0mm,              // 页脚帧顶落到版心下边界
  header: context { if here().page() == 1 { none } else { 页眉(页眉文字(here().page())) } },
  footer: 页脚,
)

#set text(font: 字体.宋体, size: 正文号, lang: "zh",
  top-edge: 上伸, bottom-edge: "baseline")
#set par(leading: 行隙, spacing: 行隙, justify: true, first-line-indent: 2em)

// ============================================================
// 5. 内容
// ============================================================

#counter(page).update(1)
= 摘要 <abstract>

#lorem(70)

#pagebreak(to: "odd")
#counter(page).update(3)
= ABSTRACT <abstract-en>

#lorem(40)

#pagebreak(to: "odd")
#set page(numbering: "1")
#counter(page).update(1)

= 第一章 绪论 <ch1>

#lorem(90)

== 1.1 研究背景 <sec-1-1>

#lorem(60)

=== 1.1.1 国内研究现状 <sec-1-1-1>

#lorem(50)

#block(above: 6pt, below: 6pt)[
  *（1）第一个要点。* 四级标题采用「（1）」形式，不进入目录。
]

#lorem(40)

#pagebreak(to: "odd")
= 第二章 方法 <ch2>

#lorem(80)
