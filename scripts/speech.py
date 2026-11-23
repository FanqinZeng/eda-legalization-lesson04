"""Cache actual bilingual narration at semantic-unit granularity."""
import asyncio,json,hashlib,argparse
from pathlib import Path
import edge_tts
ROOT=Path(__file__).resolve().parents[1];VOICES={'zh':'zh-CN-XiaoxiaoNeural','en':'en-US-JennyNeural'}
async def main(languages):
    story=json.loads((ROOT/'video/story.json').read_text());sem=asyncio.Semaphore(3)
    async def one(lang,scene,unit,index):
        folder=ROOT/'video/audio'/lang;folder.mkdir(parents=True,exist_ok=True)
        path=folder/f'{scene["id"]}-{index}.mp3';meta=path.with_suffix('.json');words=unit[lang];digest=hashlib.sha256((VOICES[lang]+words).encode()).hexdigest()
        if path.exists() and meta.exists() and json.loads(meta.read_text()).get('digest')==digest:return
        async with sem:
            for attempt in range(3):
                try:await edge_tts.Communicate(words,VOICES[lang]).save(str(path));break
                except Exception:
                    if attempt==2:raise
                    await asyncio.sleep(1+attempt)
            meta.write_text(json.dumps({'digest':digest,'voice':VOICES[lang],'text':words,'semantic_id':f'{scene["id"]}-{index}'},ensure_ascii=False,indent=2)+'\n')
            print(f'{lang} {scene["id"]}-{index}',flush=True)
    await asyncio.gather(*(one(lang,s,u,i) for lang in languages for s in story for i,u in enumerate(s['units'])))
if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--lang',choices=['zh','en','both'],default='both');a=p.parse_args();asyncio.run(main(['zh','en'] if a.lang=='both' else [a.lang]))
