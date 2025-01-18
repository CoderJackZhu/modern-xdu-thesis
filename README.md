# 西安电子科技大学学位论文 XDUthesis-Typst

## 介绍

Typst是一种新的排版标记语言，由rust编写，比latex性能优异，编译速度快，即使对非常长的文章也是一样，但是稳定性可能比不上Word和LaTeX。

这是西安电子科技大学毕业论文的Typst语言模板， 适用于本科和研究生学位论文，项目基于[modern-nju-thesis](https://github.com/nju-lug/modern-nju-thesis)重构。

目前该项目尚未完成西电毕业论文格式的适配，正在开发中，因此直接作为毕业论文模板使用时，可能会有一些问题，慎用。

## 使用方法

### VS Code 本地编辑（推荐）

在 VS Code 中安装 Tinymist Typst 和 Typst Preview 插件。前者负责语法高亮和错误检查等功能，后者负责预览。
也推荐下载 Typst Companion 插件，其提供了例如 Ctrl + B 进行加粗等便捷的快捷键。
你还可以下载我开发的 Typst Sync 和 Typst Sympy Calculator 插件，前者提供了本地包的云同步功能，后者提供了基于 Typst 语法的科学计算器功能。

最后用 VS Code 打开生成的目录，打开 template文件夹下的thesis.typ 文件，并按下 Ctrl + K V 进行实时编辑和预览。
<!--  -->
本科生和研究生的毕业论文都支持，在thesis.typ下按照要求更改选项即可，所有内容都在一个文件下了，语法简洁方便修改。

学习 Typst 需要多久？
一般而言，仅仅进行简单的编写，不关注布局的话，你可以打开模板就开始写了。

如果你想进一步学习 Typst 的语法，例如如何排篇布局，如何设置页脚页眉等，一般只需要几个小时就能学会。

如果你还想学习 Typst 的「元信息」部分，进而能够编写自己的模板，一般而言需要几天的时间阅读文档，以及他人编写的模板代码。

如果你有 Python 或 JavaScript 等脚本语言的编写经验，了解过函数式编程、宏、样式、组件化开发等概念，入门速度会快很多。

我有编写 LaTeX 的经验，如何快速入门？
可以参考 面向 LaTeX 用户的 Typst 入门指南。

目前 Typst 有哪些第三方包和模板？
可以查看 Typst Universe。






## 致谢参考仓库


[南京大学毕业论文](https://github.com/nju-lug/modern-nju-thesis)
[上海大学本科毕业论文](https://github.com/shuosc/SHU-Bachelor-Thesis-Typst)