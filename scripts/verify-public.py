"""Check actual published HTTPS resources without treating expected URLs as proof."""
from pathlib import Path
import urllib.request,json,argparse,hashlib
p=argparse.ArgumentParser();p.add_argument('--source-commit',required=True);p.add_argument('--actions-run',type=int,required=True);a=p.parse_args()
ROOT=Path(__file__).resolve().parents[1];BASE='https://fanqinzeng.github.io/eda-legalization-lesson04/';checks=[]
for path in ['', 'reading/','python/','assets/app.mjs','assets/engine.mjs','assets/player.mjs','downloads/reference.py','python/examples.mjs','python/worker.mjs','assets/style.css','media/versions.json','media/lesson.zh.bilingual.vtt','media/lesson.en.bilingual.vtt','media/lesson.zh.mp4','media/lesson.en.mp4','vendor/pyodide/pyodide.asm.wasm']:
 headers={'Range':'bytes=0-63'} if path.endswith('.mp4') else {};request=urllib.request.Request(BASE+path,headers=headers,method='HEAD' if path.endswith('.wasm') else 'GET')
 with urllib.request.urlopen(request,timeout=60) as response:
  assert response.status in [200,206]
  media=path.endswith('.mp4');runtime=path.endswith('.wasm');sample=response.read(64) if media or runtime else response.read()
  item={'path':path or '/','status':response.status,'content_type':response.headers.get('Content-Type'),'content_length':response.headers.get('Content-Length')}
  if media:assert b'ftyp' in sample,'Not an MP4 response'
  elif not runtime:
   local=ROOT/'site'/path
   if local.is_dir():local=local/'index.html'
   item['sha256']=hashlib.sha256(sample).hexdigest();assert item['sha256']==hashlib.sha256(local.read_bytes()).hexdigest(),f'Published content differs from validated source: {path}'
  checks.append(item)
report={'status':'passed','base':BASE,'source_commit':a.source_commit,'actions_run':a.actions_run,'checks':checks};(ROOT/'docs/qa/public-resources.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n');print(json.dumps(report,indent=2))
