"""Lesson-specific greedy-snap drawings; shared v2 media/timeline pipeline."""
from pathlib import Path
import json,math,argparse,importlib.util
from PIL import ImageDraw
from film_common import *
ROOT=Path(__file__).resolve().parents[1];p=argparse.ArgumentParser();p.add_argument('--lang',choices=['zh','en'],default='zh');p.add_argument('--stills',action='store_true');p.add_argument('--sample',action='store_true');p.add_argument('--encode-only',action='store_true');a=p.parse_args();film=Film(ROOT,a.lang)
DATA=json.loads((ROOT/'video/data.json').read_text());R=DATA['results'];P=DATA['presets'];LANG=a.lang
spec=importlib.util.spec_from_file_location('reference',ROOT/'site/downloads/reference.py');reference=importlib.util.module_from_spec(spec);spec.loader.exec_module(reference)
def tr(zh,en):return zh if LANG=='zh' else en
def tween(before,after,t):return {k:{axis:mix(p[axis],after[k][axis],t) for axis in ['x','y']} for k,p in before.items()}
def dotted_rect(d,box,color):
    x0,y0,x1,y1=box
    for x in range(round(x0),round(x1),20):d.line((x,y0,min(x+11,x1),y0),fill=color,width=2);d.line((x,y1,min(x+11,x1),y1),fill=color,width=2)
    for y in range(round(y0),round(y1),20):d.line((x0,y,x0,min(y+11,y1)),fill=color,width=2);d.line((x1,y,x1,min(y+11,y1)),fill=color,width=2)
def cells(im,data,positions,x=100,y=302,u=72,highlight=None,net=None):
    chip=data['chip'];d=ImageDraw.Draw(im);rgba=ImageDraw.Draw(im,'RGBA');width=chip['W']*u;height=chip['H']*u;fixed={c['id'] for c in data.get('fixed_macros',[])};m=reference.measure(data,positions);hit={k for o in m['overlaps'] for k in [o['a'],o['b']]}
    for row in chip['rows']:
        yy=y+(chip['H']-row-chip['rowH'])*u;d.rectangle((x,yy,x+width,yy+chip['rowH']*u),fill=PANEL);film.text(im,'y='+n(row),x-66,yy+chip['rowH']*u-34,22,MUTED,True)
    for i in range(chip['W']+1):
        xx=x+i*u;d.line((xx,y,xx,y+height),fill=FAINT,width=1)
        if i%2==0:film.text(im,i,xx-6,y+height+15,23,MUTED,True)
    d.rectangle((x,y,x+width,y+height),outline=MUTED,width=2)
    for i,c in enumerate(data['cells']):
        pos=positions[c['id']];xx=x+pos['x']*u;yy=y+(chip['H']-pos['y']-chip['rowH'])*u;w=c['width']*u;h=chip['rowH']*u;box=(xx,yy,xx+w,yy+h);color=IVORY if c['id']==highlight else GOLD if c['id'] in hit else '#86a9e0' if c['id'] in fixed else TEAL
        rgba.rectangle(box,fill=(118,203,181,35));
        if c['id'] in fixed:dotted_rect(d,box,color)
        else:d.rectangle(box,outline=color,width=3)
        labelx=xx+w-44 if i%2 else xx+12;labely=yy+84 if i%2 else yy+17;film.text(im,c['id'],labelx,labely,34,IVORY,True)
    if net:
        widths={c['id']:c['width'] for c in data['cells']};xs=[positions[k]['x']+widths[k]/2 for k in net];ys=[positions[k]['y']+chip['rowH']/2 for k in net];box=(x+min(xs)*u,y+(chip['H']-max(ys))*u,x+max(xs)*u,y+(chip['H']-min(ys))*u);d.rectangle(box,outline='#86a9e0',width=3)
        for xx,yy in zip(xs,ys):cx=x+xx*u;cy=y+(chip['H']-yy)*u;d.ellipse((cx-5,cy-5,cx+5,cy+5),fill='#86a9e0')
    return m
KEYS={
 'hook':('site和row对齐，不等于非重叠。','Site and row alignment do not imply non-overlap.'),
 'site':('每个cell独立取整，不检查位置是否空闲。','Each cell rounds independently, without an occupancy check.'),
 'row':('坐标是左下角；行高也是cell高度。','Coordinates are lower-left corners; row height is cell height.'),
 'collision':('A/B、A/C、B/C：三对真实重叠。','A/B, A/C, B/C: three actual overlapping pairs.'),
 'clamp':('x′ ∈ [0, W − w]','x′ ∈ [0, W − w]'),
 'fixed':('固定坐标来自约束；草图与约束不一致需明确说明。','Fixed positions come from constraints; draft inconsistencies must be explicit.'),
 'displacement':('计数范围不同：4.4 与 3.8。','Different counting scopes: 4.4 and 3.8.'),
 'hpwl':('HPWL从36降到32，仍有三对重叠。','HPWL falls from 36 to 32; three overlaps remain.'),
 'ties':('Python round与JS Math.round的半整数规则不同。','Python round and JS Math.round have different halfway rules.'),
 'touching':('严格的正面积相交；接触边界不算重叠。','Require positive-area intersection; touching an edge is allowed.'),
 'limits':('吸附是第一步，不是完整合法化器。','Snapping is a first step, not a complete legalizer.'),
 'close':('对齐、位移、线长、合法性：分开解释。','Explain alignment, displacement, wirelength and legality separately.')}
assert abs(R['teacher']['metrics']['displacement']-4.4)<1e-9 and R['teacher']['metrics']['hpwl']==32 and len(R['teacher']['metrics']['overlaps'])==3
def panel(im,items,x=1180,y=320,gap=144):
    for i,(value,label,color) in enumerate(items):film.text(im,value,x,y+i*gap,73,color,True);film.paragraph(im,label,x,y+i*gap+83,620,31,MUTED)
def frame(t):
    im,s=film.frame_shell(t);kind=s['kind'];local=t-s['start'];phase=local/s['duration'];q=ease(local/5);data=P['teacher'];before=data['placement'];after=R['teacher']['positions'];positions=after;highlight=None;net=None
    if kind=='hook':positions=tween(before,after,q)
    elif kind=='site':
        positions={k:dict(v) for k,v in before.items()}
        for k in ['A','B']:positions[k]['x']=mix(before[k]['x'],after[k]['x'],q)
        highlight='A' if phase<.5 else 'B'
    elif kind=='row':
        positions={k:dict(v) for k,v in before.items()}
        for k in ['A','B']:positions[k]['x']=after[k]['x'];positions[k]['y']=mix(before[k]['y'],after[k]['y'],q)
        highlight='A'
    elif kind=='clamp':data=P['clamp'];positions=tween(data['placement'],R['clamp']['positions'],q)
    elif kind=='fixed':positions={k:dict(v) for k,v in after.items()};positions['D']={axis:mix(before['D'][axis],after['D'][axis],q) for axis in ['x','y']};highlight='D'
    elif kind=='ties':data=P['ties'];positions=tween(data['placement'],R['ties']['positions'],q)
    elif kind=='touching':data=P['touching'];positions=R['touching']['positions']
    elif kind=='hpwl':net=data['nets'][min(5,int(phase*6))]
    m=cells(im,data,positions,highlight=highlight,net=net)
    if kind=='hook':panel(im,[(str(m['siteAligned'])+'/6',tr('site 对齐','site aligned'),TEAL),(str(len(m['overlaps'])),tr('正面积重叠对','positive-area overlapping pairs'),GOLD)])
    elif kind=='site':panel(im,[('3.7 → 4',tr('A 的目标 x','A’s target x'),TEAL),('4.1 → 4',tr('B 的目标 x','B’s target x'),GOLD)])
    elif kind=='row':panel(im,[('1.2 → 2',tr('A 的目标 row bottom','A’s target row bottom'),TEAL),('0.8 < 1.2',tr('到行2比到行0更近','row two is closer than row zero'),GOLD)])
    elif kind=='collision':
        panel(im,[('A / B',tr('面积4','area 4'),GOLD),('A / C',tr('面积2','area 2'),TEAL),('B / C',tr('面积2','area 2'),GOLD)],gap=142)
    elif kind=='clamp':panel(im,[('W=6, w=2',tr('完整宽度必须进墙','the full width must fit'),TEAL),('5.7 → 6 → 4',tr('先取整，再钳制','round, then clamp'),GOLD),('[0, 4]',tr('允许的左下角 x','allowed lower-left x'),TEAL)],gap=142)
    elif kind=='fixed':panel(im,[('D = (8,4)',tr('锁定约束','locked constraint'),TEAL),('0.4 + 0.2',tr('原浮点草图的恢复距离','restoration from the float draft'),GOLD),('= 0.6',tr('不是优化固定宏','not optimization of a fixed macro'),TEAL)],gap=142)
    elif kind=='displacement':
        panel(im,[('4.4',tr('全体单元 L1','all-cell L1'),TEAL),('3.8',tr('只计 movable','movable-only L1'),GOLD),('0.6',tr('固定D恢复的差额','fixed-D restoration difference'),TEAL)],gap=142)
        for i,item in enumerate(R['teacher']['trace']):film.text(im,item['id']+' '+n(item['displacement']),106+i*157,780,26,MUTED,True)
    elif kind=='hpwl':
        panel(im,[('36 → 32',tr('总中心 HPWL','total cell-center HPWL'),TEAL),('3',tr('仍然存在的重叠对','overlapping pairs still remain'),GOLD)])
        widths={c['id']:c['width'] for c in data['cells']};xs=[positions[k]['x']+widths[k]/2 for k in net];ys=[positions[k]['y']+data['chip']['rowH']/2 for k in net];film.text(im,'net '+'–'.join(net)+' / HPWL '+n(max(xs)-min(xs)+max(ys)-min(ys)),110,780,28,'#86a9e0',True)
    elif kind=='ties':panel(im,[('2.5 → 2',tr('Python / 本站 JS','Python / this JS engine'),TEAL),('2.5 → 3',tr('原生 JS Math.round','native JS Math.round'),GOLD),('y=1 → 0',tr('行等距：列表先出现者','row tie: first listed row'),TEAL)],gap=142)
    elif kind=='touching':
        panel(im,[('A | B',tr('仅共享边界','a shared edge only'),TEAL),('area = 0',tr('没有正面积重叠','no positive-area overlap'),GOLD),('LEGAL',tr('本课检查全部通过','all lesson checks pass'),TEAL)],gap=142)
    elif kind=='limits':
        for i,(label,value) in enumerate([(tr('site','site'),m['siteAligned']==6),(tr('row','row'),m['rowAligned']==6),(tr('边界','bounds'),m['inBounds']==6),(tr('fixed','fixed'),m['fixedAligned']==1),(tr('非重叠','non-overlap'),not m['overlaps'])]):film.text(im,('✓ ' if value else '× ')+label,1210,300+i*94,44,TEAL if value else GOLD)
    elif kind=='close':panel(im,[('4.4 / 3.8',tr('明确位移统计范围','state the displacement scope'),TEAL),('HPWL 32',tr('并不代表合法','does not establish legality'),GOLD),('3 overlaps',tr('指出下一步要解决什么','identify what the next step must solve'),TEAL)],gap=142)
    film.text(im,KEYS[kind][0 if LANG=='zh' else 1],100,814,28,MUTED)
    return im
if not a.encode_only:film.output_materials(frame)
print(f'Timeline: {film.duration:.2f}s / {len(film.scenes)} scenes',flush=True)
if a.stills:film.stills(frame)
else:film.encode(frame,sample=a.sample)
