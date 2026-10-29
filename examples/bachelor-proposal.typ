// 本科毕业设计（论文）开题报告示例
#import "@preview/modern-xdu-thesis:0.3.1": bachelor-proposal-documentclass

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
