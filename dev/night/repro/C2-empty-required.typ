// 规格列有题目、作者、学号，但未规定空字符串的校验策略。
#import "../../../lib.typ": documentclass
#let t = documentclass(info: (title: "", author: "", student-id: "",))
#show: t.doc
#(t.cover)()
#pagebreak()
#(t.title-cn)()
