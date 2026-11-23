import rawTeacher from './teacher.mjs';
const clone=x=>JSON.parse(JSON.stringify(x));
const teacher={...clone(rawTeacher),placement:clone(rawTeacher.starter_float)};
const small={chip:{W:6,H:4,siteW:1,rowH:2,rows:[0,2]},cells:[{id:'A',width:1},{id:'B',width:1}],nets:[['A','B']],fixed_macros:[]};
export const PRESETS={teacher,collision:{...clone(teacher),placement:clone(rawTeacher.starter_illegal)},ties:{...clone(small),placement:{A:{x:2.5,y:1},B:{x:3.5,y:1}}},touching:{...clone(small),placement:{A:{x:1,y:0},B:{x:2,y:0}}},clamp:{...clone(small),cells:[{id:'A',width:2},{id:'B',width:2}],placement:{A:{x:-.6,y:.2},B:{x:5.7,y:2.4}}}};
export function roundEven(x){if(!Number.isFinite(x))throw Error('coordinate must be finite');const f=Math.floor(x),d=x-f;return d===.5?(f%2===0?f:f+1):Math.round(x);}
const close=(a,b)=>Math.abs(a-b)<1e-9;
function validate(data){
 const {chip,cells,placement,nets}=data;if(!chip||chip.siteW!==1||!Number.isFinite(chip.W)||!Number.isFinite(chip.H)||!Number.isFinite(chip.rowH)||chip.rowH<=0||!chip.rows?.length)throw Error('chip grid');
 if(chip.rows.some(y=>!Number.isFinite(y)||y<0||y+chip.rowH>chip.H)||new Set(chip.rows).size!==chip.rows.length)throw Error('row');
 if(new Set(cells.map(c=>c.id)).size!==cells.length)throw Error('duplicate id');
 for(const c of cells){if(!Number.isInteger(c.width)||c.width<=0||c.width>chip.W)throw Error('width');const p=placement[c.id];if(!p||!Number.isFinite(p.x)||!Number.isFinite(p.y))throw Error('coordinate');}
 for(const net of nets)if(net.some(id=>!cells.some(c=>c.id===id)))throw Error('net pin');
 for(const c of data.fixed_macros||[])if(!placement[c.id]||!Number.isFinite(c.x)||!Number.isFinite(c.y))throw Error('fixed coordinate');
}
export function report(data,positions,origin=data.placement){
 const widths=Object.fromEntries(data.cells.map(c=>[c.id,c.width])),ids=data.cells.map(c=>c.id),fixed=Object.fromEntries((data.fixed_macros||[]).map(c=>[c.id,c]));
 let siteAligned=0,rowAligned=0,inBounds=0,fixedAligned=0,displacement=0,movableDisplacement=0;
 const overlaps=[];
 for(const id of ids){const p=positions[id],o=origin[id],w=widths[id],delta=Math.abs(p.x-o.x)+Math.abs(p.y-o.y);displacement+=delta;if(!fixed[id])movableDisplacement+=delta;if(close(p.x,roundEven(p.x)))siteAligned++;if(data.chip.rows.some(y=>close(p.y,y)))rowAligned++;if(p.x>=-1e-9&&p.x+w<=data.chip.W+1e-9&&p.y>=-1e-9&&p.y+data.chip.rowH<=data.chip.H+1e-9)inBounds++;if(fixed[id]&&close(p.x,fixed[id].x)&&close(p.y,fixed[id].y))fixedAligned++;}
 for(let i=0;i<ids.length;i++)for(let j=i+1;j<ids.length;j++){const a=positions[ids[i]],b=positions[ids[j]],dx=Math.min(a.x+widths[ids[i]],b.x+widths[ids[j]])-Math.max(a.x,b.x),dy=Math.min(a.y+data.chip.rowH,b.y+data.chip.rowH)-Math.max(a.y,b.y);if(dx>0&&dy>0)overlaps.push({a:ids[i],b:ids[j],width:dx,height:dy,area:dx*dy});}
 const hpwl=data.nets.reduce((sum,net)=>{if(!net.length)return sum;const xs=net.map(id=>positions[id].x+widths[id]/2),ys=net.map(id=>positions[id].y+data.chip.rowH/2);return sum+Math.max(...xs)-Math.min(...xs)+Math.max(...ys)-Math.min(...ys);},0);
 return {siteAligned,rowAligned,inBounds,fixedAligned,fixedCount:Object.keys(fixed).length,displacement,movableDisplacement,hpwl,overlaps,legal:siteAligned===ids.length&&rowAligned===ids.length&&inBounds===ids.length&&fixedAligned===Object.keys(fixed).length&&overlaps.length===0};
}
export function snap(data){
 validate(data);const positions=clone(data.placement),fixed=Object.fromEntries((data.fixed_macros||[]).map(c=>[c.id,c])),trace=[];
 for(const c of data.cells){const before={...positions[c.id]};let x,y,rounded;
  if(fixed[c.id]){x=fixed[c.id].x;y=fixed[c.id].y;rounded=x;}
  else{rounded=roundEven(before.x);x=Math.max(0,Math.min(data.chip.W-c.width,rounded));y=data.chip.rows.reduce((best,row)=>Math.abs(before.y-row)<Math.abs(before.y-best)?row:best,data.chip.rows[0]);}
  positions[c.id]={x,y};trace.push({id:c.id,before,target:{x,y},rounded,width:c.width,fixed:!!fixed[c.id],displacement:Math.abs(x-before.x)+Math.abs(y-before.y),positions:clone(positions)});
 }
 return {positions,trace,metrics:report(data,positions),before:report(data,data.placement)};
}
