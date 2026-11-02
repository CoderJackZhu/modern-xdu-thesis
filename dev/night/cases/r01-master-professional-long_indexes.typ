// 虚构测试：master-professional/long_indexes，变体0
#import "../../../lib.typ": documentclass
#let t = documentclass(degree: "professional", blind: false, info: (
  title: ("虚构系统验证研究",),
  title-en: ("Fictional System Verification",),
  author: "测试作者",
  author-en: "Fictional Author",
  department: "电子工程学院",
  major: "电子信息工程",
  student-id: "202600001",
  discipline: "电子科学与技术",
  subdiscipline: "电路与系统",
  supervisor: ("测试导师", "教授"),
  supervisor-en: ("Fictional Advisor", "Professor"),
  abstract: [本段研究虚构系统的性能与验证方法，说明实验条件、数据来源和适用边界。所有人物、数据与成果均为虚构，不包含真实论文内容。

本段研究虚构系统的性能与验证方法，说明实验条件、数据来源和适用边界。所有人物、数据与成果均为虚构，不包含真实论文内容。

本段研究虚构系统的性能与验证方法，说明实验条件、数据来源和适用边界。所有人物、数据与成果均为虚构，不包含真实论文内容。

本段研究虚构系统的性能与验证方法，说明实验条件、数据来源和适用边界。所有人物、数据与成果均为虚构，不包含真实论文内容。],
  abstract-en: [This fictional experiment studies reliable modeling under controlled conditions. All names and results are synthetic and the assumptions are explicitly stated. This fictional experiment studies reliable modeling under controlled conditions. All names and results are synthetic and the assumptions are explicitly stated. This fictional experiment studies reliable modeling under controlled conditions. All names and results are synthetic and the assumptions are explicitly stated. This fictional experiment studies reliable modeling under controlled conditions. All names and results are synthetic and the assumptions are explicitly stated. This fictional experiment studies reliable modeling under controlled conditions. All names and results are synthetic and the assumptions are explicitly stated. ],
  acknowledgement: [本段研究虚构系统的性能与验证方法，说明实验条件、数据来源和适用边界。所有人物、数据与成果均为虚构，不包含真实论文内容。],
  notation: (("S0", "符号名称0及其解释"),("S1", "符号名称1及其解释"),("S2", "符号名称2及其解释"),("S3", "符号名称3及其解释"),("S4", "符号名称4及其解释"),("S5", "符号名称5及其解释"),("S6", "符号名称6及其解释"),("S7", "符号名称7及其解释"),("S8", "符号名称8及其解释"),("S9", "符号名称9及其解释"),("S10", "符号名称10及其解释"),("S11", "符号名称11及其解释"),("S12", "符号名称12及其解释"),("S13", "符号名称13及其解释"),("S14", "符号名称14及其解释"),("S15", "符号名称15及其解释"),("S16", "符号名称16及其解释"),("S17", "符号名称17及其解释"),("S18", "符号名称18及其解释"),("S19", "符号名称19及其解释"),("S20", "符号名称20及其解释"),("S21", "符号名称21及其解释"),("S22", "符号名称22及其解释"),("S23", "符号名称23及其解释"),("S24", "符号名称24及其解释"),("S25", "符号名称25及其解释"),("S26", "符号名称26及其解释"),("S27", "符号名称27及其解释"),("S28", "符号名称28及其解释"),("S29", "符号名称29及其解释"),("S30", "符号名称30及其解释"),("S31", "符号名称31及其解释"),("S32", "符号名称32及其解释"),("S33", "符号名称33及其解释"),("S34", "符号名称34及其解释"),("S35", "符号名称35及其解释"),("S36", "符号名称36及其解释"),("S37", "符号名称37及其解释"),("S38", "符号名称38及其解释"),("S39", "符号名称39及其解释"),("S40", "符号名称40及其解释"),("S41", "符号名称41及其解释"),("S42", "符号名称42及其解释"),("S43", "符号名称43及其解释"),("S44", "符号名称44及其解释"),("S45", "符号名称45及其解释"),("S46", "符号名称46及其解释"),("S47", "符号名称47及其解释"),("S48", "符号名称48及其解释"),("S49", "符号名称49及其解释"),("S50", "符号名称50及其解释"),("S51", "符号名称51及其解释"),("S52", "符号名称52及其解释"),("S53", "符号名称53及其解释"),("S54", "符号名称54及其解释"),("S55", "符号名称55及其解释"),("S56", "符号名称56及其解释"),("S57", "符号名称57及其解释"),("S58", "符号名称58及其解释"),("S59", "符号名称59及其解释"),("S60", "符号名称60及其解释"),("S61", "符号名称61及其解释"),("S62", "符号名称62及其解释"),("S63", "符号名称63及其解释"),("S64", "符号名称64及其解释"),("S65", "符号名称65及其解释"),("S66", "符号名称66及其解释"),("S67", "符号名称67及其解释"),("S68", "符号名称68及其解释"),("S69", "符号名称69及其解释"),("S70", "符号名称70及其解释"),("S71", "符号名称71及其解释"),("S72", "符号名称72及其解释"),("S73", "符号名称73及其解释"),("S74", "符号名称74及其解释"),("S75", "符号名称75及其解释"),("S76", "符号名称76及其解释"),("S77", "符号名称77及其解释"),("S78", "符号名称78及其解释"),("S79", "符号名称79及其解释"),("S80", "符号名称80及其解释"),("S81", "符号名称81及其解释"),("S82", "符号名称82及其解释"),("S83", "符号名称83及其解释"),("S84", "符号名称84及其解释"),("S85", "符号名称85及其解释"),("S86", "符号名称86及其解释"),("S87", "符号名称87及其解释"),("S88", "符号名称88及其解释"),("S89", "符号名称89及其解释"),("S90", "符号名称90及其解释"),("S91", "符号名称91及其解释"),("S92", "符号名称92及其解释"),("S93", "符号名称93及其解释"),("S94", "符号名称94及其解释"),("S95", "符号名称95及其解释"),("S96", "符号名称96及其解释"),("S97", "符号名称97及其解释"),("S98", "符号名称98及其解释"),("S99", "符号名称99及其解释"),("S100", "符号名称100及其解释"),("S101", "符号名称101及其解释"),("S102", "符号名称102及其解释"),("S103", "符号名称103及其解释"),("S104", "符号名称104及其解释"),("S105", "符号名称105及其解释"),("S106", "符号名称106及其解释"),("S107", "符号名称107及其解释"),("S108", "符号名称108及其解释"),("S109", "符号名称109及其解释"),("S110", "符号名称110及其解释"),("S111", "符号名称111及其解释"),("S112", "符号名称112及其解释"),("S113", "符号名称113及其解释"),("S114", "符号名称114及其解释"),("S115", "符号名称115及其解释"),("S116", "符号名称116及其解释"),("S117", "符号名称117及其解释"),("S118", "符号名称118及其解释"),("S119", "符号名称119及其解释"),("S120", "符号名称120及其解释"),("S121", "符号名称121及其解释"),("S122", "符号名称122及其解释"),("S123", "符号名称123及其解释"),("S124", "符号名称124及其解释"),("S125", "符号名称125及其解释"),("S126", "符号名称126及其解释"),("S127", "符号名称127及其解释"),("S128", "符号名称128及其解释"),("S129", "符号名称129及其解释"),("S130", "符号名称130及其解释"),("S131", "符号名称131及其解释"),("S132", "符号名称132及其解释"),("S133", "符号名称133及其解释"),("S134", "符号名称134及其解释"),("S135", "符号名称135及其解释"),("S136", "符号名称136及其解释"),("S137", "符号名称137及其解释"),("S138", "符号名称138及其解释"),("S139", "符号名称139及其解释"),),
  abbreviations: (("ABC000", "Fictional Long English Term 0", "缩略语解释0"),("ABC001", "Fictional Long English Term 1", "缩略语解释1"),("ABC002", "Fictional Long English Term 2", "缩略语解释2"),("ABC003", "Fictional Long English Term 3", "缩略语解释3"),("ABC004", "Fictional Long English Term 4", "缩略语解释4"),("ABC005", "Fictional Long English Term 5", "缩略语解释5"),("ABC006", "Fictional Long English Term 6", "缩略语解释6"),("ABC007", "Fictional Long English Term 7", "缩略语解释7"),("ABC008", "Fictional Long English Term 8", "缩略语解释8"),("ABC009", "Fictional Long English Term 9", "缩略语解释9"),("ABC010", "Fictional Long English Term 10", "缩略语解释10"),("ABC011", "Fictional Long English Term 11", "缩略语解释11"),("ABC012", "Fictional Long English Term 12", "缩略语解释12"),("ABC013", "Fictional Long English Term 13", "缩略语解释13"),("ABC014", "Fictional Long English Term 14", "缩略语解释14"),("ABC015", "Fictional Long English Term 15", "缩略语解释15"),("ABC016", "Fictional Long English Term 16", "缩略语解释16"),("ABC017", "Fictional Long English Term 17", "缩略语解释17"),("ABC018", "Fictional Long English Term 18", "缩略语解释18"),("ABC019", "Fictional Long English Term 19", "缩略语解释19"),("ABC020", "Fictional Long English Term 20", "缩略语解释20"),("ABC021", "Fictional Long English Term 21", "缩略语解释21"),("ABC022", "Fictional Long English Term 22", "缩略语解释22"),("ABC023", "Fictional Long English Term 23", "缩略语解释23"),("ABC024", "Fictional Long English Term 24", "缩略语解释24"),("ABC025", "Fictional Long English Term 25", "缩略语解释25"),("ABC026", "Fictional Long English Term 26", "缩略语解释26"),("ABC027", "Fictional Long English Term 27", "缩略语解释27"),("ABC028", "Fictional Long English Term 28", "缩略语解释28"),("ABC029", "Fictional Long English Term 29", "缩略语解释29"),("ABC030", "Fictional Long English Term 30", "缩略语解释30"),("ABC031", "Fictional Long English Term 31", "缩略语解释31"),("ABC032", "Fictional Long English Term 32", "缩略语解释32"),("ABC033", "Fictional Long English Term 33", "缩略语解释33"),("ABC034", "Fictional Long English Term 34", "缩略语解释34"),("ABC035", "Fictional Long English Term 35", "缩略语解释35"),("ABC036", "Fictional Long English Term 36", "缩略语解释36"),("ABC037", "Fictional Long English Term 37", "缩略语解释37"),("ABC038", "Fictional Long English Term 38", "缩略语解释38"),("ABC039", "Fictional Long English Term 39", "缩略语解释39"),("ABC040", "Fictional Long English Term 40", "缩略语解释40"),("ABC041", "Fictional Long English Term 41", "缩略语解释41"),("ABC042", "Fictional Long English Term 42", "缩略语解释42"),("ABC043", "Fictional Long English Term 43", "缩略语解释43"),("ABC044", "Fictional Long English Term 44", "缩略语解释44"),("ABC045", "Fictional Long English Term 45", "缩略语解释45"),("ABC046", "Fictional Long English Term 46", "缩略语解释46"),("ABC047", "Fictional Long English Term 47", "缩略语解释47"),("ABC048", "Fictional Long English Term 48", "缩略语解释48"),("ABC049", "Fictional Long English Term 49", "缩略语解释49"),("ABC050", "Fictional Long English Term 50", "缩略语解释50"),("ABC051", "Fictional Long English Term 51", "缩略语解释51"),("ABC052", "Fictional Long English Term 52", "缩略语解释52"),("ABC053", "Fictional Long English Term 53", "缩略语解释53"),("ABC054", "Fictional Long English Term 54", "缩略语解释54"),("ABC055", "Fictional Long English Term 55", "缩略语解释55"),("ABC056", "Fictional Long English Term 56", "缩略语解释56"),("ABC057", "Fictional Long English Term 57", "缩略语解释57"),("ABC058", "Fictional Long English Term 58", "缩略语解释58"),("ABC059", "Fictional Long English Term 59", "缩略语解释59"),("ABC060", "Fictional Long English Term 60", "缩略语解释60"),("ABC061", "Fictional Long English Term 61", "缩略语解释61"),("ABC062", "Fictional Long English Term 62", "缩略语解释62"),("ABC063", "Fictional Long English Term 63", "缩略语解释63"),("ABC064", "Fictional Long English Term 64", "缩略语解释64"),("ABC065", "Fictional Long English Term 65", "缩略语解释65"),("ABC066", "Fictional Long English Term 66", "缩略语解释66"),("ABC067", "Fictional Long English Term 67", "缩略语解释67"),("ABC068", "Fictional Long English Term 68", "缩略语解释68"),("ABC069", "Fictional Long English Term 69", "缩略语解释69"),("ABC070", "Fictional Long English Term 70", "缩略语解释70"),("ABC071", "Fictional Long English Term 71", "缩略语解释71"),("ABC072", "Fictional Long English Term 72", "缩略语解释72"),("ABC073", "Fictional Long English Term 73", "缩略语解释73"),("ABC074", "Fictional Long English Term 74", "缩略语解释74"),("ABC075", "Fictional Long English Term 75", "缩略语解释75"),("ABC076", "Fictional Long English Term 76", "缩略语解释76"),("ABC077", "Fictional Long English Term 77", "缩略语解释77"),("ABC078", "Fictional Long English Term 78", "缩略语解释78"),("ABC079", "Fictional Long English Term 79", "缩略语解释79"),("ABC080", "Fictional Long English Term 80", "缩略语解释80"),("ABC081", "Fictional Long English Term 81", "缩略语解释81"),("ABC082", "Fictional Long English Term 82", "缩略语解释82"),("ABC083", "Fictional Long English Term 83", "缩略语解释83"),("ABC084", "Fictional Long English Term 84", "缩略语解释84"),("ABC085", "Fictional Long English Term 85", "缩略语解释85"),("ABC086", "Fictional Long English Term 86", "缩略语解释86"),("ABC087", "Fictional Long English Term 87", "缩略语解释87"),("ABC088", "Fictional Long English Term 88", "缩略语解释88"),("ABC089", "Fictional Long English Term 89", "缩略语解释89"),("ABC090", "Fictional Long English Term 90", "缩略语解释90"),("ABC091", "Fictional Long English Term 91", "缩略语解释91"),("ABC092", "Fictional Long English Term 92", "缩略语解释92"),("ABC093", "Fictional Long English Term 93", "缩略语解释93"),("ABC094", "Fictional Long English Term 94", "缩略语解释94"),("ABC095", "Fictional Long English Term 95", "缩略语解释95"),("ABC096", "Fictional Long English Term 96", "缩略语解释96"),("ABC097", "Fictional Long English Term 97", "缩略语解释97"),("ABC098", "Fictional Long English Term 98", "缩略语解释98"),("ABC099", "Fictional Long English Term 99", "缩略语解释99"),("ABC100", "Fictional Long English Term 100", "缩略语解释100"),("ABC101", "Fictional Long English Term 101", "缩略语解释101"),("ABC102", "Fictional Long English Term 102", "缩略语解释102"),("ABC103", "Fictional Long English Term 103", "缩略语解释103"),("ABC104", "Fictional Long English Term 104", "缩略语解释104"),("ABC105", "Fictional Long English Term 105", "缩略语解释105"),("ABC106", "Fictional Long English Term 106", "缩略语解释106"),("ABC107", "Fictional Long English Term 107", "缩略语解释107"),("ABC108", "Fictional Long English Term 108", "缩略语解释108"),("ABC109", "Fictional Long English Term 109", "缩略语解释109"),("ABC110", "Fictional Long English Term 110", "缩略语解释110"),("ABC111", "Fictional Long English Term 111", "缩略语解释111"),("ABC112", "Fictional Long English Term 112", "缩略语解释112"),("ABC113", "Fictional Long English Term 113", "缩略语解释113"),("ABC114", "Fictional Long English Term 114", "缩略语解释114"),("ABC115", "Fictional Long English Term 115", "缩略语解释115"),("ABC116", "Fictional Long English Term 116", "缩略语解释116"),("ABC117", "Fictional Long English Term 117", "缩略语解释117"),("ABC118", "Fictional Long English Term 118", "缩略语解释118"),("ABC119", "Fictional Long English Term 119", "缩略语解释119"),("ABC120", "Fictional Long English Term 120", "缩略语解释120"),("ABC121", "Fictional Long English Term 121", "缩略语解释121"),("ABC122", "Fictional Long English Term 122", "缩略语解释122"),("ABC123", "Fictional Long English Term 123", "缩略语解释123"),("ABC124", "Fictional Long English Term 124", "缩略语解释124"),("ABC125", "Fictional Long English Term 125", "缩略语解释125"),("ABC126", "Fictional Long English Term 126", "缩略语解释126"),("ABC127", "Fictional Long English Term 127", "缩略语解释127"),("ABC128", "Fictional Long English Term 128", "缩略语解释128"),("ABC129", "Fictional Long English Term 129", "缩略语解释129"),("ABC130", "Fictional Long English Term 130", "缩略语解释130"),("ABC131", "Fictional Long English Term 131", "缩略语解释131"),("ABC132", "Fictional Long English Term 132", "缩略语解释132"),("ABC133", "Fictional Long English Term 133", "缩略语解释133"),("ABC134", "Fictional Long English Term 134", "缩略语解释134"),("ABC135", "Fictional Long English Term 135", "缩略语解释135"),("ABC136", "Fictional Long English Term 136", "缩略语解释136"),("ABC137", "Fictional Long English Term 137", "缩略语解释137"),("ABC138", "Fictional Long English Term 138", "缩略语解释138"),("ABC139", "Fictional Long English Term 139", "缩略语解释139"),),
))
#show: t.doc
#(t.cover)()
#pagebreak(to: "odd")
#(t.title-cn)()
#pagebreak(to: "odd")
#(t.title-en)()
#pagebreak(to: "odd")
#(t.declaration)()
#pagebreak(to: "odd")
#counter(page).update(1)
#(t.abstract)()
#pagebreak(to: "odd")
#(t.abstract-en)()
#pagebreak(to: "odd")
#(t.list-of-figures)()
#pagebreak(to: "odd")
#(t.list-of-tables)()
#pagebreak(to: "odd")
#(t.notation)()
#pagebreak(to: "odd")
#(t.abbreviations)()
#pagebreak(to: "odd")
#(t.outline-page)()
#show: t.mainmatter

= 第一章 测试绪论 <head:one>

本段研究虚构系统的性能与验证方法，说明实验条件、数据来源和适用边界。所有人物、数据与成果均为虚构，不包含真实论文内容。

本段研究虚构系统的性能与验证方法，说明实验条件、数据来源和适用边界。所有人物、数据与成果均为虚构，不包含真实论文内容。

本段研究虚构系统的性能与验证方法，说明实验条件、数据来源和适用边界。所有人物、数据与成果均为虚构，不包含真实论文内容。

本段研究虚构系统的性能与验证方法，说明实验条件、数据来源和适用边界。所有人物、数据与成果均为虚构，不包含真实论文内容。

#figure(rect(width: 35mm, height: 6mm), caption: [图题测试0]) <fig:many0>
#figure(table(columns: 2, [项目], [数值], [测试0], [1]), caption: [表题测试0]) <tab:many0>

#figure(rect(width: 35mm, height: 6mm), caption: [图题测试1]) <fig:many1>
#figure(table(columns: 2, [项目], [数值], [测试1], [1]), caption: [表题测试1]) <tab:many1>

#figure(rect(width: 35mm, height: 6mm), caption: [图题测试2]) <fig:many2>
#figure(table(columns: 2, [项目], [数值], [测试2], [1]), caption: [表题测试2]) <tab:many2>

#figure(rect(width: 35mm, height: 6mm), caption: [图题测试3]) <fig:many3>
#figure(table(columns: 2, [项目], [数值], [测试3], [1]), caption: [表题测试3]) <tab:many3>

= 第二章 图表公式

本段研究虚构系统的性能与验证方法，说明实验条件、数据来源和适用边界。所有人物、数据与成果均为虚构，不包含真实论文内容。

#figure(rect(width: 45mm, height: 12mm), caption: [系统框图]) <fig:model>
#figure(table(columns: 2, [参数], [数值], [实验], [1]), caption: [参数设置]) <tab:model>
$ y = a x + b $ <eq:model>
图 @fig:model、表 @tab:model、式 @eq:model；见 @head:one。

#pagebreak(to: "odd")
#(t.references)(entries: ())
#pagebreak(to: "odd")
#(t.acknowledgement)()
#pagebreak(to: "odd")
#(t.bio)()
