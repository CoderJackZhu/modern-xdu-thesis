// 字段允许多长、折行后怎样避免覆盖下一栏，规格未定义。
#import "../../../lib.typ": documentclass
#let t = documentclass(info: (author: "阿卜杜拉·复杂系统联合实验中心研究者姓名很长" * 3,))
#show: t.doc
#(t.cover)()
