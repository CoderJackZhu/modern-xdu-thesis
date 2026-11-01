// 本科入口缺少必填题目的类型校验。
#import "../../../bachelor.typ": documentclass
#let t = documentclass(info: (title: none,))
#show: t.doc
#(t.cover)()
