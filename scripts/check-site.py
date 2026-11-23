"""Check project-subpath resource references and online study artifacts."""
from pathlib import Path
from html.parser import HTMLParser
from urllib.parse import urlsplit,unquote
import json,re
ROOT=Path(__file__).resolve().parents[1];SITE=ROOT/'site'
class Page(HTMLParser):
 def __init__(self):super().__init__();self.links=[];self.ids=set()
 def handle_starttag(self,tag,attrs):
  a=dict(attrs)
  if 'id' in a:self.ids.add(a['id'])
  for key in ['href','src','poster']:
   if a.get(key):self.links.append(a[key])
pages={p:Page() for p in SITE.rglob('*.html')}
for path,page in pages.items():page.feed(path.read_text())
checks=0
for path,page in pages.items():
 for link in page.links:
  url=urlsplit(link)
  if url.scheme or url.netloc:continue
  assert not url.path.startswith('/'),f'Root-relative link breaks project path: {link}'
  target=(path.parent/unquote(url.path)).resolve() if url.path else path
  if target.is_dir():target=target/'index.html'
  assert target.is_relative_to(SITE.resolve()),f'Outside site: {link}'
  assert target.exists(),f'Missing {link} in {path}'
  if url.fragment and target.suffix=='.html':assert unquote(url.fragment) in pages[target].ids,f'Unknown anchor {link}'
  checks+=1
for path in (SITE/'assets').glob('*.mjs'):
 for rel in re.findall(r"(?:from\s*|import\s*)['\"](\.[^'\"]+)['\"]",path.read_text()):assert (path.parent/rel).is_file(),f'Missing module {rel}'
assert (SITE/'vendor/pyodide/pyodide.asm.wasm').stat().st_size>1000000
assert (ROOT/'video/fonts/OFL-noto-sans-sc.txt').exists()
assert (ROOT/'video/fonts/OFL-jetbrains-mono.txt').exists()
manifest=json.loads((SITE/'media/versions.json').read_text())
for lang,v in manifest.items():
 for key in ['video','poster']:
  p=SITE/v[key];assert p.is_file() and p.stat().st_size>1000
 for caption in v['captionTracks'].values():assert (SITE/caption).read_text().startswith('WEBVTT')
print(f'PASS: {checks} local resource/anchor references, module imports, runtime, licenses and bilingual media paths')
