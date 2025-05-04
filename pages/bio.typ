// 致谢页
#let bio(
  // documentclass 传入参数
  anonymous: false,
  twoside: false,
  // 其他参数
  title: "作者简介",
  outlined: true,
  body,
) = {
  if not anonymous {
    pagebreak(weak: true, to: if twoside { "odd" })
    [
      #heading(level: 1, numbering: none, outlined: outlined, title) <no-auto-pagebreak>

      #body
    ]
  }
}