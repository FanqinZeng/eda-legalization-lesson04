"""Reusable bilingual timeline, typography, subtitles, and real MP4 encoding."""
from pathlib import Path
from functools import lru_cache
import json,hashlib,math,subprocess,wave,time
import numpy as np
from PIL import Image,ImageDraw,ImageFont
import imageio_ffmpeg
W,H,FPS=1920,1080,30
BG='#061820';PANEL='#0d2933';IVORY='#eeeadd';TEAL='#76cbb5';GOLD='#ddbd78';MUTED='#9ab0af';FAINT='#2a4852'
def ease(x):x=max(0,min(1,x));return x*x*(3-2*x)
def mix(a,b,t):return a+(b-a)*t
def n(v):return str(round(v,4)).removesuffix('.0')
def ts(s):
    ms=round(s*1000);h,ms=divmod(ms,3600000);m,ms=divmod(ms,60000);sec,ms=divmod(ms,1000);return f'{h:02}:{m:02}:{sec:02}.{ms:03}'

class Film:
    def __init__(self,root,lang):
        self.root=Path(root);self.lang=lang;self.cache=self.root/'.cache';self.cache.mkdir(exist_ok=True);self.media=self.root/'site/media';self.media.mkdir(exist_ok=True)
        self.story=json.loads((self.root/'video/story.json').read_text());meta=self.root/'video/course.json';self.metadata=json.loads(meta.read_text()) if meta.exists() else {'badge':'CONGESTION / LESSON 05','titles':{'zh':'一张网，两种可能','en':'One Net, Two Routes'}};self.ff=imageio_ffmpeg.get_ffmpeg_exe();self.timeline=self.build_timeline();self.duration=self.timeline['duration'];self.scenes=self.timeline['scenes']
    @lru_cache(None)
    def font(self,size,mono=False):return ImageFont.truetype(str(self.root/'video/fonts'/('JetBrainsMono-Regular.ttf' if mono else 'NotoSansSC-Regular.otf')),size)
    @lru_cache(5000)
    def sprite(self,content,size,color,mono=False):
        f=self.font(size,mono);box=f.getbbox(content);im=Image.new('RGBA',(max(1,math.ceil(f.getlength(content))+8),box[3]-box[1]+8));ImageDraw.Draw(im).text((4,4-box[1]),content,font=f,fill=color);return im
    def text(self,im,s,x,y,size=36,color=IVORY,mono=False):
        sp=self.sprite(str(s),size,color,mono);im.paste(sp,(round(x),round(y)),sp)
    def fit_size(self,s,width,max_size=28,mono=False):
        size=max_size
        while size>8 and self.font(size,mono).getlength(str(s))>width:size-=1
        return size
    def wrap(self,s,size,width,lang=None):
        if '\n' in s:return [line for block in s.split('\n') for line in self.wrap(block,size,width,lang)]
        lang=lang or self.lang;tokens=s.split(' ') if lang=='en' else list(s);lines=[];line=''
        for token in tokens:
            candidate=(line+' '+token).strip() if lang=='en' else line+token
            if line and self.font(size).getlength(candidate)>width:lines.append(line);line=token
            else:line=candidate
        if line:lines.append(line)
        return lines
    def paragraph(self,im,s,x,y,width=900,size=34,color=MUTED):
        for i,line in enumerate(self.wrap(s,size,width)):self.text(im,line,x,y+i*size*1.55,size,color)
    @lru_cache(1)
    def background(self):
        y,x=np.mgrid[:H,:W];v=np.maximum(0,1-((x-W*.35)/(W*1.05))**2-((y-H*.3)/H)**2)[...,None];return Image.fromarray(np.uint8(np.array([6,20,28])+(np.array([12,35,44])-np.array([6,20,28]))*v))
    def build_timeline(self):
        files=[self.root/'video/audio'/lang/f'{s["id"]}-{i}.mp3' for lang in ['zh','en'] for s in self.story for i,_ in enumerate(s['units'])]
        digest=hashlib.sha256((self.root/'video/story.json').read_bytes()+b''.join(p.read_bytes() for p in files)).hexdigest();path=self.root/'video/timeline.json'
        if path.exists():
            old=json.loads(path.read_text())
            if old.get('digest')==digest and all((self.cache/f'narration.{l}.wav').exists() for l in ['zh','en']):return old
        audio={};cursor=0;scenes=[];chunks={'zh':[],'en':[]}
        for scene in self.story:
            entry={'id':scene['id'],'kind':scene['kind'],'title':scene['title'],'start':cursor,'units':[]}
            for i,u in enumerate(scene['units']):
                pcm={lang:subprocess.check_output([self.ff,'-v','error','-i',str(self.root/'video/audio'/lang/f'{scene["id"]}-{i}.mp3'),'-f','s16le','-ar','24000','-ac','1','pipe:1']) for lang in ['zh','en']}
                lengths={lang:len(pcm[lang])/48000 for lang in ['zh','en']};reading=max(len(u['zh'])/4.5,len(u['en'])/15)+.8
                duration=math.ceil(max(*[v+.6 for v in lengths.values()],reading)*FPS)/FPS
                cue={'id':f'{scene["id"]}-{i}','start':cursor,'end':cursor+duration,'duration':duration,'audioDuration':lengths,'text':u}
                for lang in ['zh','en']:
                    prefix=b'\0\0'*round(.15*24000);body=prefix+pcm[lang];target=round(duration*24000)*2;assert len(body)<=target;chunks[lang].append(body+b'\0'*(target-len(body)))
                entry['units'].append(cue);cursor+=duration
            entry['end']=cursor;entry['duration']=cursor-entry['start'];scenes.append(entry)
        for lang in ['zh','en']:
            with wave.open(str(self.cache/f'narration.{lang}.wav'),'wb') as out:out.setnchannels(1);out.setsampwidth(2);out.setframerate(24000);out.writeframes(b''.join(chunks[lang]))
        timeline={'digest':digest,'width':W,'height':H,'fps':FPS,'duration':cursor,'scenes':scenes};path.write_text(json.dumps(timeline,ensure_ascii=False,indent=2)+'\n');return timeline
    def scene_at(self,t):return next((s for s in self.scenes if s['start']<=t<s['end']),self.scenes[-1])
    def frame_shell(self,t):
        scene=self.scene_at(t);im=self.background().copy();d=ImageDraw.Draw(im);self.text(im,self.metadata['badge'],90,52,25,TEAL,True);self.text(im,f'{self.scenes.index(scene)+1:02} / {len(self.scenes)}',1640,52,25,MUTED,True)
        title=scene['title'][self.lang];size=min(58,int(1725*58/max(1,self.font(58).getlength(title))));self.text(im,title,90,126,size);d.line((94,230,1826,230),fill=FAINT,width=1)
        d.line((94,860,1826,860),fill=FAINT,width=1);d.rectangle((94,1045,1826,1049),fill=FAINT);d.rectangle((94,1045,94+1732*t/self.duration,1049),fill=TEAL)
        return im,scene
    def output_materials(self,frame):
        for lang in ['zh','en']:
            transcript=['# '+self.metadata['titles'][lang],''];chapters=[]
            for s in self.scenes:
                chapters.append({'id':s['id'],'start':s['start'],'title':s['title'][lang]});transcript+=['## '+ts(s['start'])+' · '+s['title'][lang],'']+[u['text'][lang] for u in s['units']]+['']
            (self.root/f'site/downloads/transcript.{lang}.md').write_text('\n\n'.join(transcript).rstrip()+'\n');(self.media/f'chapters.{lang}.json').write_text(json.dumps(chapters,ensure_ascii=False,indent=2)+'\n')
            for mode in ['bilingual','zh','en']:
                lines=['WEBVTT','']
                for s in self.scenes:
                    for u in s['units']:
                        text='\n'.join(self.wrap(u['text']['zh'],30,1670,'zh')+self.wrap(u['text']['en'],30,1670,'en')) if mode=='bilingual' else '\n'.join(self.wrap(u['text'][mode],30,1670,mode))
                        lines += [u['id'],f'{ts(u["start"])} --> {ts(u["end"]-.05)} line:78% size:92%',text,'']
                (self.media/f'lesson.{lang}.{mode}.vtt').write_text('\n'.join(lines))
            (self.media/f'lesson.{lang}.vtt').write_text((self.media/f'lesson.{lang}.{lang}.vtt').read_text())
        versions={lang:{'label':'中文' if lang=='zh' else 'English','voice':'zh-CN-XiaoxiaoNeural' if lang=='zh' else 'en-US-JennyNeural','video':f'media/lesson.{lang}.mp4','poster':'media/poster.jpg' if lang=='zh' else 'media/poster.en.jpg','transcript':f'reading/#transcript-{lang}','trackLabel':'中文 + English','captionTracks':{mode:f'media/lesson.{lang}.{mode}.vtt' for mode in ['bilingual','zh','en']},'chapters':json.loads((self.media/f'chapters.{lang}.json').read_text()),'scenes':[{'id':s['id'],'start':s['start'],'end':s['end']} for s in self.scenes]} for lang in ['zh','en']}
        (self.media/'versions.json').write_text(json.dumps(versions,ensure_ascii=False,indent=2)+'\n')
        frame(self.scenes[3]['start']+5).save(self.media/('poster.jpg' if self.lang=='zh' else 'poster.en.jpg'),quality=92)
    def stills(self,frame):
        out=self.root/'.qa'/self.lang;out.mkdir(parents=True,exist_ok=True);contact=Image.new('RGB',(960*2,540*math.ceil(len(self.scenes)/2)),BG)
        for i,s in enumerate(self.scenes):
            im=frame(s['start']+s['duration']*.7);im.save(out/f'scene-{i:02}.jpg',quality=88);contact.paste(im.resize((960,540)),((i%2)*960,(i//2)*540))
        contact.save(out/'contact.jpg',quality=90);print('Saved real representative frames',out,flush=True)
    def encode(self,frame,sample=False):
        start=self.scenes[2]['start'] if sample else 0;duration=min(12,self.duration-start) if sample else self.duration
        dest=self.root/'.qa'/f'sample.{self.lang}.mp4' if sample else self.media/f'lesson.{self.lang}.mp4';dest.parent.mkdir(exist_ok=True)
        cmd=[self.ff,'-v','error','-y','-f','rawvideo','-pix_fmt','rgb24','-s',f'{W}x{H}','-r',str(FPS),'-i','pipe:0','-ss',str(start),'-i',str(self.cache/f'narration.{self.lang}.wav')]
        if not sample:cmd+=['-i',str(self.media/f'lesson.{self.lang}.bilingual.vtt')]
        cmd+=['-map','0:v:0','-map','1:a:0']
        if not sample:cmd+=['-map','2:s:0','-c:s','mov_text','-metadata:s:s:0','language=mul','-metadata:s:s:0','title=Chinese + English','-disposition:s:0','default']
        cmd+=['-c:v','libx264','-preset','fast','-crf','22','-pix_fmt','yuv420p','-c:a','aac','-b:a','128k','-movflags','+faststart','-threads','4','-t',str(duration),str(dest)]
        p=subprocess.Popen(cmd,stdin=subprocess.PIPE);began=time.monotonic();frames=round(duration*FPS)
        try:
            for f in range(frames):
                p.stdin.write(frame(start+f/FPS).tobytes())
                if f%600==0:print(f'{self.lang}: {f}/{frames}, {time.monotonic()-began:.1f}s',flush=True)
            p.stdin.close();assert p.wait()==0
        except BaseException:p.kill();raise
        print('Encoded',dest,flush=True)
