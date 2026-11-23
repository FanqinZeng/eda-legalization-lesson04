"""Independent greedy snap with Python ties-to-even and cell-center HPWL.
Coordinates are lower-left. Each cell has chip.rowH height; all nets have weight 1.
"""
import json,math,sys

def measure(data, positions, origin=None):
    origin=data['placement'] if origin is None else origin
    widths={c['id']:c['width'] for c in data['cells']};fixed={c['id']:c for c in data.get('fixed_macros',[])};ids=list(widths);chip=data['chip']
    aligned=lambda a,b:abs(a-b)<1e-9
    site=sum(aligned(p['x'],round(p['x'])) for p in positions.values())
    rows=sum(any(aligned(p['y'],r) for r in chip['rows']) for p in positions.values())
    bounds=sum(p['x']>=-1e-9 and p['x']+widths[k]<=chip['W']+1e-9 and p['y']>=-1e-9 and p['y']+chip['rowH']<=chip['H']+1e-9 for k,p in positions.items())
    locked=sum(aligned(positions[k]['x'],v['x']) and aligned(positions[k]['y'],v['y']) for k,v in fixed.items())
    overlaps=[]
    for i,a in enumerate(ids):
        for b in ids[i+1:]:
            pa,pb=positions[a],positions[b]
            dx=min(pa['x']+widths[a],pb['x']+widths[b])-max(pa['x'],pb['x']);dy=min(pa['y']+chip['rowH'],pb['y']+chip['rowH'])-max(pa['y'],pb['y'])
            if dx>0 and dy>0:overlaps.append({'a':a,'b':b,'area':dx*dy})
    distances={k:abs(p['x']-origin[k]['x'])+abs(p['y']-origin[k]['y']) for k,p in positions.items()}
    hpwl=0
    for net in data['nets']:
        if not net:continue
        xs=[positions[k]['x']+widths[k]/2 for k in net];ys=[positions[k]['y']+chip['rowH']/2 for k in net]
        hpwl+=max(xs)-min(xs)+max(ys)-min(ys)
    return {'displacement':sum(distances.values()),'movableDisplacement':sum(v for k,v in distances.items() if k not in fixed),'hpwl':hpwl,'overlaps':overlaps,'siteAligned':site,'rowAligned':rows,'inBounds':bounds,'fixedAligned':locked,'legal':site==len(ids) and rows==len(ids) and bounds==len(ids) and locked==len(fixed) and not overlaps}

def greedy_snap(data):
    chip=data['chip'];fixed={c['id']:c for c in data.get('fixed_macros',[])};result={}
    for cell in data['cells']:
        key=cell['id'];p=data['placement'][key]
        if not all(math.isfinite(p[a]) for a in ['x','y']):raise ValueError('coordinate')
        if key in fixed:result[key]={'x':fixed[key]['x'],'y':fixed[key]['y']}
        else:
            x=max(0,min(chip['W']-cell['width'],round(p['x'])))
            y=min(chip['rows'],key=lambda r:abs(r-p['y']))
            result[key]={'x':x,'y':y}
    return {'positions':result,'metrics':measure(data,result)}

if __name__=='__main__':print(json.dumps([greedy_snap(d) for d in json.load(sys.stdin)]))
