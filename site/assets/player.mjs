/** Keep the same authored scene and its relative progress across voice timelines. */
export function mapPlaybackTime(time,from,to){
 if(!Number.isFinite(time)||time<=0||!from?.length||!to?.length)return 0;
 if(time>=from.at(-1).end)return to.at(-1).end;
 const i=from.findIndex(s=>time<s.end);if(i<0||!to[i])return 0;
 const a=from[i],b=to.find(s=>s.id&&s.id===a.id)||to[i],fraction=Math.max(0,Math.min(1,(time-a.start)/(a.end-a.start)));
 return b.start+(b.end-b.start)*fraction;
}
export async function initLessonPlayer(root=document){
 const $=s=>root.querySelector(s),video=$('#lesson-video'),select=$('#voice-language'),track=$('#lesson-captions');
 const tr=(zh,en)=>root.documentElement.lang.startsWith('en')?en:zh;
 let versions,active='zh',request=0,pending=null,captionChoice='bilingual';
 const captionSelect=$('#caption-mode');
 function captionSource(lang){return versions[lang].captionTracks[captionChoice==='off'?'bilingual':captionChoice];}
 function applyCaption(lang){
  track.src=captionSource(lang);track.srclang=captionChoice==='bilingual'?'mul':captionChoice==='en'?'en-US':'zh-CN';
  track.label=captionChoice==='bilingual'?'中英双语 / Chinese + English':captionChoice==='en'?'English captions':'中文字幕';
  track.track.mode=captionChoice==='off'?'disabled':'showing';
 }
 const status=$('#video-language-status');select.disabled=true;
 $('#video-speed').onchange=e=>{video.playbackRate=Number(e.target.value);if(pending)pending.speed=video.playbackRate;};
 video.addEventListener('error',()=>{$('#video-status').textContent=tr('播放器暂时无法载入。可下载当前语言MP4或阅读文字稿。','The player could not load. Download the current MP4 or continue with the transcript.');});
 function resources(lang){
  const v=versions[lang];$('#download-video').href=v.video;$('#download-video').textContent=`${v.label} MP4`;
  $('#download-captions').href=captionSource(lang);$('#download-captions').textContent=`${captionChoice==='zh'?'中文':captionChoice==='en'?'English':v.trackLabel} VTT`;
  $('#video-transcript').href=v.transcript;$('#video-transcript').textContent=tr('在线文字稿','Read transcript');
  $('#chapters').innerHTML=v.chapters.map((c,i)=>`<button data-chapter="${i}"><span>${Math.floor(c.start/60)}:${String(Math.floor(c.start%60)).padStart(2,'0')}</span>${c.title}</button>`).join('');
  $('#chapters').querySelectorAll('button').forEach((button,i)=>button.onclick=()=>{
   const t=v.chapters[i].start;if(pending){pending.time=t;pending.resume=true;return;}
   video.currentTime=t;const chapterRequest=request;video.play().catch(()=>{if(chapterRequest!==request)return;$('#video-status').textContent=tr('章节已定位，点击播放器开始。','Chapter selected. Press play to start.');});
  });
 }
 function switchVoice(lang){
  if(!versions[lang])return;
  const token=++request,from=pending?.lang||active,time=pending?.time??video.currentTime;
  const state={lang,time:mapPlaybackTime(time,versions[from].scenes,versions[lang].scenes),resume:pending?.resume??!video.paused,speed:pending?.speed??video.playbackRate,captionMode:pending?.captionMode??track.track?.mode??'showing'};
  pending=state;video.pause();resources(lang);status.textContent=tr('正在载入配音：','Loading voice: ')+versions[lang].label;$('#video-status').textContent='';
  for(const t of video.textTracks)t.mode='disabled';
  applyCaption(lang);
  video.poster=versions[lang].poster;
  video.addEventListener('loadedmetadata',()=>{
   if(token!==request)return;
   active=lang;video.dataset.language=lang;video.currentTime=Math.min(state.time,Math.max(0,video.duration-.01));video.playbackRate=state.speed;
   if(track.track)track.track.mode=state.captionMode;select.value=lang;status.textContent=tr('当前配音：','Current voice: ')+`${versions[lang].label} · ${versions[lang].voice}`;pending=null;
   if(state.resume)video.play().catch(()=>{if(token!==request)return;$('#video-status').textContent=tr('语言已切换，点击播放器继续播放。','Voice changed. Press play to continue.');});
  },{once:true});
  video.src=versions[lang].video;video.load();
 }
 function initializeVoice(lang){
  active=lang;select.value=lang;video.preload='none';video.src=versions[lang].video;video.poster=versions[lang].poster;video.dataset.language=lang;
  resources(lang);applyCaption(lang);status.textContent=tr('当前配音：','Current voice: ')+versions[lang].label+' · '+versions[lang].voice;
 }
 try{
  const r=await fetch('media/versions.json');if(!r.ok)throw Error('versions');versions=await r.json();
  initializeVoice(root.documentElement.lang.startsWith('en')?'en':'zh');select.disabled=false;
  select.onchange=e=>switchVoice(e.target.value);
  if(captionSelect)captionSelect.onchange=e=>{captionChoice=e.target.value;applyCaption(pending?.lang||active);resources(pending?.lang||active);if(pending)pending.captionMode=captionChoice==='off'?'disabled':'showing';};
  // Interface changes select the matching rendered film, including its pictures.
  // The voice picker can still override that choice independently afterwards.
  root.addEventListener('lessonlanguagechange',e=>{
   const lang=e.detail.language;if(versions[lang]&&lang!==(pending?.lang||active))switchVoice(lang);else{resources(active);status.textContent=tr('当前配音：','Current voice: ')+versions[active].label;}
  });
 }catch{status.textContent=tr('双语影片资料暂时无法载入。','Bilingual film metadata could not load.');}
}
