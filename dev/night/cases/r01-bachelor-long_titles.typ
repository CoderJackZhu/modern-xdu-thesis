// 虚构测试：bachelor/long_titles，变体0
#import "../../../bachelor.typ": documentclass
#let t = documentclass(info: (
  title: ("面向多源异构数据的可靠系统建模及验证方法研究面向多源异构数据的可靠系统建模及验证方法研究面向多源异构数据的可靠系统建模及验证方法研究面向多源异构数据的可靠系统建模及验证方法研究面向多源异构数据的可靠系统建模及验证方法研究",),
  title-en: ("Reliable Modeling and Verification of Heterogeneous Complex Systems Reliable Modeling and Verification of Heterogeneous Complex Systems Reliable Modeling and Verification of Heterogeneous Complex Systems Reliable Modeling and Verification of Heterogeneous Complex Systems Reliable Modeling and Verification of Heterogeneous Complex Systems Reliable Modeling and Verification of Heterogeneous Complex Systems ",),
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
#(t.references)(entries: ())
#pagebreak(to: "odd")
#(t.acknowledgement)()
