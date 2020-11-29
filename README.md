<br />
<p align="center">
  <h3 align="center">新标准日本语单词一览表</h3>
</p>
<br />

# 目录
* [关于此项目](#关于此项目)
  * [最近更新](#最近更新)
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

## 最近更新

2020-11-29 新增了语法查询 Demo

## 使用到的框架
* [DataTables](https://datatables.net)
* [JQuery](https://jquery.com)

# 上手指南
你可以本地打开这个项目，在浏览器中使用，下面是简要操作指南

## 做好准备
* 正版用户可在 App 中下载数据后，拷贝手机存储设备中的 PEP/BiaoRi 目录到本目录下，改名为 assets ，来使用里面的音频等资源

* （老页面可选）发音音频部分，使用了 Anki 上面的相关牌组，请到其官网自行搜索下载安装：
https://ankiweb.net/shared/decks/

  提示关键词：新标准日本语

## 安装步骤
1. 克隆本项目
```sh
git clone https://github.com/smartsl/biaori.git
```
2. 在 DataTables 官网下载本地包：https://datatables.net/download/ ，解压覆盖到本项目中
3. 将 config.js.example 复制一份并改名为 config.js
4. （老页面可选）修改 config.js 中的 media_dir 变量为本地 Anki 资源存储目录路径。如果省略此步，就没有发音功能了

# 使用指南
用你喜爱的浏览器打开 HTML 文件即可。在搜索栏里输入部分假名、汉字或者课号，结果会即时显示出来。可以用空格隔开多个关键词。如果有音频可以点击听发音
* gram.html （新页面，可查询初级上册第一单元语法）
* n5n4.html （老页面，可查询初级上下册范围内单词）

# 功能规划
* 重新规划了新的查询页面，将默认使用 App 资源，待加入单词和课文

# 许可证
该项目签署了MIT 授权许可，详情请参阅 `LICENSE`

# 联系
smartsl@github