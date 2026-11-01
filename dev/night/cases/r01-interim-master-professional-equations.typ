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
$ y_0 &= a x + b \ z_0 &= c x + d $ <eq:multi0>

式 @eq:multi0。

本段研究虚构系统的性能与验证方法，说明实验条件、数据来源和适用边界。所有人物、数据与成果均为虚构，不包含真实论文内容。

$ y_1 &= a x + b \ z_1 &= c x + d $ <eq:multi1>

式 @eq:multi1。

本段研究虚构系统的性能与验证方法，说明实验条件、数据来源和适用边界。所有人物、数据与成果均为虚构，不包含真实论文内容。

$ y_2 &= a x + b \ z_2 &= c x + d $ <eq:multi2>

式 @eq:multi2。

本段研究虚构系统的性能与验证方法，说明实验条件、数据来源和适用边界。所有人物、数据与成果均为虚构，不包含真实论文内容。

$ y_3 &= a x + b \ z_3 &= c x + d $ <eq:multi3>

式 @eq:multi3。

本段研究虚构系统的性能与验证方法，说明实验条件、数据来源和适用边界。所有人物、数据与成果均为虚构，不包含真实论文内容。

$ y_4 &= a x + b \ z_4 &= c x + d $ <eq:multi4>

式 @eq:multi4。

本段研究虚构系统的性能与验证方法，说明实验条件、数据来源和适用边界。所有人物、数据与成果均为虚构，不包含真实论文内容。

$ y_5 &= a x + b \ z_5 &= c x + d $ <eq:multi5>

式 @eq:multi5。

本段研究虚构系统的性能与验证方法，说明实验条件、数据来源和适用边界。所有人物、数据与成果均为虚构，不包含真实论文内容。

$ y_6 &= a x + b \ z_6 &= c x + d $ <eq:multi6>

式 @eq:multi6。

本段研究虚构系统的性能与验证方法，说明实验条件、数据来源和适用边界。所有人物、数据与成果均为虚构，不包含真实论文内容。

$ y_7 &= a x + b \ z_7 &= c x + d $ <eq:multi7>

式 @eq:multi7。

本段研究虚构系统的性能与验证方法，说明实验条件、数据来源和适用边界。所有人物、数据与成果均为虚构，不包含真实论文内容。

$ y_8 &= a x + b \ z_8 &= c x + d $ <eq:multi8>

式 @eq:multi8。

本段研究虚构系统的性能与验证方法，说明实验条件、数据来源和适用边界。所有人物、数据与成果均为虚构，不包含真实论文内容。

$ y_9 &= a x + b \ z_9 &= c x + d $ <eq:multi9>

式 @eq:multi9。

本段研究虚构系统的性能与验证方法，说明实验条件、数据来源和适用边界。所有人物、数据与成果均为虚构，不包含真实论文内容。

$ y_10 &= a x + b \ z_10 &= c x + d $ <eq:multi10>

式 @eq:multi10。

本段研究虚构系统的性能与验证方法，说明实验条件、数据来源和适用边界。所有人物、数据与成果均为虚构，不包含真实论文内容。

$ y_11 &= a x + b \ z_11 &= c x + d $ <eq:multi11>

式 @eq:multi11。

本段研究虚构系统的性能与验证方法，说明实验条件、数据来源和适用边界。所有人物、数据与成果均为虚构，不包含真实论文内容。


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
