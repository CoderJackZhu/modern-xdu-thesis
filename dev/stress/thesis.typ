// 压力测试：把一份真实的 112 页硕士论文（专业学位）用本模板重排
//
// 源：github.com/未公开的硕士论文仓库 —— 已通过学校格式检查的成品
// 生成方式：`python3 dev/stress/port.py <源仓库> dev/stress`（正文）
//           `python3 dev/stress/front-data.py <源chapter> dev/stress/front-data.typ`（前置数据）
//
// 目的：示例论文只有 33 页占位内容，覆盖不到真实体量。
//       这里用真实论文压一遍，看模板在**长文档 + 101 个公式 + 26 张图 + 102 条文献**
//       下会不会出问题，再与源 `main.pdf`（112 页）逐页对照。
//
// 编译（需先 bash dev/pkg-stage.sh）：
//   typst compile --root . dev/stress/thesis.typ /tmp/stress.pdf

#import "@preview/modern-xdu-thesis:0.1.0": documentclass
#import "front-data.typ": 符号表, 缩略语表, 简介

#let (
  doc,
  cover, title-cn, title-en, declaration, abstract, abstract-en,
  list-of-figures, list-of-tables, notation, abbreviations, outline-page,
  mainmatter, appendix, references, acknowledgement, bio, 引用,
) = documentclass(
  degree: "professional",
  blind: false,
  info: (
    title: ("复杂场景下的图像分析", "与理解"),
    title-en: ("Key Technologies for Controllable Multimodal Generation",
               "and Their Application to Interior Scenes"),
    author: "张三", author-en: "Zhang San",

    // 专业学位：领域
    domain: "人工智能", domain-en: "Artificial Intelligence",
    discipline: "电子科学与技术", discipline-en: "Electronic Science and Technology",

    degree-name: "电子信息硕士",
    degree-name-en: "Master of Electronic Information",

    supervisor: ("李四", "教授"), supervisor-en: ("Li Si", "Professor"),
    enterprise-supervisor: ("王五", "高级工程师"),
    enterprise-supervisor-en: ("Wang Wu", "Senior Engineer"),

    department: "电子工程学院", department-en: "School of Artificial Intelligence",
    submit-date: (year: 2025, month: 6),

    school-code: "10701", clc: "TP18", student-id: "22171214772", secret-level: "公开",

    abstract: include "abstract-zh.typ",
    abstract-en: include "abstract-en.typ",
    keywords: ("多模态理解与生成", "人工智能生成内容", "家居设计", "可控图像生成",
               "大语言模型", "风格迁移"),
    keywords-en: ("Multimodal Understanding and Generation", "AI-generated Content",
                  "Interior Design", "Controllable Image Generation",
                  "Large Language Model", "Style Transfer"),

    notation: 符号表,
    abbreviations: 缩略语表,
  ),
)

#show: doc

// ============================================================
// 前置部分（罗马页码；每页从奇数页起）
// ============================================================

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

#pagebreak(to: "odd")
#counter(page).update(5)
#list-of-figures()

#pagebreak(to: "odd")
#counter(page).update(7)
#list-of-tables()

#pagebreak(to: "odd")
#counter(page).update(9)
#notation()

#pagebreak(to: "odd")
#counter(page).update(11)
#abbreviations()

#pagebreak(to: "odd")
#counter(page).update(13)
#outline-page()

// ============================================================
// 正文（由 pandoc 从 LaTeX 转出，章号已补）
// ============================================================

#show: mainmatter.with(header-title: "西安电子科技大学硕士学位论文")

#include "body.typ"

// ============================================================
// 后置部分
// ============================================================

#pagebreak(to: "odd")
#references(bib: "/dev/stress/references.bib")

#pagebreak(to: "odd")
#acknowledgement(body: include "acknowledgements.typ")

#pagebreak(to: "odd")
#bio(items: 简介)
