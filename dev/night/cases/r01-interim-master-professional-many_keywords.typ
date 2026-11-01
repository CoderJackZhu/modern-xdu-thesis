// 全部内容为虚构测试
// 研究生中期考核报告示例；编译参数：--input graduate=doctor --input degree=professional
#import "../../../supporting/interim.typ": interim-documentclass

#let 层次 = "master"
#let 学位 = "professional"
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
关键词：关键词0；关键词1；关键词2；关键词3；关键词4；关键词5；关键词6；关键词7；关键词8；关键词9；关键词10；关键词11；关键词12；关键词13；关键词14；关键词15；关键词16；关键词17；关键词18；关键词19；关键词20；关键词21；关键词22；关键词23；关键词24；关键词25；关键词26；关键词27；关键词28；关键词29；关键词30；关键词31；关键词32；关键词33；关键词34；关键词35；关键词36；关键词37；关键词38；关键词39；关键词40；关键词41；关键词42；关键词43；关键词44；关键词45；关键词46；关键词47；关键词48；关键词49；关键词50；关键词51；关键词52；关键词53；关键词54；关键词55；关键词56；关键词57；关键词58；关键词59


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
