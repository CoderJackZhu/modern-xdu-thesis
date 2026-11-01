// 无效必填字段应提示字段名称；当前暴露内部枚举方法错误。
#import "../../../lib.typ": documentclass
#let t = documentclass(info: (title: none,))
#show: t.doc
#(t.cover)()
