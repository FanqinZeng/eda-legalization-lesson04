from pathlib import Path
import json
ROOT=Path(__file__).resolve().parents[1];presets=json.loads((ROOT/'site/downloads/examples.json').read_text());reference=(ROOT/'site/downloads/reference.py').read_text().split("if __name__=='__main__':")[0]
def example(name):
 return reference+'\ndata=json.loads('+repr(json.dumps(presets[name]))+')\nresult=greedy_snap(data)\nfor key,position in result["positions"].items():print(key,position)\nprint("L1:",round(result["metrics"]["displacement"],6))\nprint("movable L1:",round(result["metrics"]["movableDisplacement"],6))\nprint("HPWL:",round(result["metrics"]["hpwl"],6))\nprint("overlap pairs:",len(result["metrics"]["overlaps"]))\nprint("legal:",result["metrics"]["legal"])\n'
exercise='''# Implement the two primitives; Python round uses ties-to-even.
# 完成两个基础函数；Python round采用等距取偶。
def snap_x(x, width, chip_width):
    # Round first, then clamp the entire width. / 先取整，再为完整宽度留空间。
    raise NotImplementedError("round and clamp")

def nearest_row(y, rows):
    # Keep the first row on an equal-distance tie. / 等距时保留列表第一行。
    raise NotImplementedError("nearest row")

assert snap_x(2.5,1,6)==2
assert snap_x(3.5,1,6)==4
assert snap_x(5.7,2,6)==4
assert snap_x(-0.6,2,6)==0
assert nearest_row(1,[0,2,4])==0
assert nearest_row(1.2,[0,2,4])==2
print("6 checks passed / 6项检查通过")

def greedy_snap(data):
    locked={c["id"]:c for c in data.get("fixed_macros",[])}
    result={}
    for cell in data["cells"]:
        key=cell["id"];p=data["placement"][key]
        if key in locked:result[key]={"x":locked[key]["x"],"y":locked[key]["y"]}
        else:result[key]={"x":snap_x(p["x"],cell["width"],data["chip"]["W"]),"y":nearest_row(p["y"],data["chip"]["rows"])}
    return result
'''
(ROOT/'site/downloads/exercise.py').write_text(exercise)
(ROOT/'site/python/examples.mjs').write_text('export const RUN_TIMEOUT_MS=5000,LIVE_DEBOUNCE_MS=700,MAX_OUTPUT_CHARS=40000;\nexport const EXAMPLES='+json.dumps({'reference':example('teacher'),'asymmetric':example('ties'),'exercise':exercise},ensure_ascii=False)+';\n')
# The committed HTML/controller/CSS are the authoritative, lesson-local workspace.
# Regeneration only changes examples and the exercise; no sibling checkout is read.
print('Built lesson-specific CPython examples from local sources')
