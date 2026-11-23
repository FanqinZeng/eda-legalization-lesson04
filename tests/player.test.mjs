import test from 'node:test';import assert from 'node:assert/strict';
import {mapPlaybackTime} from '../site/assets/player.mjs';
test('voice changes map by semantic scene id, including reordered manifests',()=>{
 const a=[{id:'intro',start:0,end:10},{id:'bend',start:10,end:20}];
 const b=[{id:'bend',start:0,end:20},{id:'intro',start:20,end:40}];
 assert.equal(mapPlaybackTime(15,a,b),10);
});
test('empty timelines and invalid playback position are safe',()=>{assert.equal(mapPlaybackTime(NaN,[],[]),0);assert.equal(mapPlaybackTime(0,[],[]),0);});
