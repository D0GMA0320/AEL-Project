(function(root){
'use strict';
function pcmWav(samples){
  const buffer=new ArrayBuffer(44+samples.length*2),v=new DataView(buffer);
  const str=(at,text)=>{for(let i=0;i<text.length;i++)v.setUint8(at+i,text.charCodeAt(i));};
  str(0,'RIFF');v.setUint32(4,36+samples.length*2,true);str(8,'WAVE');str(12,'fmt ');
  v.setUint32(16,16,true);v.setUint16(20,1,true);v.setUint16(22,1,true);v.setUint32(24,16000,true);
  v.setUint32(28,32000,true);v.setUint16(32,2,true);v.setUint16(34,16,true);str(36,'data');v.setUint32(40,samples.length*2,true);
  for(let i=0;i<samples.length;i++){const n=Math.max(-1,Math.min(1,samples[i]));v.setInt16(44+i*2,n<0?n*32768:n*32767,true);}
  return new Uint8Array(buffer);
}
async function wavBase64(blob){
  const Context=window.AudioContext||window.webkitAudioContext;
  const context=new Context();let decoded;
  try{decoded=await context.decodeAudioData(await blob.arrayBuffer());}finally{await context.close();}
  if(decoded.duration<0.5||decoded.duration>30)throw Error('0.5~30초 안으로 모델 문장을 다시 녹음해 주세요.');
  const offline=new OfflineAudioContext(1,Math.ceil(decoded.duration*16000),16000),source=offline.createBufferSource();
  source.buffer=decoded;source.connect(offline.destination);source.start();
  const converted=await offline.startRendering(),bytes=pcmWav(converted.getChannelData(0));let binary='';
  for(let i=0;i<bytes.length;i+=8192)binary+=String.fromCharCode(...bytes.subarray(i,i+8192));
  return btoa(binary);
}
const api={pcmWav,wavBase64};if(typeof module!=='undefined'&&module.exports)module.exports=api;else root.AELPronunciation=api;
})(typeof window!=='undefined'?window:globalThis);
