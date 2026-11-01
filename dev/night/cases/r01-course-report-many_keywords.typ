// 全部内容为虚构测试
// 通用课程实验报告示例（非学校统一行政表，教师有指定模板时以教师模板为准）
#import "../../../supporting/course-report.typ": course-report-documentclass

#let (doc, report) = course-report-documentclass(
  info: (
    course: "数据结构与算法",
    title: "基于哈希表的词频统计实验",
    author: "张三",
    student-id: "2026000001",
    department: "电子工程学院 / 电子信息工程",
    instructor: "李四",
    date: "2026 年 10 月",
  ),
)

#show: doc

#report(
  sections: (
    ("实验目的", [
      理解哈希表的基本原理，掌握冲突处理方法，并使用实际文本数据比较不同实现的性能。
    ]),
    ("实验环境", [
      操作系统：macOS；编译器：Clang；语言：C++20；输入数据：约 10 MB 的虚构文本。
    ]),
    ("实验原理", [
关键词：关键词0 / fictional keyword 0；关键词1 / fictional keyword 1；关键词2 / fictional keyword 2；关键词3 / fictional keyword 3；关键词4 / fictional keyword 4；关键词5 / fictional keyword 5；关键词6 / fictional keyword 6；关键词7 / fictional keyword 7；关键词8 / fictional keyword 8；关键词9 / fictional keyword 9；关键词10 / fictional keyword 10；关键词11 / fictional keyword 11；关键词12 / fictional keyword 12；关键词13 / fictional keyword 13；关键词14 / fictional keyword 14；关键词15 / fictional keyword 15；关键词16 / fictional keyword 16；关键词17 / fictional keyword 17；关键词18 / fictional keyword 18；关键词19 / fictional keyword 19；关键词20 / fictional keyword 20；关键词21 / fictional keyword 21；关键词22 / fictional keyword 22；关键词23 / fictional keyword 23；关键词24 / fictional keyword 24；关键词25 / fictional keyword 25；关键词26 / fictional keyword 26；关键词27 / fictional keyword 27；关键词28 / fictional keyword 28；关键词29 / fictional keyword 29；关键词30 / fictional keyword 30；关键词31 / fictional keyword 31；关键词32 / fictional keyword 32；关键词33 / fictional keyword 33；关键词34 / fictional keyword 34；关键词35 / fictional keyword 35；关键词36 / fictional keyword 36；关键词37 / fictional keyword 37；关键词38 / fictional keyword 38；关键词39 / fictional keyword 39；关键词40 / fictional keyword 40；关键词41 / fictional keyword 41；关键词42 / fictional keyword 42；关键词43 / fictional keyword 43；关键词44 / fictional keyword 44；关键词45 / fictional keyword 45；关键词46 / fictional keyword 46；关键词47 / fictional keyword 47；关键词48 / fictional keyword 48；关键词49 / fictional keyword 49；关键词50 / fictional keyword 50；关键词51 / fictional keyword 51；关键词52 / fictional keyword 52；关键词53 / fictional keyword 53；关键词54 / fictional keyword 54；关键词55 / fictional keyword 55；关键词56 / fictional keyword 56；关键词57 / fictional keyword 57；关键词58 / fictional keyword 58；关键词59 / fictional keyword 59


      使用哈希函数将词项映射到桶中，采用链地址法处理冲突。统计每个词项出现次数，
      最后按频次排序输出。实验比较不同桶数量对平均查找长度的影响。
    ]),
    ("实验步骤", [
      1. 读取文本并完成分词和大小写归一化。#linebreak()
      2. 构建哈希表并记录冲突次数。#linebreak()
      3. 重复运行不同桶数量下的实验。#linebreak()
      4. 汇总运行时间、平均查找长度和最频繁词项。
    ]),
    ("实验结果", [
      在示例数据上，桶数量增加后平均查找长度下降，但内存占用和初始化时间上升。
      具体数值应替换为真实实验记录。
    ]),
    ("分析与结论", [
      哈希表在词频统计任务中具有较好的平均性能，参数选择需要同时考虑时间和空间成本。
      后续可比较开放寻址法和不同哈希函数的影响。
    ]),
  ),
  summary: [提交前请替换虚构数据，附上源程序、原始记录和教师要求的其他材料。],
)
