#import "../utils/datetime-display.typ": datetime-display, datetime-en-display
#import "../utils/justify-text.typ": justify-text
#import "../utils/style.typ": 字号, 字体

// 硕士研究生封面
#let master-cover(
  // documentclass 传入的参数
  doctype: "master",
  degree: "academic",
  nl-cover: false,
  anonymous: false,
  twoside: false,
  fonts: (:),
  info: (:),
  // 其他参数
  stoke-width: 0.5pt,
  min-title-lines: 2,
  min-reviewer-lines: 5,
  info-inset: (x: 0pt, bottom: 0.5pt),
  info-key-width: 86pt,
  info-column-gutter: 18pt,
  info-row-gutter: 12pt,
  //左上角
  meta-block-inset-left: (left: -15pt,  top: 0pt),
  //右上角
  meta-block-inset-right: (left: 325pt, right: -400pt, top: 0pt),
  meta-info-inset: (x: 0pt, bottom: 2pt),
  meta-info-key-width: 35pt,
  meta-info-column-gutter: 10pt,
  meta-info-row-gutter: 1pt,
  defence-info-inset: (x: 0pt, bottom: 0pt),
  defence-info-key-width: 110pt,
  defence-info-column-gutter: 2pt,
  defence-info-row-gutter: 12pt,
  anonymous-info-keys: ("student-id", "author", "author-en", "supervisor", "supervisor-en", "supervisor-ii", "supervisor-ii-en", "chairman", "reviewer"),
  datetime-display: datetime-display,
  datetime-en-display: datetime-en-display,
) = {
  // 1.  默认参数
  fonts = 字体 + fonts

  // 2.  对参数进行处理
  // 2.1 如果是字符串，则使用换行符将标题分隔为列表
  if type(info.title) == str {
    info.title = info.title.split("\n")
  }
  if type(info.title-en) == str {
    info.title-en = info.title-en.split("\n")
  }
  // 2.2 根据 min-title-lines 和 min-reviewer-lines 填充标题和评阅人
  info.title = info.title + range(min-title-lines - info.title.len()).map((it) => "　")
  info.reviewer = info.reviewer + range(min-reviewer-lines - info.reviewer.len()).map((it) => "　")
  // 2.3 处理日期
  assert(type(info.submit-date) == datetime, message: "submit-date must be datetime.")
  if type(info.defend-date) == datetime {
    info.defend-date = datetime-display(info.defend-date)
  }
  if type(info.confer-date) == datetime {
    info.confer-date = datetime-display(info.confer-date)
  }
  if type(info.bottom-date) == datetime {
    info.bottom-date = datetime-display(info.bottom-date)
  }
  // 2.4 处理 degree
  if info.degree == auto {
    if doctype == "doctor" {
      info.degree = "工程博士"
    } else {
      info.degree = "工程硕士"
    }
  }

  // 3.  内置辅助函数
  let info-key(body, info-inset: info-inset, is-meta: false) = {
    set text(
      font: if is-meta { fonts.宋体 } else { fonts.楷体 },
      size: if is-meta { 字号.小五 } else { 字号.三号 },
      weight: if is-meta { "regular" } else { "bold" },
    )
    rect(
      width: 100%,
      inset: info-inset,
      stroke: none,
      justify-text(with-tail: is-meta, body)
    )
  }

  let info-value(key, body, info-inset: info-inset, is-meta: false, no-stroke: false) = {
    set align(center)
    rect(
      width: 100%,
      inset: info-inset,
      stroke: if no-stroke { none } else { (bottom: stoke-width + black) },
      text(
        font: if is-meta { fonts.宋体 } else { fonts.楷体 },
        size: if is-meta { 字号.小五 } else { 字号.三号 },
        bottom-edge: "descender",
        if anonymous and (key in anonymous-info-keys) {
          if is-meta { "█████" } else { "██████████" }
        } else {
          body
        },
      ),
    )
  }

  let anonymous-text(key, body) = {
    if anonymous and (key in anonymous-info-keys) {
      "██████████"
    } else {
      body
    }
  }

  let meta-info-key = info-key.with(info-inset: meta-info-inset, is-meta: true)
  let meta-info-value = info-value.with(info-inset: meta-info-inset, is-meta: true)
  let defence-info-key = info-key.with(info-inset: defence-info-inset)
  let defence-info-value = info-value.with(info-inset: defence-info-inset)
  

  // 4.  正式渲染
  pagebreak(weak: true, to: if twoside { "odd" })

  block(width: 70pt, inset: meta-block-inset-left, grid(
    columns: (meta-info-key-width, 1fr),
    column-gutter: meta-info-column-gutter,
    row-gutter: meta-info-row-gutter,
    meta-info-key("学校代码"),
    meta-info-value("school-code", info.school-code),
    meta-info-key("分类号"),
    meta-info-value("clc", info.clc),
  ))

    block(width: 70pt, inset: meta-block-inset-right, grid(
    columns: (meta-info-key-width, 1fr), 
    //右对齐
    column-gutter: meta-info-column-gutter,
    row-gutter: meta-info-row-gutter,
    meta-info-key("密级"),
    meta-info-value("secret-level", info.secret-level),
    meta-info-key("学号"),
    meta-info-value("student-id", info.student-id),
  ))

  // 居中对齐
  set align(center)

  // 匿名化处理去掉封面标识
  if anonymous {
    v(70pt)
  } else {
    
  text(size: 28pt, font: fonts.宋体, spacing: 200%, weight: "bold",
    { "西安电子科技大学"}
  )
    
    v(30pt)
  }

  // 将中文之间的空格间隙从 0.25 em 调整到 0.5 em
  text(size: 24pt, font: fonts.宋体,
    if doctype == "doctor" { "博 士 学 位 论 文" } else { "硕 士 学 位 论 文" },
  )
  
  if anonymous {
    v(132pt)
  } else {
    v(100pt)
  }

  text(size: 24pt, font: fonts.宋体, spacing: 200%, weight: "bold",
    { info.title.intersperse("\n").sum() }
  )

  v(30pt)
  
  block(width: 294pt, grid(
    columns: (info-key-width, 1fr),
    column-gutter: info-column-gutter,
    row-gutter: info-row-gutter,
    
    info-key("作者姓名"),
    info-value("author", info.author),
    ..(if degree == "professional" {(
      {
        set text(font: fonts.楷体, size: 字号.三号, weight: "bold")
        info-key("领域")
      },
      info-value("domain", info.domain ),
    )} else {(
      info-key("专业名称"),
      info-value("major", info.major),
    )}),
    info-key("学校导师姓名、职称："),
    info-value("supervisor", info.supervisor.intersperse(" ").sum()),
    info-key("企业导师姓名、职称："),
    info-value("supervisor", info.supervisor.intersperse(" ").sum()),
  ))

  v(50pt)

  text(font: fonts.楷体, size: 字号.三号, datetime-display(info.submit-date))


  // 第二页
  pagebreak(weak: true)

  v(161pt)

  block(width: 284pt, grid(
    columns: (defence-info-key-width, 1fr),
    column-gutter: defence-info-column-gutter,
    row-gutter: defence-info-row-gutter,
    defence-info-key("答辩委员会主席"),
    defence-info-value("chairman", info.chairman),
    defence-info-key("评阅人"),
    ..info.reviewer.map((s) => defence-info-value("reviewer", s)).intersperse(defence-info-key("　")),
    defence-info-key("论文答辩日期"),
    defence-info-value("defend-date", info.defend-date, no-stroke: true),
  ))

  v(216pt)

  align(left, box(width: 7.3em, text(font: fonts.楷体, size: 字号.三号, weight: "bold", justify-text(with-tail: true, "研究生签名"))))

  v(7pt)

  align(left, box(width: 7.3em, text(font: fonts.楷体, size: 字号.三号, weight: "bold", justify-text(with-tail: true, "导师签名"))))

  // 第三页英文封面页
  pagebreak(weak: true)

  set text(font: fonts.楷体, size: 字号.小四)
  set par(leading: 1.3em)

  v(45pt)
  
  text(font: fonts.黑体, size: 字号.二号, weight: "bold", info.title-en.intersperse("\n").sum())

  v(36pt)

  text(size: 字号.四号)[by]

  v(-6pt)

  text(font: fonts.黑体, size: 字号.四号, weight: "bold", anonymous-text("author-en", info.author-en))

  v(11pt)

  text(size: 字号.四号)[Supervised by]

  v(-6pt)

  text(font: fonts.黑体, size: 字号.四号, anonymous-text("supervisor-en", info.supervisor-en))

  if info.supervisor-ii-en != "" {
    v(-4pt)
    
    text(font: fonts.黑体, size: 字号.四号, anonymous-text("supervisor-ii-en", info.supervisor-ii-en))

    v(-9pt)
  }

  v(26pt)

  [
    A dissertation submitted to  \
    the graduate school of #(if not anonymous { "Nanjing University" })  \
    in partial fulfilment of the requirements for the degree of  \
  ]

  v(6pt)

  smallcaps(if doctype == "doctor" { "Doctor of phlosophy" } else { "Master" })

  v(6pt)

  [in]

  v(6pt)

  info.major-en
  
  v(46pt)

  if not anonymous {
    [Xidian University]
  }

  v(28pt)

  info.department-en

  v(2pt)

  if not anonymous {
    [Nanjing University]
  }

  v(28pt)

  datetime-en-display(info.submit-date)
}