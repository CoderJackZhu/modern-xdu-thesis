// 全部内容为虚构测试
// 研究生中期考核报告示例；编译参数：--input graduate=doctor --input degree=professional
#import "../../../supporting/interim.typ": interim-documentclass

#let 层次 = "master"
#let 学位 = "academic"
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
关键词：关键词0 / fictional keyword 0；关键词1 / fictional keyword 1；关键词2 / fictional keyword 2；关键词3 / fictional keyword 3；关键词4 / fictional keyword 4；关键词5 / fictional keyword 5；关键词6 / fictional keyword 6；关键词7 / fictional keyword 7；关键词8 / fictional keyword 8；关键词9 / fictional keyword 9；关键词10 / fictional keyword 10；关键词11 / fictional keyword 11；关键词12 / fictional keyword 12；关键词13 / fictional keyword 13；关键词14 / fictional keyword 14；关键词15 / fictional keyword 15；关键词16 / fictional keyword 16；关键词17 / fictional keyword 17；关键词18 / fictional keyword 18；关键词19 / fictional keyword 19；关键词20 / fictional keyword 20；关键词21 / fictional keyword 21；关键词22 / fictional keyword 22；关键词23 / fictional keyword 23；关键词24 / fictional keyword 24；关键词25 / fictional keyword 25；关键词26 / fictional keyword 26；关键词27 / fictional keyword 27；关键词28 / fictional keyword 28；关键词29 / fictional keyword 29；关键词30 / fictional keyword 30；关键词31 / fictional keyword 31；关键词32 / fictional keyword 32；关键词33 / fictional keyword 33；关键词34 / fictional keyword 34；关键词35 / fictional keyword 35；关键词36 / fictional keyword 36；关键词37 / fictional keyword 37；关键词38 / fictional keyword 38；关键词39 / fictional keyword 39；关键词40 / fictional keyword 40；关键词41 / fictional keyword 41；关键词42 / fictional keyword 42；关键词43 / fictional keyword 43；关键词44 / fictional keyword 44；关键词45 / fictional keyword 45；关键词46 / fictional keyword 46；关键词47 / fictional keyword 47；关键词48 / fictional keyword 48；关键词49 / fictional keyword 49；关键词50 / fictional keyword 50；关键词51 / fictional keyword 51；关键词52 / fictional keyword 52；关键词53 / fictional keyword 53；关键词54 / fictional keyword 54；关键词55 / fictional keyword 55；关键词56 / fictional keyword 56；关键词57 / fictional keyword 57；关键词58 / fictional keyword 58；关键词59 / fictional keyword 59


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
