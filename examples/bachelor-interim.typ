// 本科毕业设计（论文）中期报告示例
#import "@preview/modern-xdu-thesis:0.3.0": bachelor-interim-documentclass

#let (doc, interim) = bachelor-interim-documentclass(
  info: (
    title: ("面向校园场景的文本检索工具设计与实现"),
    author: "张三",
    major: "电子信息工程",
    student-id: "22010100001",
    supervisor: "李四　教授",
    department: "电子工程学院",
    report-date: "2027 年 4 月",
  ),
)

#show: doc

#interim(body: (
  titleAndSchedule: [
    未更换题目。已完成需求分析、基础数据整理和原型开发，进度与原开题计划基本一致。
  ],
  completed: [
    完成文本清洗和倒排索引模块；实现查询界面；在虚构数据集上完成两组功能测试，
    并记录了查询响应时间和结果排序情况。
  ],
  nextPlan: [
    补充语义检索对照实验，完善异常输入处理，完成结果分析和论文主体撰写。
  ],
  difficulties: [测试数据规模有限，语义检索模型的部署时间超出预期。],
  feasibility: [
    核心功能已经可以运行，剩余工作主要是补充实验和整理文档，预计可按计划完成。
  ],
  advisorOpinion: [进度正常，建议补充对照实验并规范记录测试条件。],
  groupOpinion: [中期检查通过，按意见继续完成后续工作。],
  unitReview: [同意继续开展毕业设计工作。],
))
