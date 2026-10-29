// 研究生中期考核报告示例；编译参数：--input graduate=doctor --input degree=professional
#import "@preview/modern-xdu-thesis:0.3.1": interim-documentclass

#let 层次 = sys.inputs.at("graduate", default: "master")
#let 学位 = sys.inputs.at("degree", default: "academic")
#let 专业 = 学位 == "professional"

#let (doc, interim) = interim-documentclass(
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
    report-date: "2027 年 6 月",
  ),
)

#show: doc

#interim(body: (
  topicSource: [国家自然科学基金项目（示例）。],
  goalContent: [
    建立可复现的复杂系统建模流程，形成支持实验验证和结果分析的模板化方法。
  ],
  completed: [
    已完成文献调研、需求抽象和原型系统第一版；完成了两组基准实验，
    并对实验结果进行了统计和误差分析。
  ],
  changes: [
    原计划采用单一评价指标，实验后发现该指标不能反映系统在异常输入下的稳定性，
    因此增加了鲁棒性测试，但总体研究目标未改变。
  ],
  nextPlan: [
    下一阶段将补充跨场景实验，完善数据接口，并完成论文主体章节的撰写。
  ],
  publications: [
    已投稿学术论文一篇（示例）；拟整理技术报告和实验数据说明各一份。
  ],
  advisorOpinion: [研究进度基本符合计划，建议加强对照实验和结果复现。],
  conclusion: [中期考核通过。请按专家意见完善实验并推进后续论文工作。],
))
