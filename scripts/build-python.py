from pathlib import Path
import json
ROOT=Path(__file__).resolve().parents[1];BASE=ROOT.parent/'eda-congestion-lesson05';presets=json.loads((ROOT/'site/downloads/examples.json').read_text());reference=(ROOT/'site/downloads/reference.py').read_text().split("if __name__=='__main__':")[0]
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
replacements={
 'Congestion Lesson 05':'Legalization Lesson 04','CONGESTION · LESSON 05':'LEGALIZATION · LESSON 04','congestion05-':'legalization04-',
 '逐格重算概率L路径，用真正的Python验证端点、转角与溢出。':'编辑greedy snap，用真正的Python核对取偶、边界、位移和重叠。',
 'Recompute probabilistic L routes and verify endpoints, bends and overflow with real Python.':'Edit greedy snap and verify ties, bounds, displacement and overlap with real Python.',
 '对角黄金例：总需求7，两个端点各1，转角0.5；容量0.6时总溢出0.8。矩阵按列存储，打印时y向上。':'教师黄金例：全体L1=4.4，可移动L1=3.8，中心HPWL=32，仍有3对重叠。坐标是cell左下角。',
 'Diagonal golden: total demand 7, endpoint 1, bend 0.5; total overflow 0.8 at capacity 0.6. Matrices are x-major; printed rows increase upward.':'Teacher golden: all-cell L1=4.4, movable-only L1=3.8, center HPWL=32, and three overlapping pairs. Coordinates denote cell lower-left corners.',
 '独立参考 · 对角两点':'独立参考 · 教师浮点例','Independent reference · Diagonal pair':'Independent reference · Teacher floats','三pin中心星形':'半整数与行等距','Three-pin center star':'Half-integer and row ties'}
for name in ['index.html','workspace.mjs','workspace.css']:
 text=(BASE/'site/python'/name).read_text()
 for a,b in replacements.items():text=text.replace(a,b)
 (ROOT/'site/python'/name).write_text(text)
print('Built lesson-specific CPython examples with retained BFCache recovery')
