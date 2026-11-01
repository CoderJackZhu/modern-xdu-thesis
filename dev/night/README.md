# 用户写法压测

基准与停止条件见 `triage.json`；结果见 `summary.json`；仓库外报告路径记在该JSON中。本目录所有人物、正文、文献与成果均为虚构。

## 重跑

在独立worktree根目录执行（需要Typst 0.15.1、系统python3及PyMuPDF）：

```sh
python3 dev/night/test_checks.py
python3 dev/night/gen.py --round 1
python3 dev/night/run.py --round 1
python3 dev/night/gen.py --round 2
python3 dev/night/run.py --round 2
python3 dev/night/gen.py --round 3
python3 dev/night/run.py --round 3
python3 dev/night/measure_repros.py
python3 dev/night/measure_coverage.py
```

`run.py`自动在忽略的`out/packages`中为已有的doctor入口创建本次进程专用包路径，并设置`TYPST_PACKAGE_PATH`，不会改变全局包软链。所有测试文件的直接import都是指向本worktree的相对路径。不要运行worktree内的`dev/pkg-stage.sh`。

`--recheck`对现有PDF重跑通用检查，不重新编译。`--only`筛选名称，并把结果合并回同轮完整记录；校准重复编译不增加唯一场景数量。官方页面读取可运行`python3 dev/night/official.py`，仅访问HTML、不下载附件。`report.py`的日期和路径固定为本次任务，重跑其它日期任务时应另建目录/分支，不能把旧报告日期当成新证据。

## 证据与范围

- `cases/`：三轮680份输入；`manifest-r*.json`：入口、场景与参数。
- `results-r*.json`：源码SHA256、编译状态、现有尺退出码及失败文本、独立PDF检查结果。
- `checks.py`：墨迹、页眉页码/切换、未解析引用、编号连续、目录链接、正文行距与空白填充页；`test_checks.py`：14项故障注入和正向对照。
- `repro/`：4条A、1条B、4条C的13份最小Typst文件与1份文献文件；`repro-results.json`记录坐标。
- `coverage-measurements.json`：长内容条目数的测量记录，配合人工比对预期值，不能替代逐项文献标准审查。
- `official-results.json`：官方URL、日期和附件名；`triage.json`：人工分类、误报修正和停止依据。
- `out/`：PDF、PNG、完整日志和局部包路径，均忽略，不提交。

目录校验依赖内部链接及文字层；墨迹以72dpi灰度栅格和2bp容差测量；正文基线差容差0.08bp。前置页使用自己的独立区域口径；不把封面或行政表套进正文版心。无正文行/目录/图表的页面相应检查没有可比较对象，不能将零告警解释为全格式正确。模板内容块无法自动匿名的已知约定不列作新问题。
