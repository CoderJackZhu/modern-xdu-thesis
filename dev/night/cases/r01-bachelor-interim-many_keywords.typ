// 全部内容为虚构测试
// 本科毕业设计（论文）中期报告示例
#import "../../../supporting/bachelor-forms.typ": bachelor-interim-documentclass

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
关键词：关键词0 / fictional keyword 0；关键词1 / fictional keyword 1；关键词2 / fictional keyword 2；关键词3 / fictional keyword 3；关键词4 / fictional keyword 4；关键词5 / fictional keyword 5；关键词6 / fictional keyword 6；关键词7 / fictional keyword 7；关键词8 / fictional keyword 8；关键词9 / fictional keyword 9；关键词10 / fictional keyword 10；关键词11 / fictional keyword 11；关键词12 / fictional keyword 12；关键词13 / fictional keyword 13；关键词14 / fictional keyword 14；关键词15 / fictional keyword 15；关键词16 / fictional keyword 16；关键词17 / fictional keyword 17；关键词18 / fictional keyword 18；关键词19 / fictional keyword 19；关键词20 / fictional keyword 20；关键词21 / fictional keyword 21；关键词22 / fictional keyword 22；关键词23 / fictional keyword 23；关键词24 / fictional keyword 24；关键词25 / fictional keyword 25；关键词26 / fictional keyword 26；关键词27 / fictional keyword 27；关键词28 / fictional keyword 28；关键词29 / fictional keyword 29；关键词30 / fictional keyword 30；关键词31 / fictional keyword 31；关键词32 / fictional keyword 32；关键词33 / fictional keyword 33；关键词34 / fictional keyword 34；关键词35 / fictional keyword 35；关键词36 / fictional keyword 36；关键词37 / fictional keyword 37；关键词38 / fictional keyword 38；关键词39 / fictional keyword 39；关键词40 / fictional keyword 40；关键词41 / fictional keyword 41；关键词42 / fictional keyword 42；关键词43 / fictional keyword 43；关键词44 / fictional keyword 44；关键词45 / fictional keyword 45；关键词46 / fictional keyword 46；关键词47 / fictional keyword 47；关键词48 / fictional keyword 48；关键词49 / fictional keyword 49；关键词50 / fictional keyword 50；关键词51 / fictional keyword 51；关键词52 / fictional keyword 52；关键词53 / fictional keyword 53；关键词54 / fictional keyword 54；关键词55 / fictional keyword 55；关键词56 / fictional keyword 56；关键词57 / fictional keyword 57；关键词58 / fictional keyword 58；关键词59 / fictional keyword 59


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
