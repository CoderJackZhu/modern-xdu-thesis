// 虚构测试：master-academic-blind/code_notes_lists，变体0
#import "../../../lib.typ": documentclass
#let t = documentclass(degree: "academic", blind: true, info: (
  title: ("虚构系统验证研究",),
  title-en: ("Fictional System Verification",),
  author: "测试作者",
  author-en: "Fictional Author",
  department: "电子工程学院",
  major: "电子信息工程",
  student-id: "202600001",
  discipline: "电子科学与技术",
  subdiscipline: "电路与系统",
  supervisor: ("测试导师", "教授"),
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
#(t.title-cn)()
#pagebreak(to: "odd")
#(t.title-en)()
#pagebreak(to: "odd")
#(t.declaration)()
#pagebreak(to: "odd")
#counter(page).update(1)
#(t.abstract)()
#pagebreak(to: "odd")
#(t.abstract-en)()
#pagebreak(to: "odd")
#(t.list-of-figures)()
#pagebreak(to: "odd")
#(t.list-of-tables)()
#pagebreak(to: "odd")
#(t.notation)()
#pagebreak(to: "odd")
#(t.abbreviations)()
#pagebreak(to: "odd")
#(t.outline-page)()
#show: t.mainmatter

= 第一章 测试绪论 <head:one>

本段研究虚构系统的性能与验证方法，说明实验条件、数据来源和适用边界。所有人物、数据与成果均为虚构，不包含真实论文内容。

本段研究虚构系统的性能与验证方法，说明实验条件、数据来源和适用边界。所有人物、数据与成果均为虚构，不包含真实论文内容。

本段研究虚构系统的性能与验证方法，说明实验条件、数据来源和适用边界。所有人物、数据与成果均为虚构，不包含真实论文内容。

本段研究虚构系统的性能与验证方法，说明实验条件、数据来源和适用边界。所有人物、数据与成果均为虚构，不包含真实论文内容。

正文带脚注#footnote[脚注内容用于检查长文档。]。

```python
def fictional(value):
    return value + 1
```

- 一级列表
  - 二级列表
    - 三级列表
- 第二个项目

本段研究虚构系统的性能与验证方法，说明实验条件、数据来源和适用边界。所有人物、数据与成果均为虚构，不包含真实论文内容。

本段研究虚构系统的性能与验证方法，说明实验条件、数据来源和适用边界。所有人物、数据与成果均为虚构，不包含真实论文内容。

本段研究虚构系统的性能与验证方法，说明实验条件、数据来源和适用边界。所有人物、数据与成果均为虚构，不包含真实论文内容。

本段研究虚构系统的性能与验证方法，说明实验条件、数据来源和适用边界。所有人物、数据与成果均为虚构，不包含真实论文内容。

本段研究虚构系统的性能与验证方法，说明实验条件、数据来源和适用边界。所有人物、数据与成果均为虚构，不包含真实论文内容。

本段研究虚构系统的性能与验证方法，说明实验条件、数据来源和适用边界。所有人物、数据与成果均为虚构，不包含真实论文内容。

本段研究虚构系统的性能与验证方法，说明实验条件、数据来源和适用边界。所有人物、数据与成果均为虚构，不包含真实论文内容。

本段研究虚构系统的性能与验证方法，说明实验条件、数据来源和适用边界。所有人物、数据与成果均为虚构，不包含真实论文内容。

= 第二章 图表公式

本段研究虚构系统的性能与验证方法，说明实验条件、数据来源和适用边界。所有人物、数据与成果均为虚构，不包含真实论文内容。

#figure(rect(width: 45mm, height: 12mm), caption: [系统框图]) <fig:model>
#figure(table(columns: 2, [参数], [数值], [实验], [1]), caption: [参数设置]) <tab:model>
$ y = a x + b $ <eq:model>
图 @fig:model、表 @tab:model、式 @eq:model；见 @head:one。

#pagebreak(to: "odd")
#(t.references)(entries: ())
#pagebreak(to: "odd")
#(t.acknowledgement)()
#pagebreak(to: "odd")
#(t.bio)()
