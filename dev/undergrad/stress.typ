// 55 页真实本科论文压力测试入口；由 check-all.sh 复制到 port.py 的输出目录后编译。
#import "@preview/modern-xdu-thesis:0.2.0": bachelor

#let (doc, cover, abstract, abstract-en, outline-page, mainmatter,
  acknowledgement, references) = bachelor.documentclass(
  info: (
    title: ("基于视频的人体动作识别", "算法研究"),
    department: "人工智能学院",
    major: "智能科学与技术",
    author: "朱一杰",
    supervisor: ("缑水平", "李睿敏"),
    class-id: "1820011",
    student-id: "18200100036",
    abstract: include "abstract-zh.typ",
    abstract-en: include "abstract-en.typ",
    keywords: ("动作识别", "膨胀三维卷积神经网络", "残差网络", "注意力机制", "Non-Local 模型"),
    keywords-en: ("Action Recognition", "I3D", "ResNet", "Attentional Mechanisms", "Non-Local model"),
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
