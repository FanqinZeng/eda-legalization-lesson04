# 媒体实现

已有参考：`eda-placement-lesson3/scripts/speech.py`、`media_config.py`、`render-film.py`、`build-bilingual-captions.py`、`verify-media.py`、`build-versions.py`。这些是可参考的已运行实现，不能原样保留旧课程的模型和画面。

本机已有可复用依赖环境：`/Users/fanqin/Documents/Codex/VLSI/eda-placement-lesson3/.venv/bin/python`。先验证 Pillow、numpy、imageio_ffmpeg、edge_tts 和所需浏览器检查依赖，避免再装一套。项目仍记录自身 requirements-media.txt。ffmpeg 可以由 imageio_ffmpeg 提供，不因 PATH 中没有 ffmpeg 就判断不能制作。

分别缓存中文和英文的实际语音。可用声音基线是 zh-CN-XiaoxiaoNeural、en-US-JennyNeural；实际读法、停顿和字幕需要抽查。声源失效时选择可用替代，诚实记录，不能省略任一语言音轨。

分镜以稳定语义 id 对齐，不依赖两种语言句子数量相等。使用实测音频时长；有必要时给短段增加停顿而不随意拉伸旁白。时间线端点须落在成片内，字幕不逆序、不重叠，文本宽度不溢出。双语阅读时间按两种文本较慢者安排；不能仅以中文节奏假定英文读得完。

优先复用通用文字排版、缓动、编码、字幕和音频缓存。算法图形针对新课重写，至少包含逐步过程、一个数值示例和一个有解释的反例。网页导出可核对轨迹供渲染器使用；关键数值由断言核对。

影片输出 H.264 / AAC，MP4 faststart，web VTT 和嵌入字幕轨。大文件各自保持 GitHub 单文件限制内，关注仓库与 Pages 总体积。仅按内容变更重渲染相关语言或场景，避免不断全量渲染。

先检查开头、关键公式、峰值复杂画面、反例、结尾代表帧；短样片观察连续运动。完整导出后实际解码、检测音轨能量、字幕端点、章节 seek 和网页播放。用实际时长更新清单，未做完整人工听审时保留说明。
