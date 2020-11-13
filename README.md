<br />
<p align="center">
  <h3 align="center">新标准日本语单词一览表</h3>
</p>
<br />

# 目录
* [关于此项目](#关于此项目)
  * [使用到的框架](#使用到的框架)
* [上手指南](#上手指南)
  * [做好准备](#做好准备)
  * [安装步骤](#安装步骤)
* [使用指南](#使用指南)
* [功能规划](#功能规划)
* [许可证](#许可证)
* [联系](#联系)

# 关于此项目
学习新标准日本语（第二版）时，经常会遇到读音或书写相近的单词，因此有了快速查找相似词的想法，以方便学习记忆。这个项目就是用来快速查词的。建议在 Windows 下面运行使用，其他平台请自行修改尝试

## 使用到的框架
* [DataTables](https://datatables.net)
* [JQuery](https://jquery.com)

# 上手指南
你可以本地打开这个项目，在浏览器中使用，下面是简要操作指南

## 做好准备
发音音频部分，使用了 Anki 上面的相关牌组，请到其官网自行搜索下载安装：
https://ankiweb.net/shared/decks/

提示关键词：新标准日本语

## 安装步骤
1. 克隆本项目
```sh
git clone https://github.com/smartsl/biaori.git
```
2. 在 DataTables 官网下载本地包：https://datatables.net/download/ ，解压覆盖到本项目中
3. （可选）将 config.js.example 复制一份并改名为 config.js，修改其中变量为本地 Anki 资源存储目录路径。如果省略此步，就没有发音功能了

# 使用指南
用你喜爱的浏览器打开 HTML 文件即可。在搜索栏里输入部分假名、汉字或者课号，结果会即时显示出来。可以用空格隔开多个关键词。点击音频听单词发音

# 功能规划
* 待加入N3、N2、N1部分
* 待加入假名标注音调功能

# 许可证
该项目签署了MIT 授权许可，详情请参阅 `LICENSE`

# 联系
smartsl@github