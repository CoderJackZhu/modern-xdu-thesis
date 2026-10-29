// 研究生开题报告示例；编译参数：--input graduate=doctor --input degree=professional
#import "@preview/modern-xdu-thesis:0.3.0": proposal-documentclass

#let 层次 = sys.inputs.at("graduate", default: "master")
#let 学位 = sys.inputs.at("degree", default: "academic")
#let 专业 = 学位 == "professional"

#let (doc, proposal) = proposal-documentclass(
  graduate: 层次,
  degree: 学位,
  info: (
    title: ("面向复杂系统的可靠建模", "与验证方法研究"),
    author: "张三",
    student-id: "2026000001",
    department: "电子工程学院",
    discipline: "电子科学与技术",
    subdiscipline: "电路与系统",
    degree-name: if 层次 == "doctor" {
      if 专业 { "工程博士" } else { "工学博士" }
    } else {
      if 专业 { "电子信息硕士" } else { "工学硕士" }
    },
    domain: "电子信息",
    supervisor: "李四　教授",
    enterprise-supervisor: if 专业 { "王五　高级工程师" } else { "" },
    proposal-date: "2026 年 10 月",
    internship-unit: "示例技术有限公司",
    internship-post: "算法研发",
    internship-mode: "校外",
    internship-period: "2026 年 7 月至 2027 年 6 月",
    thesis-type: "应用基础技术",
  ),
)

#show: doc

#proposal(body: (
  topicSource: [国家自然科学基金项目（示例）。],
  abstract: [
    本报告围绕复杂系统的可靠建模与验证开展研究，说明研究目标、技术路线和预期成果。
    全部姓名、单位、项目和成果均为虚构，仅用于展示开题报告的结构与排版。
  ],
  significance: [
    复杂系统广泛存在于通信、控制与计算平台。明确系统边界、故障模式和验证条件，
    有助于提高模型的可复核性，并为后续实验设计提供依据。
  ],
  researchStatus: [
    现有研究通常分别处理建模、仿真和测试。不同方法的数据接口与评价指标尚不统一，
    因此需要建立可重复的实验流程，并明确每种方法的适用条件。
  ],
  goal: [建立可复现的复杂系统建模流程，形成能够支持实验验证和结果分析的模板化方法。],
  researchContent: [
    研究内容包括需求抽象、模型构建、实验设计、结果评价和工具实现五个部分。
    各部分通过统一的数据结构连接，使读者能够追踪从假设到结论的完整过程。
  ],
  keyProblems: [
    一是不同来源数据的一致性；二是实验条件难以复现；三是评价指标与工程目标之间的映射。
  ],
  methods: [
    采用文献分析、原型实现和对照实验相结合的方法。先构建最小可行原型，再通过重复实验
    检查结果稳定性，最后比较不同参数设置对系统性能的影响。
  ],
  innovation: if 层次 == "doctor" [
    拟提出面向跨阶段验证的统一数据模型，并将建模假设、实验条件和评价结果关联起来。
  ] else { none },
  plan: [
    2026 年 10 月至 2027 年 1 月：完成文献调研和问题定义。#linebreak()
    2027 年 2 月至 2027 年 6 月：完成原型与第一轮实验。#linebreak()
    2027 年 7 月至 2027 年 12 月：完善方法、整理结果并撰写论文。
  ],
  foundation: [已具备计算服务器、开发环境和基础实验数据，完成了前期可行性验证。],
  achievements: [已整理技术报告一份，完成了原型系统的第一版。],
  record: [专家组建议进一步明确实验边界，并补充与现有方法的对照。],
  rubric: (
    "论文选题": "良好",
    "研究方案": "良好",
    "研究基础": "合格",
    "进度安排": "良好",
  ),
  conclusion: [开题报告通过。请按专家意见完善技术路线和进度安排后进入论文工作。],
  advisorOpinion: [同意开题，按专家组意见修改后继续开展研究。],
))
