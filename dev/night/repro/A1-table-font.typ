// 表格未显式覆盖字号：模板应遵守五号10.5pt。
#import "../../../lib.typ": documentclass
#let t = documentclass()
#show: t.doc
#show: t.mainmatter
= 第一章 测试
#figure(table(columns: 2, [参数], [数值], [样本], [1]), caption: [字号复现])
