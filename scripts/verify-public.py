"""Check actual published HTTPS resources without treating expected URLs as proof."""
from pathlib import Path
import urllib.request,json,argparse
p=argparse.ArgumentParser();p.add_argument('--source-commit',required=True);p.add_argument('--actions-run',type=int,required=True);a=p.parse_args()
ROOT=Path(__file__).resolve().parents[1];BASE='https://fanqinzeng.github.io/eda-legalization-lesson04/';checks=[]
for path in ['', 'reading/','python/','assets/engine.mjs','assets/player.mjs','assets/style.css','media/versions.json','media/lesson.zh.bilingual.vtt','media/lesson.en.bilingual.vtt','media/lesson.zh.mp4','media/lesson.en.mp4','vendor/pyodide/pyodide.asm.wasm']:
 headers={'Range':'bytes=0-63'} if path.endswith('.mp4') else {};request=urllib.request.Request(BASE+path,headers=headers,method='HEAD' if path.endswith('.wasm') else 'GET')
 with urllib.request.urlopen(request,timeout=60) as response:
  assert response.status in [200,206];sample=response.read(64);checks.append({'path':path or '/','status':response.status,'content_type':response.headers.get('Content-Type'),'content_length':response.headers.get('Content-Length')})
  if path.endswith('.mp4'):assert b'ftyp' in sample,'Not an MP4 response'
report={'status':'passed','base':BASE,'source_commit':a.source_commit,'actions_run':a.actions_run,'checks':checks};(ROOT/'docs/qa/public-resources.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n');print(json.dumps(report,indent=2))
