// 六行题目与中文题名页的固定字段发生覆盖。
#import "../../../lib.typ": documentclass
#let t = documentclass(info: (title: "面向多源异构数据的可靠系统建模及验证方法研究" * 5,))
#show: t.doc
#(t.title-cn)()
