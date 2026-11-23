import {writeFileSync} from 'node:fs';import {snap,PRESETS} from '../site/assets/engine.mjs';
const results=Object.fromEntries(Object.entries(PRESETS).map(([key,data])=>[key,snap(data)]));
writeFileSync(new URL('../video/data.json',import.meta.url),JSON.stringify({presets:PRESETS,results},null,2)+'\n');writeFileSync(new URL('../site/downloads/examples.json',import.meta.url),JSON.stringify(PRESETS,null,2)+'\n');console.log('Exported greedy-snap fixtures and actual traces');
