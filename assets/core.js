(function(root){
  'use strict';
  function chooseFollowups(answers, bank, count=2){
    const missed=[...new Set(answers.filter(a=>!a.correct).map(a=>a.skill))];
    const selected=bank.filter(q=>missed.includes(q.skill));
    return (selected.length?selected:bank.filter(q=>q.challenge)).slice(0,count);
  }
  function recommend(answers){
    if(!answers.length) return '먼저 한 세션을 완료해 주세요.';
    const accuracy=answers.filter(a=>a.correct).length/answers.length;
    const timeout=answers.some(a=>a.timedOut);
    if(timeout) return '시간 초과가 있었습니다. 다음에는 제한 없이 풀고, 정확도가 안정되면 시간을 줄이세요.';
    if(accuracy<0.6) return '스크립트와 해설을 확인한 뒤 0.85배속으로 새 지문을 연습하세요.';
    if(accuracy<0.85) return '현재 난도를 유지하고 오답 유형의 새 문장을 연습하세요.';
    return '새 지문에서도 정답률을 확인하세요. 안정적으로 맞힐 때만 시간 제한을 줄이세요.';
  }
  function validateLesson(l){
    if(!l || typeof l!=='object') throw Error('자료 형식이 올바르지 않습니다.');
    for(const k of ['id','title','level','kind','source','script','translation','goal']) if(typeof l[k]!=='string'||!l[k].trim()) throw Error(k+' 필드가 필요합니다.');
    if(!/^[a-zA-Z0-9_-]{1,60}$/.test(l.id)) throw Error('id는 영문/숫자/-/_ 60자 이내여야 합니다.');
    if(l.script.length>12000) throw Error('지문은 12,000자 이내로 입력해 주세요.');
    if(!Array.isArray(l.questions)||l.questions.length<2||l.questions.length>12) throw Error('문항은 2~12개여야 합니다.');
    const ids=new Set();
    for(const q of l.questions){
      if(!q||typeof q.id!=='string'||ids.has(q.id)) throw Error('문항 id는 고유해야 합니다.'); ids.add(q.id);
      if(!['listen','context'].includes(q.type)||!['detail','inference','tense','agreement','vocabulary'].includes(q.skill)) throw Error('문항 유형/skill을 확인해 주세요.');
      if(!Array.isArray(q.options)||q.options.length<2||q.options.length>4||q.options.some(x=>typeof x!=='string'||!x.trim())||new Set(q.options).size!==q.options.length) throw Error('중복 없는 보기 2~4개가 필요합니다.');
      if(!Number.isInteger(q.answer)||q.answer<0||q.answer>=q.options.length) throw Error('정답 번호가 범위를 벗어났습니다.');
      for(const k of ['prompt','explanation','evidence']) if(typeof q[k]!=='string'||!q[k].trim()) throw Error('문항 '+k+'가 필요합니다.');
    }
    if(!l.questions.some(q=>q.type==='listen')||!l.questions.some(q=>q.type==='context')) throw Error('듣기와 문맥 문항을 모두 포함해 주세요.');
    return true;
  }
  const api={chooseFollowups,recommend,validateLesson};
  if(typeof module!=='undefined'&&module.exports) module.exports=api;
  else root.AELCore=api;
})(typeof window!=='undefined'?window:globalThis);
