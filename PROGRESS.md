# 制作进度

2026-11-24，Asia/Shanghai。目标截止：今天14:00。

初始提交 923c9fe 已实际推送，GitHub Pages已启用public=true、build_type=workflow。发布流水线随site变更触发，尚未上传课程网页，因此尚未有已交付的公开成品。

初始skill已建立并通过官方结构验证，拥塞仓库保留v1快照。中英文TTS实际短样音均可解码且非静音。上游固定003bcd49e3794e6cfd2680181cdbd347d673ad07，module与common共33个文本文件已保存于当前VLSI项目course-production-20261124/research/。

每30分钟制作任务已ACTIVE，id=skill，接续本聊天；目标14:00前交付。当前没有需用户处理的授权阻塞。

接续course-production-20261124/PLAN.md、PROGRESS.md和research/source-semantics.md。先用v1完成拥塞网页及真实成片，根据观察迭代skill，冻结后再一次制作合法化课程。现阶段不得把源预检或skill试用写成产品验收。

## 一次迁移的本地成品

冻结skill v2.0.0五文件散列均验证，消费记录在docs/skill-transfer.json。已一次完成greedy snap纯JS与独立Python、双语网页/真实trace/可编辑输入/拖动/键盘、全部重叠诊断、六题解析、完整在线讲义源码数据文字稿、真正Worker Python和两种新旁白影片。

中文与英文各277.03秒、1920×1080/30fps、H.264/AAC，12个语义场景、24个双语cue、内嵌/外部双语字幕、章节与封面齐全；真实全解码和音量检查通过，中文均值-20.5dB、英文-22.1dB。实际看过两语言代表帧及12秒真实样片，没有重新进行风格探索。

9项Node、2项通用字体回归、105组JS/Python对照、47项资源/锚点、在线资料与skill散列检查通过。真实Edge19项完整路径通过，包括精确半整数/row tie、fixed保护、连续键盘、真实拖动、手机、按需英片、章节/语种/字幕、真实Python异常/停止/live/超时和无存储。真实BFCache返回后的首次执行也通过。

正常验收修复了稳定表格的目标列翻译和答题后的焦点保留；属于必要正确性修复，未改变冻结skill或重开风格探索。

下一步：独立整课审阅、处理实质问题后推送并验收实际公开Pages。完整人工听审与物理触屏未做，线上发布尚未完成。
