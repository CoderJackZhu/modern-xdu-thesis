// 双语:true 是本科 references 的公开参数，但英文多作者仍显示“等”。
#import "../../../bachelor.typ": documentclass
#let t = documentclass()
#show: t.doc
#show: t.mainmatter
= 测试
引用#cite(<english>)。
#pagebreak(to: "odd")
#(t.references)(双语: true, body: bibliography("A4-english.bib", style: "gb-7714-2015-numeric", title: none))
