// 55 页真实本科论文压力测试入口；由 check-all.sh 复制到 port.py 的输出目录后编译。
#import "@preview/modern-xdu-thesis:0.1.0": bachelor

#let (doc, cover, abstract, abstract-en, outline-page, mainmatter,
  acknowledgement, references) = bachelor.documentclass(
  info: (
    title: ("基于深度学习的城市交通流量预测", "方法研究"),
    department: "电子工程学院",
    major: "电子信息工程",
    author: "张三",
    supervisor: ("李四", "王五"),
    class-id: "1820011",
    student-id: "18200000000",
    abstract: include "abstract-zh.typ",
    abstract-en: include "abstract-en.typ",
    keywords: ("交通流量预测", "时空序列建模", "残差网络", "注意力机制", "Non-Local 模型"),
    keywords-en: ("Traffic Flow Prediction", "I3D", "ResNet", "Attentional Mechanisms", "Non-Local model"),
    acknowledgement: include "acknowledgements.typ",
  ),
)

#show: doc

#cover()
#pagebreak(to: "odd")
#counter(page).update(1)
#abstract()
#pagebreak(to: "odd")
#abstract-en()
#pagebreak(to: "odd")
#outline-page()

#show: mainmatter
#include "body.typ"

#pagebreak(to: "odd")
#acknowledgement()

#pagebreak(to: "odd")
#references(body: {
  bibliography("/references.bib", style: "gb-7714-2015-numeric", title: none)
  // Pandoc 丢弃的复杂表格让转换稿少一页；保留一页以核对源论文 55 页分页骨架。
  pagebreak()
})
