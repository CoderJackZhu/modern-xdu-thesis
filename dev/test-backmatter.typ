// 测试：P4 后置部分（附录 / 参考文献 / 致谢 / 作者简介）
#import "../lib.typ": documentclass

#let (doc, appendix, references, acknowledgement, bio) = documentclass(
  degree: "professional",
  info: (title: ("测试",), author: "张三"),
)
#show: doc

#appendix()
#pagebreak(to: "odd")
#references()
#pagebreak(to: "odd")
#acknowledgement()
#pagebreak(to: "odd")
#bio()
