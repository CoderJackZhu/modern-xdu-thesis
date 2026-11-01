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
#figure(rect(width: 35mm, height: 6mm), caption: [图题测试0]) <fig:many0>
#figure(table(columns: 2, [项目], [数值], [测试0], [1]), caption: [表题测试0]) <tab:many0>

#figure(rect(width: 35mm, height: 6mm), caption: [图题测试1]) <fig:many1>
#figure(table(columns: 2, [项目], [数值], [测试1], [1]), caption: [表题测试1]) <tab:many1>

#figure(rect(width: 35mm, height: 6mm), caption: [图题测试2]) <fig:many2>
#figure(table(columns: 2, [项目], [数值], [测试2], [1]), caption: [表题测试2]) <tab:many2>

#figure(rect(width: 35mm, height: 6mm), caption: [图题测试3]) <fig:many3>
#figure(table(columns: 2, [项目], [数值], [测试3], [1]), caption: [表题测试3]) <tab:many3>

#figure(rect(width: 35mm, height: 6mm), caption: [图题测试4]) <fig:many4>
#figure(table(columns: 2, [项目], [数值], [测试4], [1]), caption: [表题测试4]) <tab:many4>

#figure(rect(width: 35mm, height: 6mm), caption: [图题测试5]) <fig:many5>
#figure(table(columns: 2, [项目], [数值], [测试5], [1]), caption: [表题测试5]) <tab:many5>

#figure(rect(width: 35mm, height: 6mm), caption: [图题测试6]) <fig:many6>
#figure(table(columns: 2, [项目], [数值], [测试6], [1]), caption: [表题测试6]) <tab:many6>

#figure(rect(width: 35mm, height: 6mm), caption: [图题测试7]) <fig:many7>
#figure(table(columns: 2, [项目], [数值], [测试7], [1]), caption: [表题测试7]) <tab:many7>

#figure(rect(width: 35mm, height: 6mm), caption: [图题测试8]) <fig:many8>
#figure(table(columns: 2, [项目], [数值], [测试8], [1]), caption: [表题测试8]) <tab:many8>

#figure(rect(width: 35mm, height: 6mm), caption: [图题测试9]) <fig:many9>
#figure(table(columns: 2, [项目], [数值], [测试9], [1]), caption: [表题测试9]) <tab:many9>

#figure(rect(width: 35mm, height: 6mm), caption: [图题测试10]) <fig:many10>
#figure(table(columns: 2, [项目], [数值], [测试10], [1]), caption: [表题测试10]) <tab:many10>

#figure(rect(width: 35mm, height: 6mm), caption: [图题测试11]) <fig:many11>
#figure(table(columns: 2, [项目], [数值], [测试11], [1]), caption: [表题测试11]) <tab:many11>

#figure(rect(width: 35mm, height: 6mm), caption: [图题测试12]) <fig:many12>
#figure(table(columns: 2, [项目], [数值], [测试12], [1]), caption: [表题测试12]) <tab:many12>

#figure(rect(width: 35mm, height: 6mm), caption: [图题测试13]) <fig:many13>
#figure(table(columns: 2, [项目], [数值], [测试13], [1]), caption: [表题测试13]) <tab:many13>

#figure(rect(width: 35mm, height: 6mm), caption: [图题测试14]) <fig:many14>
#figure(table(columns: 2, [项目], [数值], [测试14], [1]), caption: [表题测试14]) <tab:many14>

#figure(rect(width: 35mm, height: 6mm), caption: [图题测试15]) <fig:many15>
#figure(table(columns: 2, [项目], [数值], [测试15], [1]), caption: [表题测试15]) <tab:many15>

#figure(rect(width: 35mm, height: 6mm), caption: [图题测试16]) <fig:many16>
#figure(table(columns: 2, [项目], [数值], [测试16], [1]), caption: [表题测试16]) <tab:many16>

#figure(rect(width: 35mm, height: 6mm), caption: [图题测试17]) <fig:many17>
#figure(table(columns: 2, [项目], [数值], [测试17], [1]), caption: [表题测试17]) <tab:many17>

#figure(rect(width: 35mm, height: 6mm), caption: [图题测试18]) <fig:many18>
#figure(table(columns: 2, [项目], [数值], [测试18], [1]), caption: [表题测试18]) <tab:many18>

#figure(rect(width: 35mm, height: 6mm), caption: [图题测试19]) <fig:many19>
#figure(table(columns: 2, [项目], [数值], [测试19], [1]), caption: [表题测试19]) <tab:many19>

#figure(rect(width: 35mm, height: 6mm), caption: [图题测试20]) <fig:many20>
#figure(table(columns: 2, [项目], [数值], [测试20], [1]), caption: [表题测试20]) <tab:many20>

#figure(rect(width: 35mm, height: 6mm), caption: [图题测试21]) <fig:many21>
#figure(table(columns: 2, [项目], [数值], [测试21], [1]), caption: [表题测试21]) <tab:many21>

#figure(rect(width: 35mm, height: 6mm), caption: [图题测试22]) <fig:many22>
#figure(table(columns: 2, [项目], [数值], [测试22], [1]), caption: [表题测试22]) <tab:many22>

#figure(rect(width: 35mm, height: 6mm), caption: [图题测试23]) <fig:many23>
#figure(table(columns: 2, [项目], [数值], [测试23], [1]), caption: [表题测试23]) <tab:many23>

#figure(rect(width: 35mm, height: 6mm), caption: [图题测试24]) <fig:many24>
#figure(table(columns: 2, [项目], [数值], [测试24], [1]), caption: [表题测试24]) <tab:many24>

#figure(rect(width: 35mm, height: 6mm), caption: [图题测试25]) <fig:many25>
#figure(table(columns: 2, [项目], [数值], [测试25], [1]), caption: [表题测试25]) <tab:many25>

#figure(rect(width: 35mm, height: 6mm), caption: [图题测试26]) <fig:many26>
#figure(table(columns: 2, [项目], [数值], [测试26], [1]), caption: [表题测试26]) <tab:many26>

#figure(rect(width: 35mm, height: 6mm), caption: [图题测试27]) <fig:many27>
#figure(table(columns: 2, [项目], [数值], [测试27], [1]), caption: [表题测试27]) <tab:many27>

#figure(rect(width: 35mm, height: 6mm), caption: [图题测试28]) <fig:many28>
#figure(table(columns: 2, [项目], [数值], [测试28], [1]), caption: [表题测试28]) <tab:many28>

#figure(rect(width: 35mm, height: 6mm), caption: [图题测试29]) <fig:many29>
#figure(table(columns: 2, [项目], [数值], [测试29], [1]), caption: [表题测试29]) <tab:many29>

#figure(rect(width: 35mm, height: 6mm), caption: [图题测试30]) <fig:many30>
#figure(table(columns: 2, [项目], [数值], [测试30], [1]), caption: [表题测试30]) <tab:many30>

#figure(rect(width: 35mm, height: 6mm), caption: [图题测试31]) <fig:many31>
#figure(table(columns: 2, [项目], [数值], [测试31], [1]), caption: [表题测试31]) <tab:many31>

#figure(rect(width: 35mm, height: 6mm), caption: [图题测试32]) <fig:many32>
#figure(table(columns: 2, [项目], [数值], [测试32], [1]), caption: [表题测试32]) <tab:many32>

#figure(rect(width: 35mm, height: 6mm), caption: [图题测试33]) <fig:many33>
#figure(table(columns: 2, [项目], [数值], [测试33], [1]), caption: [表题测试33]) <tab:many33>

#figure(rect(width: 35mm, height: 6mm), caption: [图题测试34]) <fig:many34>
#figure(table(columns: 2, [项目], [数值], [测试34], [1]), caption: [表题测试34]) <tab:many34>

#figure(rect(width: 35mm, height: 6mm), caption: [图题测试35]) <fig:many35>
#figure(table(columns: 2, [项目], [数值], [测试35], [1]), caption: [表题测试35]) <tab:many35>

#figure(rect(width: 35mm, height: 6mm), caption: [图题测试36]) <fig:many36>
#figure(table(columns: 2, [项目], [数值], [测试36], [1]), caption: [表题测试36]) <tab:many36>

#figure(rect(width: 35mm, height: 6mm), caption: [图题测试37]) <fig:many37>
#figure(table(columns: 2, [项目], [数值], [测试37], [1]), caption: [表题测试37]) <tab:many37>

#figure(rect(width: 35mm, height: 6mm), caption: [图题测试38]) <fig:many38>
#figure(table(columns: 2, [项目], [数值], [测试38], [1]), caption: [表题测试38]) <tab:many38>

#figure(rect(width: 35mm, height: 6mm), caption: [图题测试39]) <fig:many39>
#figure(table(columns: 2, [项目], [数值], [测试39], [1]), caption: [表题测试39]) <tab:many39>

#figure(rect(width: 35mm, height: 6mm), caption: [图题测试40]) <fig:many40>
#figure(table(columns: 2, [项目], [数值], [测试40], [1]), caption: [表题测试40]) <tab:many40>

#figure(rect(width: 35mm, height: 6mm), caption: [图题测试41]) <fig:many41>
#figure(table(columns: 2, [项目], [数值], [测试41], [1]), caption: [表题测试41]) <tab:many41>

#figure(rect(width: 35mm, height: 6mm), caption: [图题测试42]) <fig:many42>
#figure(table(columns: 2, [项目], [数值], [测试42], [1]), caption: [表题测试42]) <tab:many42>

#figure(rect(width: 35mm, height: 6mm), caption: [图题测试43]) <fig:many43>
#figure(table(columns: 2, [项目], [数值], [测试43], [1]), caption: [表题测试43]) <tab:many43>

#figure(rect(width: 35mm, height: 6mm), caption: [图题测试44]) <fig:many44>
#figure(table(columns: 2, [项目], [数值], [测试44], [1]), caption: [表题测试44]) <tab:many44>

#figure(rect(width: 35mm, height: 6mm), caption: [图题测试45]) <fig:many45>
#figure(table(columns: 2, [项目], [数值], [测试45], [1]), caption: [表题测试45]) <tab:many45>

#figure(rect(width: 35mm, height: 6mm), caption: [图题测试46]) <fig:many46>
#figure(table(columns: 2, [项目], [数值], [测试46], [1]), caption: [表题测试46]) <tab:many46>

#figure(rect(width: 35mm, height: 6mm), caption: [图题测试47]) <fig:many47>
#figure(table(columns: 2, [项目], [数值], [测试47], [1]), caption: [表题测试47]) <tab:many47>

#figure(rect(width: 35mm, height: 6mm), caption: [图题测试48]) <fig:many48>
#figure(table(columns: 2, [项目], [数值], [测试48], [1]), caption: [表题测试48]) <tab:many48>

#figure(rect(width: 35mm, height: 6mm), caption: [图题测试49]) <fig:many49>
#figure(table(columns: 2, [项目], [数值], [测试49], [1]), caption: [表题测试49]) <tab:many49>

#figure(rect(width: 35mm, height: 6mm), caption: [图题测试50]) <fig:many50>
#figure(table(columns: 2, [项目], [数值], [测试50], [1]), caption: [表题测试50]) <tab:many50>

#figure(rect(width: 35mm, height: 6mm), caption: [图题测试51]) <fig:many51>
#figure(table(columns: 2, [项目], [数值], [测试51], [1]), caption: [表题测试51]) <tab:many51>

#figure(rect(width: 35mm, height: 6mm), caption: [图题测试52]) <fig:many52>
#figure(table(columns: 2, [项目], [数值], [测试52], [1]), caption: [表题测试52]) <tab:many52>

#figure(rect(width: 35mm, height: 6mm), caption: [图题测试53]) <fig:many53>
#figure(table(columns: 2, [项目], [数值], [测试53], [1]), caption: [表题测试53]) <tab:many53>

#figure(rect(width: 35mm, height: 6mm), caption: [图题测试54]) <fig:many54>
#figure(table(columns: 2, [项目], [数值], [测试54], [1]), caption: [表题测试54]) <tab:many54>

#figure(rect(width: 35mm, height: 6mm), caption: [图题测试55]) <fig:many55>
#figure(table(columns: 2, [项目], [数值], [测试55], [1]), caption: [表题测试55]) <tab:many55>

#figure(rect(width: 35mm, height: 6mm), caption: [图题测试56]) <fig:many56>
#figure(table(columns: 2, [项目], [数值], [测试56], [1]), caption: [表题测试56]) <tab:many56>

#figure(rect(width: 35mm, height: 6mm), caption: [图题测试57]) <fig:many57>
#figure(table(columns: 2, [项目], [数值], [测试57], [1]), caption: [表题测试57]) <tab:many57>

#figure(rect(width: 35mm, height: 6mm), caption: [图题测试58]) <fig:many58>
#figure(table(columns: 2, [项目], [数值], [测试58], [1]), caption: [表题测试58]) <tab:many58>

#figure(rect(width: 35mm, height: 6mm), caption: [图题测试59]) <fig:many59>
#figure(table(columns: 2, [项目], [数值], [测试59], [1]), caption: [表题测试59]) <tab:many59>

#figure(rect(width: 35mm, height: 6mm), caption: [图题测试60]) <fig:many60>
#figure(table(columns: 2, [项目], [数值], [测试60], [1]), caption: [表题测试60]) <tab:many60>

#figure(rect(width: 35mm, height: 6mm), caption: [图题测试61]) <fig:many61>
#figure(table(columns: 2, [项目], [数值], [测试61], [1]), caption: [表题测试61]) <tab:many61>

#figure(rect(width: 35mm, height: 6mm), caption: [图题测试62]) <fig:many62>
#figure(table(columns: 2, [项目], [数值], [测试62], [1]), caption: [表题测试62]) <tab:many62>

#figure(rect(width: 35mm, height: 6mm), caption: [图题测试63]) <fig:many63>
#figure(table(columns: 2, [项目], [数值], [测试63], [1]), caption: [表题测试63]) <tab:many63>

#figure(rect(width: 35mm, height: 6mm), caption: [图题测试64]) <fig:many64>
#figure(table(columns: 2, [项目], [数值], [测试64], [1]), caption: [表题测试64]) <tab:many64>

#figure(rect(width: 35mm, height: 6mm), caption: [图题测试65]) <fig:many65>
#figure(table(columns: 2, [项目], [数值], [测试65], [1]), caption: [表题测试65]) <tab:many65>

#figure(rect(width: 35mm, height: 6mm), caption: [图题测试66]) <fig:many66>
#figure(table(columns: 2, [项目], [数值], [测试66], [1]), caption: [表题测试66]) <tab:many66>

#figure(rect(width: 35mm, height: 6mm), caption: [图题测试67]) <fig:many67>
#figure(table(columns: 2, [项目], [数值], [测试67], [1]), caption: [表题测试67]) <tab:many67>

#figure(rect(width: 35mm, height: 6mm), caption: [图题测试68]) <fig:many68>
#figure(table(columns: 2, [项目], [数值], [测试68], [1]), caption: [表题测试68]) <tab:many68>

#figure(rect(width: 35mm, height: 6mm), caption: [图题测试69]) <fig:many69>
#figure(table(columns: 2, [项目], [数值], [测试69], [1]), caption: [表题测试69]) <tab:many69>


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
