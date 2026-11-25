const {test}=require('node:test');
const assert=require('node:assert/strict');
const fs=require('node:fs'),path=require('node:path'),vm=require('node:vm');
const C=require('../assets/trainer-core.js');
const D=JSON.parse(fs.readFileSync(path.join(__dirname,'../assets/trainer-data.json'),'utf8'));
const source=fs.readFileSync(path.join(__dirname,'../assets/trainer.js'),'utf8');
const flush=()=>new Promise(resolve=>setImmediate(resolve));
function draft(stage,allCorrect=false){
  const p=D.packs.find(p=>p.id==='toeic3');
  const answers=p.questions.map((q,i)=>({id:q.id,pick:!allCorrect&&i===0?3:q.answer,correct:allCorrect||i!==0,skill:q.skill}));
  return {id:'qa-flow',version:D.version,pack:p.id,contentSnapshot:p,accent:'AU',stage,index:2,diagnosticDone:true,answers,events:[],target:C.targetFor(p,answers),startedAt:new Date().toISOString()};
}
async function harness(session,{apiFails=false}={}){
  let html='',storage=JSON.stringify({history:[],draft:session,pack:session.pack,accent:'AU',exam:'TOEIC'}),fields={};
  const handlers={},windowHandlers={},requests=[];
  const app={get innerHTML(){return html;},set innerHTML(v){html=v;fields={};},addEventListener(name,fn){handlers[name]=fn;}};
  const query=selector=>{
    if(selector==='#app')return app;
    if(selector==='#toast')return {textContent:'',className:''};
    const id=selector.slice(1);
    if(!html.includes(`id="${id}"`))return null;
    return fields[id]||=( {id,value:'',dataset:{},checked:false} );
  };
  const location={hash:'#session'};
  const window={AEL_TRAINER:D,TrainerCore:C,AEL_AUDIO:{},scrollTo(){},addEventListener(n,f){windowHandlers[n]=f;}};
  vm.runInNewContext(source,{window,document:{querySelector:query,querySelectorAll:()=>[]},location,
    localStorage:{getItem:()=>storage,setItem:(k,v)=>{storage=v;}},
    fetch:async(url,opts)=>{if(url==='/api/health')return {status:200,json:async()=>({openaiConfigured:true,pronunciationConfigured:true})};
      const body=JSON.parse(opts.body);requests.push({url,body});return {ok:!apiFails,json:async()=>apiFails?{error:'QA provider unavailable'}:{text:'QA: eleven은 시작 시각이고 도착은 10분 전입니다.',request:body,rawResponseText:'QA raw output',requestId:'qa'}};},
    setTimeout:()=>0,clearTimeout(){},AbortSignal,crypto:{randomUUID:()=> 'qa-new'},URL,Blob,console,navigator:{}});
  await flush();
  return {get html(){return html;},state:()=>JSON.parse(storage),requests,
    input(id,value){const field=query('#'+id);assert.ok(field,`Missing field ${id}`);field.value=value;handlers.input({target:field});},
    async click(action){const buttons=[...html.matchAll(/<button\b([^>]*)>/g)];const found=buttons.find(m=>m[1].includes(`data-action="${action}"`));assert.ok(found,`Missing button ${action}`);assert.ok(!/\bdisabled\b/.test(found[1]),`Disabled ${action}`);handlers.click({target:{closest:()=>({disabled:false,dataset:{action}})}});await flush();},
    route(hash){location.hash=hash;windowHandlers.hashchange();}
  };
}
test('perfect diagnostic saves completion without feedback, recheck or scheduled review',async()=>{
  const ui=await harness(draft(0,true));await ui.click('diag-continue');
  const h=ui.state().history[0];assert.equal(h.completed,true);assert.equal(h.target,null);assert.equal(h.reviewDue,null);assert.equal(h.retryChecked,undefined);assert.equal(ui.requests.length,0);
  assert.match(ui.html,/모두 맞혔어요/);ui.route('#history');assert.doesNotMatch(ui.html,/data-action="review"/);assert.match(ui.html,/재확인 없음/);
});
test('resumed old all-correct extension is completed without another exercise',async()=>{
  const s=draft(4,true);s.target={questionId:'t3-1',challenge:true,missed:[]};
  const ui=await harness(s);assert.equal(ui.state().history[0].target,null);assert.doesNotMatch(ui.html,/data-action="record"/);
});
test('step 2 sends one reason and the selected option, then allows continuing',async()=>{
  const ui=await harness(draft(1));assert.equal((ui.html.match(/<textarea/g)||[]).length,1);
  ui.input('reason','eleven을 듣고 시작 시각을 골랐어요.');await ui.click('coach');
  assert.deepEqual(ui.requests[0].body,{mode:'reason-feedback',pack:'toeic3',contentVersion:D.version,questionId:'t3-1',selectedAnswer:3,reason:'eleven을 듣고 시작 시각을 골랐어요.'});
  assert.match(ui.html,/QA: eleven/);assert.doesNotMatch(ui.html,/id="revision"|id="coach-question"/);
  await ui.click('to-dictation');assert.equal(ui.state().draft.stage,2);
});
test('step 2 provider failure offers a visible prepared explanation and continuation',async()=>{
  const ui=await harness(draft(1),{apiFails:true});ui.input('reason','I heard eleven.');await ui.click('coach');assert.match(ui.html,/QA provider unavailable/);assert.match(ui.html,/AI 연결 대신 준비된 해설/);await ui.click('to-dictation');assert.equal(ui.state().draft.stage,2);
});
test('correct first dictation renders no correction field and continues immediately',async()=>{
  const s=draft(2),ui=await harness(s);ui.input('dictation',s.contentSnapshot.questions[0].dictation);await ui.click('check-dictation');assert.doesNotMatch(ui.html,/id="dictationRetry"|data-action="dictation-retry"/);await ui.click('to-expression');assert.equal(ui.state().draft.stage,3);assert.equal(ui.state().draft.dictationRetryResult,null);
});
test('incorrect dictation still renders and checks a correction',async()=>{
  const s=draft(2),ui=await harness(s);ui.input('dictation','Please ask everyone to arrive early.');await ui.click('check-dictation');assert.match(ui.html,/id="dictationRetry"/);ui.input('dictationRetry',s.contentSnapshot.questions[0].dictation);await ui.click('dictation-retry');await ui.click('to-expression');assert.equal(ui.state().draft.stage,3);
});
test('step 5 can continue without writing, checklist or microphone',async()=>{
  const ui=await harness(draft(4));assert.doesNotMatch(ui.html,/<textarea|type="checkbox"/);assert.match(ui.html,/data-action="record"/);assert.match(ui.html,/data-action="assess"/);await ui.click('to-retry');assert.equal(ui.state().draft.stage,5);assert.equal(ui.requests.length,0);
});
