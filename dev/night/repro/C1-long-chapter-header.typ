// 规格未规定长章名在页眉中应折行、缩小还是截断；当前多行页眉越过双线。
#import "../../../lib.typ": documentclass
#let t = documentclass()
#show: t.doc
#show: t.mainmatter
#heading(level: 1, "第一章 " + "复杂系统的鲁棒建模方法与验证 " * 9)
正文内容。
