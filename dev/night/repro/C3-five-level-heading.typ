// 五级标题与四级标题使用同样的括号编号，规格只定义到四级。
#import "../../../lib.typ": documentclass
#let t = documentclass()
#show: t.doc
#show: t.mainmatter
= 第一章 测试
== 节
=== 小节
==== 四级甲
正文。
===== 五级子项
正文。
