(function(root){
'use strict';
function targetFor(pack,answers){
  const missed=pack.questions.filter(q=>answers.some(a=>a.id===q.id&&!a.correct));
  const counts={};missed.forEach(q=>counts[q.skill]=(counts[q.skill]||0)+1);
  const selected=[...missed].sort((a,b)=>counts[b.skill]-counts[a.skill])[0]||pack.questions[0];
  return {questionId:selected.id,skill:selected.skill,challenge:missed.length===0,missed:missed.map(q=>q.id)};
}
function words(text){return String(text).toLowerCase().replace(/[’‘]/g,"'").replace(/[^a-z0-9'\s]/g,' ').trim().split(/\s+/).filter(Boolean);}
function compareText(input,target){
  const a=words(input),b=words(target),d=Array.from({length:a.length+1},()=>Array(b.length+1).fill(0));
  for(let i=a.length-1;i>=0;i--)for(let j=b.length-1;j>=0;j--)d[i][j]=a[i]===b[j]?1+d[i+1][j+1]:Math.max(d[i+1][j],d[i][j+1]);
  let i=0,j=0;const missing=[],extra=[],matched=[];
  while(i<a.length||j<b.length){if(i<a.length&&j<b.length&&a[i]===b[j]){matched.push(b[j]);i++;j++;}else if(j<b.length&&(i===a.length||d[i][j+1]>=d[i+1][j])){missing.push(b[j++]);}else extra.push(a[i++]);}
  return {exact:a.join(' ')===b.join(' '),missing,extra,matched};
}
function reviewDate(at,days=1){return new Date(new Date(at).getTime()+days*86400000).toISOString();}
const api={targetFor,compareText,reviewDate};if(typeof module!=='undefined'&&module.exports)module.exports=api;else root.TrainerCore=api;
})(typeof window!=='undefined'?window:globalThis);
