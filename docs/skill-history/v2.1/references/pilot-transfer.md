# 真实试点之后如何一次迁移

试点：同工作区 `eda-congestion-lesson05/`，公开目标 https://fanqinzeng.github.io/eda-congestion-lesson05/ 。具体观察与回归在 `docs/skill-iteration.md`、`docs/qa/browser.json`、`docs/qa/media.json`、`tests/test_film_typography.py` 和 `tests/player.test.mjs`。初稿、before帧和散列在 `docs/skill-history/v1*` 与 `docs/qa/v1/`。仅以实际部署记录判断公开站是否已发布。

## 经试点证实的失误与修正

- 实帧看到中文换行丢字、数值越过格宽、多pin虚拟中心冒用原始pin名；修复字体排版、真实数据身份和逐步/合计状态区分后重看实帧及重编码。
- 真实390px浏览器复现隐藏章节导航；修复为可用的响应布局，375/390/768/1440与实际影片seek回归通过。
- 播放位置按数组索引会在场景重排时映射错误；通过稳定scene id修正，独立回归从失败到通过。
- 源helper与讲稿单位不一致，必须把兼容复现、教学修正和公平的空间分布对比说清楚；不能机械复制数字。
- 独立整课审阅实测指出：原始RUDY仍用占用容量画热点、英文首访隐式下载MP4、重绘丢失连续键盘焦点、精确小数容量被step限制，以及BFCache返回后的Worker已死亡。均需以真实浏览器回归落实，不能只在说明文字中承诺。回归脚本与before/after报告随试点保留；生成器也必须保留修复。

## 可复用的实现

从试点只复制真正通用部分，保留MIT/字体/Pyodide许可：

- `scripts/film_common.py`：真实音频和两种文本阅读时间共同生成语义时间轴、缓存PCM、字体字宽/换行、章节/双语VTT/文字稿、MP4编码和内嵌字幕。新课提供自己的 `video/course.json`、`video/story.json` 与课程图形渲染器；不要复制拥塞的grid、事实断言或讲解数字。
- `scripts/speech.py`：按scene id和unit缓存两语言TTS，文本未变不重合成。`video/story.json` 的每个unit必须是同一个意思的中英文本。
- `site/assets/player.mjs`：语言联动、语义进度、章节、倍速、字幕和单独配音选择；新manifest提供新课路径和scene id。
- `site/python/worker.mjs`、workspace控制器与本地vendor：真实Worker CPython、异常、停止、限时与实时执行。替换全部样例、提示、课名、持久化key和返回链接；不要沿用前课golden声明。
- 阅读页生成和静态资源检查可参考其机制，但新课文字、标题、指标、资料和页面须按新主题生成。时长来自timeline，不手写旧课秒数。

这些路径适用于当前两个仓库所在的同一VLSI工作区。跨机器时从上述源码仓库取得相同文件，并按requirements建立自己的环境；不能假定原机器的绝对Python路径存在。

## 一次消费

1. 复制冻结skill到新课的skills/eda-lesson-studio，记录版本和每文件SHA256；读取正文及本参考。
2. 新课只读源审计与数学约定，写课程设计；先完成引擎、独立Python及针对边界的检查。
3. 沿用试点的版式、双语组件与媒体机制，一次完成新的网页、例题、讲义、Python、语义分镜及课程专用图形。
4. 看真实样片和代表帧以发现事实/排版错误，完成两种实际MP4；这些是正常制作与验收，不是重启风格探索。
5. 运行真实学习路径、数学、媒体、公开资源与部署验证，修复实质错误后交付。不要为了证明“一次性”而跳过必要修复，也不要无依据追加新的整站功能。

## v2.1：把迁移验收前移

第二课`eda-legalization-lesson04`实际消费的是v2.0.0。其`docs/qa/review-before.json`、`review-after.json`、`review-findings.md`记录：小数移动改变未操作轴、全局epsilon漏掉严格正面积重叠、语言重绘留下过期错误、生成器依赖兄弟仓库；前后五个可观察断言均从失败变为通过。首次浏览器验收还修正了动态目标列翻译与答题提交焦点；规则适用于完整状态变化，不能只测初始静态页面。

v2.1把这些经验写入[制作约定](production.md)的前置检查，后续课在写事件/判定/生成器时就采用，完成网页和影片后再做完整验收。现成回归可参考第二课`scripts/check-review.py`、`tests/engine.test.mjs`和`scripts/check-browser.py`的机制；按新课模型改造，不复制教师答案或绝对机器路径。

新课开始时冻结当时的最新版；旧课消费证明继续核对原版本的历史快照。v2.1更新不等于第二课曾用v2.1生成，也不等于已把整部新课重新制作一次。后续交付报告写明实际制作轮次、必要修复和执行过的检查。
