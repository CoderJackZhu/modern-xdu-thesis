// 虚构测试：bachelor/appendices，变体0
#import "../../../bachelor.typ": documentclass
#let t = documentclass(info: (
  title: ("虚构系统验证研究",),
  title-en: ("Fictional System Verification",),
  author: "测试作者",
  author-en: "Fictional Author",
  department: "电子工程学院",
  major: "电子信息工程",
  student-id: "202600001",
  discipline: "电子科学与技术",
  subdiscipline: "电路与系统",
  supervisor: ("测试导师甲", "测试导师乙"),
  supervisor-en: ("Fictional Advisor", "Professor"),
  abstract: [本段研究虚构系统的性能与验证方法，说明实验条件、数据来源和适用边界。所有人物、数据与成果均为虚构，不包含真实论文内容。

本段研究虚构系统的性能与验证方法，说明实验条件、数据来源和适用边界。所有人物、数据与成果均为虚构，不包含真实论文内容。

本段研究虚构系统的性能与验证方法，说明实验条件、数据来源和适用边界。所有人物、数据与成果均为虚构，不包含真实论文内容。

本段研究虚构系统的性能与验证方法，说明实验条件、数据来源和适用边界。所有人物、数据与成果均为虚构，不包含真实论文内容。],
  abstract-en: [This fictional experiment studies reliable modeling under controlled conditions. All names and results are synthetic and the assumptions are explicitly stated. This fictional experiment studies reliable modeling under controlled conditions. All names and results are synthetic and the assumptions are explicitly stated. This fictional experiment studies reliable modeling under controlled conditions. All names and results are synthetic and the assumptions are explicitly stated. This fictional experiment studies reliable modeling under controlled conditions. All names and results are synthetic and the assumptions are explicitly stated. This fictional experiment studies reliable modeling under controlled conditions. All names and results are synthetic and the assumptions are explicitly stated. ],
  acknowledgement: [本段研究虚构系统的性能与验证方法，说明实验条件、数据来源和适用边界。所有人物、数据与成果均为虚构，不包含真实论文内容。],
))
#show: t.doc
#(t.cover)()
#pagebreak(to: "odd")
#counter(page).update(1)
#(t.abstract)()
#pagebreak(to: "odd")
#(t.abstract-en)()
#pagebreak(to: "odd")
#(t.outline-page)()
#show: t.mainmatter

= 测试绪论 <head:one>

本段研究虚构系统的性能与验证方法，说明实验条件、数据来源和适用边界。所有人物、数据与成果均为虚构，不包含真实论文内容。

本段研究虚构系统的性能与验证方法，说明实验条件、数据来源和适用边界。所有人物、数据与成果均为虚构，不包含真实论文内容。

本段研究虚构系统的性能与验证方法，说明实验条件、数据来源和适用边界。所有人物、数据与成果均为虚构，不包含真实论文内容。

本段研究虚构系统的性能与验证方法，说明实验条件、数据来源和适用边界。所有人物、数据与成果均为虚构，不包含真实论文内容。



= 图表公式

本段研究虚构系统的性能与验证方法，说明实验条件、数据来源和适用边界。所有人物、数据与成果均为虚构，不包含真实论文内容。

#figure(rect(width: 45mm, height: 12mm), caption: [系统框图]) <fig:model>
#figure(table(columns: 2, [参数], [数值], [实验], [1]), caption: [参数设置]) <tab:model>
$ y = a x + b $ <eq:model>
图 @fig:model、表 @tab:model、式 @eq:model；见 @head:one。

#pagebreak(to: "odd")
#(t.appendix)(title: "补充材料A", body: [
本段研究虚构系统的性能与验证方法，说明实验条件、数据来源和适用边界。所有人物、数据与成果均为虚构，不包含真实论文内容。
#figure(rect(width: 30mm, height: 10mm), caption: [附录图0]) <fig:app0>
#figure(table(columns: 2, [甲], [乙]), caption: [附录表0]) <tab:app0>
$ z = x + 0 $ <eq:app0>
图 @fig:app0、表 @tab:app0、式 @eq:app0。
])

#pagebreak(to: "odd")
#(t.appendix)(title: "补充材料B", body: [
本段研究虚构系统的性能与验证方法，说明实验条件、数据来源和适用边界。所有人物、数据与成果均为虚构，不包含真实论文内容。
#figure(rect(width: 30mm, height: 10mm), caption: [附录图1]) <fig:app1>
#figure(table(columns: 2, [甲], [乙]), caption: [附录表1]) <tab:app1>
$ z = x + 1 $ <eq:app1>
图 @fig:app1、表 @tab:app1、式 @eq:app1。
])

#pagebreak(to: "odd")
#(t.appendix)(title: "补充材料C", body: [
本段研究虚构系统的性能与验证方法，说明实验条件、数据来源和适用边界。所有人物、数据与成果均为虚构，不包含真实论文内容。
#figure(rect(width: 30mm, height: 10mm), caption: [附录图2]) <fig:app2>
#figure(table(columns: 2, [甲], [乙]), caption: [附录表2]) <tab:app2>
$ z = x + 2 $ <eq:app2>
图 @fig:app2、表 @tab:app2、式 @eq:app2。
])

#pagebreak(to: "odd")
#(t.references)(entries: ())
#pagebreak(to: "odd")
#(t.acknowledgement)()
