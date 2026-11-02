// 同一个章标题用于目录、页眉和正文时，脚注会重复生成。
#import "../../../lib.typ": documentclass
#let t = documentclass()
#show: t.doc
#(t.outline-page)()
#show: t.mainmatter
= 第一章 绪论#footnote[唯一的标题说明]
#for i in range(70) [测试正文用于让同一章跨越多个页眉。

]
