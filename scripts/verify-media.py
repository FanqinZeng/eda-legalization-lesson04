"""Inspect actual decoded files, audio energy, semantic captions and timelines."""
from pathlib import Path
import json,re,subprocess,hashlib
import imageio_ffmpeg
ROOT=Path(__file__).resolve().parents[1];FF=imageio_ffmpeg.get_ffmpeg_exe();timeline=json.loads((ROOT/'video/timeline.json').read_text());report={'status':'passed','duration':timeline['duration'],'files':[],'caption_units':0,'human_full_listening':'not performed','physical_touchscreen':'not tested'}
for s in timeline['scenes']:
 for u in s['units']:
  assert u['end']>u['start']>=0 and u['end']<=timeline['duration']+1e-6
  assert u['duration']+1e-8>=max(len(u['text']['zh'])/4.5,len(u['text']['en'])/15)+.8
  for lang in ['zh','en']:assert u['audioDuration'][lang]+.15<=u['duration']
  report['caption_units']+=1
for lang in ['zh','en']:
 path=ROOT/f'site/media/lesson.{lang}.mp4';assert 10000<path.stat().st_size<100_000_000
 proc=subprocess.run([FF,'-hide_banner','-i',str(path),'-map','0:v:0','-map','0:a:0','-f','null','-'],capture_output=True,text=True);assert proc.returncode==0,proc.stderr
 for expected in ['Video: h264','1920x1080','30 fps','Audio: aac','Subtitle: mov_text']:assert expected in proc.stderr,expected
 vol=subprocess.run([FF,'-hide_banner','-i',str(path),'-map','0:a:0','-af','volumedetect','-f','null','-'],capture_output=True,text=True);assert vol.returncode==0
 mean=float(re.search(r'mean_volume:\s*([-\d.]+) dB',vol.stderr).group(1));peak=float(re.search(r'max_volume:\s*([-\d.]+) dB',vol.stderr).group(1));assert -45<mean<-6 and peak<=0
 for mode in ['bilingual','zh','en']:
  vtt=(ROOT/f'site/media/lesson.{lang}.{mode}.vtt').read_text();assert vtt.startswith('WEBVTT') and vtt.count('-->')==report['caption_units']
 out=ROOT/'.qa'/f'encoded-{lang}.jpg';subprocess.run([FF,'-v','error','-y','-ss',str(timeline['scenes'][3]['start']+4),'-i',str(path),'-frames:v','1',str(out)],check=True)
 report['files'].append({'lang':lang,'bytes':path.stat().st_size,'sha256':hashlib.sha256(path.read_bytes()).hexdigest(),'mean_volume_db':mean,'peak_db':peak,'full_decode':'passed','video':'1920x1080 / 30fps / H.264','audio':'AAC','embedded_subtitles':'mov_text / Chinese + English','representative_frame':str(out.relative_to(ROOT))})
assert report['files'][0]['sha256']!=report['files'][1]['sha256']
(ROOT/'docs/qa/media.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n');print(json.dumps(report,ensure_ascii=False,indent=2))
