"""Generate an online, no-JavaScript-readable bilingual study room."""
from pathlib import Path
import html,json,re,argparse
ROOT=Path(__file__).resolve().parents[1];SITE=ROOT/'site'
def md(text):
    out=[];paragraph=[];code=None
    def flush():
        if paragraph:out.append('<p>'+html.escape(' '.join(paragraph))+'</p>');paragraph.clear()
    for line in text.splitlines()+['']:
        if line.startswith('```'):
            flush()
            if code is None:code=[]
            else:out.append('<pre tabindex="0"><code>'+html.escape('\n'.join(code))+'</code></pre>');code=None
        elif code is not None:code.append(line)
        elif not line.strip():flush()
        elif line.startswith('#'):
            flush();level=min(4,len(line)-len(line.lstrip('#'))+1);out.append(f'<h{level}>'+html.escape(line.lstrip('#').strip())+f'</h{level}>')
        else:paragraph.append(line)
    return '\n'.join(out)
def build():
    docs={l:(SITE/f'downloads/lesson.{l}.md').read_text() for l in ['zh','en']}
    transcripts={l:(SITE/f'downloads/transcript.{l}.md').read_text() for l in ['zh','en']}
    reference=(SITE/'downloads/reference.py').read_text();exercise=(SITE/'downloads/exercise.py').read_text();data=(SITE/'downloads/examples.json').read_text()
    text='''<!doctype html><html lang="zh-CN"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>学习资料 · Legalization 04</title><link rel="stylesheet" href="../assets/style.css"></head><body><header><div class="wrap top"><a class="brand" id="back" href="../">Legalization 04</a><label class="lang-label">Language / 语言 <select id="language"><option value="zh">中文</option><option value="en">English</option></select></label></div></header><main class="wrap reading section"><p class="eyebrow">READ / UNDERSTAND / REPRODUCE</p><h1 data-zh="在这里，把每个约定读清楚。" data-en="Read every convention, right here.">在这里，把每个约定读清楚。</h1><p data-zh="完整资料可以直接阅读和复制。原文件下载是可选补充。" data-en="Read and copy the complete materials online. Original downloads are optional.">完整资料可以直接阅读和复制。原文件下载是可选补充。</p><nav class="toc" aria-label="Study materials"><a href="#notes" data-zh="完整讲义" data-en="Full notes">完整讲义</a><a href="#reference" data-zh="Python参考" data-en="Python reference">Python参考</a><a href="#exercise" data-zh="练习代码" data-en="Exercise">练习代码</a><a href="#data" data-zh="样例数据" data-en="Fixtures">样例数据</a><a href="#transcript-zh">中文文字稿</a><a href="#transcript-en">English transcript</a><a href="#reproduce" data-zh="复现" data-en="Reproduce">复现</a></nav>'''
    text+='<section id="notes"><article data-reading-lang="zh">'+md(docs['zh'])+'</article><article data-reading-lang="en" hidden>'+md(docs['en'])+'</article></section>'
    for ident,titlezh,titleen,source,filename in [('reference','独立Python参考','Independent Python reference',reference,'reference.py'),('exercise','自己补全的练习','Complete the exercise',exercise,'exercise.py'),('data','可复现情境数据','Reproducible fixtures',data,'examples.json')]:
        text+=f'<section id="{ident}"><h2 data-zh="{titlezh}" data-en="{titleen}">{titlezh}</h2><div class="actions"><button data-copy="code-{ident}" data-zh="复制代码 / 数据" data-en="Copy code / data">复制代码 / 数据</button><a href="../downloads/{filename}" download data-zh="可选：下载原文件" data-en="Optional: download original">可选：下载原文件</a><a id="python-{ident}" href="../python/" data-zh="在浏览器中运行Python" data-en="Run Python in this browser">在浏览器中运行Python</a></div><pre tabindex="0"><code id="code-{ident}">'+html.escape(source)+'</code></pre></section>'
    for lang in ['zh','en']:text+=f'<section id="transcript-{lang}">'+md(transcripts[lang])+f'<p><a href="../media/lesson.{lang}.mp4">MP4</a> · <a href="../media/lesson.{lang}.bilingual.vtt" download>中文 + English VTT</a></p></section>'
    text+='''<section id="reproduce"><h2 data-zh="复现与验证" data-en="Reproduce and verify">复现与验证</h2><p data-zh="源码、固定上游、引擎、独立Python、冻结音频与语义分镜都保存在指定GitHub仓库。使用Python媒体依赖环境运行下列命令；只有语音文字改变才需要重新调用TTS。" data-en="Source, pinned upstream references, engine, independent Python, frozen audio and semantic storyboards are in the GitHub repository. Use the media Python environment for the commands below. TTS is needed again only when speech changes."></p><pre tabindex="0"><code>node --test tests/*.test.mjs
node scripts/export-data.mjs
python scripts/speech.py
python scripts/render-film.py --stills
python scripts/render-film.py
python scripts/render-film.py --lang en
python scripts/build_reading.py
python scripts/check-site.py
python scripts/verify-media.py</code></pre><p data-zh="影片共303.67秒，12个语义场景，两种语言独立配音，共用经过阅读时间检查的时间轴。自动媒体检查不等于完整人工听审。" data-en="The film has 12 semantic scenes over 303.67 seconds, with separate narration and a shared timeline checked for caption reading time. Automated media checks are not a complete human listening review."></p><a href="https://github.com/FanqinZeng/eda-legalization-lesson04">GitHub / source / licenses</a></section><p id="copy-status" role="status"></p></main><footer class="wrap">LEGALIZATION / 04 <a id="footer-back" href="../" data-zh="返回实验" data-en="Back to the lab">返回实验</a></footer><script type="module" src="../assets/reading.mjs"></script></body></html>'''
    duration=json.loads((ROOT/'video/timeline.json').read_text())['duration']
    return text.replace('303.67',f'{duration:.2f}')
if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--check',action='store_true');a=p.parse_args();path=SITE/'reading/index.html';value=build()
    if a.check:assert path.read_text()==value,'Reading page is stale';print('Reading page matches all source files')
    else:path.write_text(value);print('Generated complete online study room')
