// 双下划线
#let double-underline(body) = context {
  let size = measure(body)
  stack(
    body,
    v(3pt),
    line(length: size.width),
    v(2pt),
    line(length: size.width),
  )
}
//全长度下划线
#let double-underline-full(body) = context {
  // 获取正文的宽度
  let size = measure("A4")

  stack(
    body,
    v(3pt),
    line(length: size.width),
    v(2pt),
    line(length: size.width),
  )
}