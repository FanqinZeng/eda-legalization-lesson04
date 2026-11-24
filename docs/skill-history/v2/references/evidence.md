# 来自当前 VLSI 项目的证据

提炼日期：2026-11-24，Asia/Shanghai。依据实际读取的对话、源码及验收文档，不假定其他聊天自动共享上下文。

## Placement Lesson 03

对话 id：`01a1e5a3-109e-7c40-a0d2-83fce355a3b5`，标题以工具原文为准：`https://github.com/yongfu-li/eda-learning/issues/26 这个是我负责的…`。

实际读到用户要求：

- 对推荐静态课程方案选择“按推荐方案全权推进”。
- “配音不仅仅要是中文的应该要是中英文都有”。
- 资料应在网站板块或独立页面显示，不能必须下载才能看。
- “网站要修改为中英文可选的”“视频要增加双语字幕”“python要增加一个实时代码交互台”。
- 用户指出只有视频画面或配音仍是中文；后续实际定位为默认硬编码中文影片，修复了界面与视频语言的初始及后续联动。

可检查的成果和实现：`eda-placement-lesson3/README.md`、`PROGRESS.md`、`docs/course-design.md`、`docs/qa/voice-ui.json`、`docs/qa/full-upgrade-deployment.json` 及 scripts、site 源码。公开作品：https://fanqinzeng.github.io/eda-placement-lesson3/ 。

## Partitioning 课程

对话 id：`01a19fcd-3411-7ee0-a9b5-49fa15fb8c82`，标题：`你读取并分析一下https://github.com/yongfu-li/eda-learning/issues的所有…`。

近期对话显示用户明确要求把最新版发布到 Pages；此前仅有分支提交并不能满足公开网站交付。影片文字稿被纳入搜索并能够定位具体时间点，说明完整学习路径需要实际浏览器验证。

只读来源：`Partitioning_Module_Coordinator/course-playbook/SKILL.md`、`reference/07-lessons-learned.md`、`scripts/film/` 和首页影片。经验包括：真引擎先于图片、深色技术影片、拒绝重复图形移动、真实样片审查、字幕阅读时间、来源和许可、不能把过期文档或未验证计划写成已完成。

注意：该旧任务的分支限制和已暂停定时任务只属于旧仓库，不限制本次明确授权的两个新仓库。

## 本次验证环境

GitHub connector 与 gh CLI 均验证为 FanqinZeng；两个目标仓库原始为空，账号有 admin / push 权限，CLI 含 repo 和 workflow 权限。媒体依赖环境及 imageio_ffmpeg 已实际导入验证。受限沙箱内的联网错误不能当作登录失效；联网验证后 CLI 登录正常。

两个历史“检查 GitHub 账号访问”类聊天中有单次 turn 超过工具读取上限，未声称完整读完。核心教学要求取自以上已成功读取的实际消息及本地可核对产物。
