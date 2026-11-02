// 博士入口暴露内部len方法错误。
#import "../../../doctor.typ": documentclass
#let t = documentclass(info: (title: none,))
#show: t.doc
#(t.cover)()
