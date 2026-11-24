# 对齐了，还不一定合法 · Legalization Lesson 04

中英文Greedy Site/Row Snap交互课程，对应 [issue #36](https://github.com/yongfu-li/eda-learning/issues/36) 与 [固定上游教材](https://github.com/yongfu-li/eda-learning/tree/003bcd49e3794e6cfd2680181cdbd347d673ad07/courses/learn_legalization/module02-01-greedy-snap)。

公开入口：[课程主页](https://fanqinzeng.github.io/eda-legalization-lesson04/)。实际部署与验收结果见 [PROGRESS.md](PROGRESS.md)。

一次消费拥塞试点冻结的 **skill v2.0.0**；五文件SHA256及消费记录在 [docs/skill-transfer.json](docs/skill-transfer.json)。沿用已验证的版式、播放器、Worker与语义影片流水线，为本课新写算法、图形、讲义和配音；必要的正确性与验收修复不重新开启风格探索。

当前可复用skill已更新为 [v2.1.0](skills/eda-lesson-studio/SKILL.md)，吸收合法化课验收问题，并加入制作前置检查。已发布课程原来消费的版本及散列继续保留；后续新课使用最新版，具体更新见 [版本说明](docs/skill-update-v2.1.md)。

## 内容

- 全站中文/English，保留实验状态；可编辑坐标、真实宽度与行高的双布局图、拖动/键盘、真实逐cell前缀与重放、全部重叠对和合法性分项。
- 默认教师例吸附后A/B同在(4,2)、C在(5,2)，仍有3对重叠。全体L1=4.4、movable-only=3.8、中心HPWL=32，分别说明计数范围与fixed D的恢复。
- Python ties-to-even在JS中显式复现；半整数、行等距、宽度边界与相邻接触反例。独立Python与105组输入交叉核对。
- 两部独立中英文配音MP4，各277.03秒，1080p/30fps、H.264/AAC、12个语义场景与24个语义字幕单元；双语内嵌/外部字幕、封面、章节、全文文字稿和可复现源。
- 真正Worker CPython，任意编辑执行、实时运行、输出/异常、停止、5秒超时及BFCache返回恢复。本地Pyodide按需载入，无外部CDN。
- 讲义、参考/练习代码、数据和文字稿全部在线阅读复制；6项带解析练习和本机学习记录。

## 运行与验证

```bash
python3 scripts/serve.py --port 8186
node --test tests/*.test.mjs
python3 scripts/build-python.py
python3 scripts/build_reading.py --check
python3 scripts/check-transfer.py
python3 scripts/check-site.py
```

媒体制作使用Python 3.12+隔离环境与requirements-media.txt；ffmpeg由imageio-ffmpeg提供。

```bash
node scripts/export-data.mjs
python scripts/speech.py
python scripts/render-film.py --stills
python scripts/render-film.py
python scripts/render-film.py --lang en
python scripts/build_reading.py
python scripts/verify-media.py
python -m unittest discover -s tests -p 'test_*.py'
python scripts/check-browser.py --media
```

源码与实际验收证据在 [docs/qa](docs/qa)，课程约定见 [docs/course-design.md](docs/course-design.md)。自动检查不等于完整人工听审或真实触屏验收；这两项限制如实保留。

新代码MIT，新教材CC BY 4.0，字体与Pyodide遵循其许可，见 [THIRD_PARTY_NOTICES.md](THIRD_PARTY_NOTICES.md)。
