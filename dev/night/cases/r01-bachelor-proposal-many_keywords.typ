// 全部内容为虚构测试
// 本科毕业设计（论文）开题报告示例
#import "../../../supporting/bachelor-forms.typ": bachelor-proposal-documentclass

#let (doc, proposal) = bachelor-proposal-documentclass(
  info: (
    title: ("面向校园场景的文本检索", "工具设计与实现"),
    author: "张三",
    major: "电子信息工程",
    student-id: "22010100001",
    supervisor: "李四　教授",
    department: "电子工程学院",
    class-year: "2026",
    proposal-date: "2026 年 10 月",
  ),
)

#show: doc

#proposal(body: (
  titleSource: [教师科研项目（示例）。],
  purpose: [
关键词：关键词0 / fictional keyword 0；关键词1 / fictional keyword 1；关键词2 / fictional keyword 2；关键词3 / fictional keyword 3；关键词4 / fictional keyword 4；关键词5 / fictional keyword 5；关键词6 / fictional keyword 6；关键词7 / fictional keyword 7；关键词8 / fictional keyword 8；关键词9 / fictional keyword 9；关键词10 / fictional keyword 10；关键词11 / fictional keyword 11；关键词12 / fictional keyword 12；关键词13 / fictional keyword 13；关键词14 / fictional keyword 14；关键词15 / fictional keyword 15；关键词16 / fictional keyword 16；关键词17 / fictional keyword 17；关键词18 / fictional keyword 18；关键词19 / fictional keyword 19；关键词20 / fictional keyword 20；关键词21 / fictional keyword 21；关键词22 / fictional keyword 22；关键词23 / fictional keyword 23；关键词24 / fictional keyword 24；关键词25 / fictional keyword 25；关键词26 / fictional keyword 26；关键词27 / fictional keyword 27；关键词28 / fictional keyword 28；关键词29 / fictional keyword 29；关键词30 / fictional keyword 30；关键词31 / fictional keyword 31；关键词32 / fictional keyword 32；关键词33 / fictional keyword 33；关键词34 / fictional keyword 34；关键词35 / fictional keyword 35；关键词36 / fictional keyword 36；关键词37 / fictional keyword 37；关键词38 / fictional keyword 38；关键词39 / fictional keyword 39；关键词40 / fictional keyword 40；关键词41 / fictional keyword 41；关键词42 / fictional keyword 42；关键词43 / fictional keyword 43；关键词44 / fictional keyword 44；关键词45 / fictional keyword 45；关键词46 / fictional keyword 46；关键词47 / fictional keyword 47；关键词48 / fictional keyword 48；关键词49 / fictional keyword 49；关键词50 / fictional keyword 50；关键词51 / fictional keyword 51；关键词52 / fictional keyword 52；关键词53 / fictional keyword 53；关键词54 / fictional keyword 54；关键词55 / fictional keyword 55；关键词56 / fictional keyword 56；关键词57 / fictional keyword 57；关键词58 / fictional keyword 58；关键词59 / fictional keyword 59


    设计一个可检索校园公开文本的小型工具，验证文本预处理、索引构建和结果排序方法，
    并通过对照实验分析不同参数对检索效果的影响。
  ],
  researchStatus: [
    现有检索系统通常采用倒排索引和向量表示两类方案。前者实现简单、可解释性较好，
    后者更适合处理语义相近的查询，但需要额外考虑模型部署和计算成本。
  ],
  researchContent: [
    完成文本清洗、索引构建、查询接口和结果评价四个模块；实现一个小规模原型，
    使用虚构数据完成功能和性能测试，并总结不同方案的适用范围。
  ],
  schedule: [
    2026 年 10 月：完成需求分析和资料收集。#linebreak()
    2026 年 11 月至 2027 年 2 月：完成原型开发和第一轮测试。#linebreak()
    2027 年 3 月至 2027 年 4 月：完成对照实验、论文撰写和答辩准备。
  ],
  preparation: [已完成相关课程学习，搭建开发环境，并整理了基础测试数据。],
  advisorOpinion: [同意开题，建议进一步明确测试指标和数据规模。],
  schoolOpinion: [同意开题。],
))
