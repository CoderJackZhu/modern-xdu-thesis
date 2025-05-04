#import "../utils/style.typ": 字号, 字体
#import "../utils/justify-text.typ": justify-text


// 研究生声明页
#let master-decl-page(
  anonymous: false,
  twoside: false,
  fonts: (:),
  stoke-width: 0.5pt,
  meta-info-inset: (x: 0pt, bottom: 2pt),
  meta-info-key-width: 35pt,
  info-inset: (x: 0pt, bottom: 0.5pt),
) = {
  // 0. 如果需要匿名则短路返回
  if anonymous {
    return
  }

  // 1.  默认参数
  fonts = 字体 + fonts




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
  width: 10%,  // 宽度设置为页面宽度的 100%
  stroke: (bottom: stoke-width + black),  // 设置底部的黑色边框
  text(
    font: fonts.宋体,  // 设置字体为宋体
    size: 字号.小五,  // 设置字体大小为小五
    bottom-edge: "descender",  // 设置底边对齐方式
    "  "  // 确保传递了文本内容，填入正文
  ),
)
  }

   let meta-info-key = info-key.with(info-inset: meta-info-inset, is-meta: true)
let meta-info-value = info-value.with(info-inset: meta-info-inset, is-meta: true)

  // 2.  正式渲染
  pagebreak(weak: true, to: if twoside { "odd" })

  v(25pt)

  align(
    center,
    text(
      font: fonts.黑体,
      size: 字号.四号,
      weight: "bold",
      "西安电子科技大学\n学位论文独创性（或创新性）声明",
    ),
  )

  v(20pt)

  block[
    #set text(font: fonts.宋体, size: 字号.小四)
    #set par(justify: true, first-line-indent: (amount: 2em, all: true), leading: 1.2em)

    秉承学校严谨的学风和优良的科学道德，本人声明所呈交的论文是我个人在导师指导下进行的研究工作及取得的研究成果。尽我所知，除了文中特别加以标注和致谢中所罗列的内容以外，论文中不包含其他人已经发表或撰写过的研究成果；也不包含为获得西安电子科技大学或其它教育机构的学位或证书而使用过的材料。与我一同工作的同事对本研究所做的任何贡献均已在论文中作了明确的说明并表示了谢意。
    
    学位论文若有不实之处，本人承担一切法律责任。  
  ]

  v(23pt)

  // align(left)[
  //   #set text(font: fonts.黑体, size: 字号.小四)
  //   //左对齐
  //   研究生签名：
  // ]

block(width: 70pt, grid(
    columns: (auto, 1fr),
    meta-info-key("分类号"),
    meta-info-value("研究生签名：", "   "),
    meta-info-key("日期"),
    meta-info-value("clc", ""),
  ))


  v(40pt)

align(
    center,
    text(
      font: fonts.黑体,
      size: 字号.四号,
      weight: "bold",
      "西安电子科技大学\n关于论文使用授权的说明",
    ),
  )

  v(20pt)

  block[
    #set text(font: fonts.宋体, size: 字号.小四)
    #set par(justify: true, first-line-indent: (amount: 2em, all: true), leading: 1.2em)

    本人完全了解西安电子科技大学有关保留和使用学位论文的规定，即：研究生在校攻读学位期间论文工作的知识产权属于西安电子科技大学。学校有权保留并向国家有关部门或机构送交学位论文的复印件和电子版，以学术交流为目的赠送和交换学位论文，允许学位论文被查阅、借阅和复印，将学位论文的全部或部分内容编入有关数据库进行检索和提供相应阅览服务；允许采用影印、缩印或其它复制手段保存学位论文。同时本人保证，结合学位论文研究成果完成的论文、发明专利等成果，署名单位为西安电子科技大学。

本人保证遵守上述规定。

（保密的论文在解密后遵守此规定）  
  ]

  v(43pt)

  align(right)[
    #set text(font: fonts.黑体, size: 字号.小四)
    
    研究生签名：#h(5.8em)
    日期：#h(5.8em)
  ]

}
