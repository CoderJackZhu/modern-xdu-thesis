// 多行公式的编号应位于最后一行最右侧。
#import "../../../lib.typ": documentclass
#let t = documentclass()
#show: t.doc
#show: t.mainmatter
= 第一章 测试
$ y &= a x + b \ z &= c x + d $ <eq:multi>
见 @eq:multi。
