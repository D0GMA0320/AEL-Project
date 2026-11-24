const assert = require('node:assert/strict');
const fs = require('node:fs');
const vm = require('node:vm');
const path = require('node:path');
const core = require('../assets/core.js');
const context = {window:{}};
vm.runInNewContext(fs.readFileSync(path.join(__dirname,'../assets/data.js'),'utf8'),context);
const data = JSON.parse(JSON.stringify(context.window.AEL_DATA));
let count=0;
function test(name, fn){fn();count++;console.log('PASS',name);}
test('all built-in lessons meet schema',()=>data.lessons.forEach(l=>core.validateLesson(l)));
test('answer evidence and IDs are present and unique',()=>{
  const ids=data.lessons.flatMap(l=>l.questions.map(q=>q.id));assert.equal(new Set(ids).size,ids.length);
  data.lessons.forEach(l=>l.questions.forEach(q=>assert.ok(q.evidence&&q.options[q.answer])));
});
test('poor equal scores never recommend increased difficulty',()=>assert.ok(core.recommend([{correct:false},{correct:false}]).includes('0.85')));
test('timeouts prioritize untimed practice',()=>assert.ok(core.recommend([{correct:false,timedOut:true},{correct:true}]).includes('제한 없이')));
test('followups target the actual missed skills',()=>assert.deepEqual(core.chooseFollowups([{correct:false,skill:'agreement'},{correct:true,skill:'tense'}],data.followups).map(q=>q.skill),['agreement']));
test('all-correct sessions receive new challenge questions',()=>assert.ok(core.chooseFollowups([{correct:true,skill:'tense'}],data.followups).every(q=>q.challenge)));
test('followups are capped at two',()=>assert.equal(core.chooseFollowups(data.followups.map(q=>({skill:q.skill,correct:false})),data.followups).length,2));
test('invalid answer index is rejected',()=>{const l=structuredClone(data.lessons[0]);l.questions[0].answer=99;assert.throws(()=>core.validateLesson(l));});
test('duplicate choices are rejected',()=>{const l=structuredClone(data.lessons[0]);l.questions[0].options=['same','same'];assert.throws(()=>core.validateLesson(l));});
test('missing listening or context phase is rejected',()=>{const l=structuredClone(data.lessons[0]);l.questions=l.questions.filter(q=>q.type==='context');assert.throws(()=>core.validateLesson(l));});
test('unsafe lesson filename IDs are rejected',()=>{const l=structuredClone(data.lessons[0]);l.id='../secret';assert.throws(()=>core.validateLesson(l));});
test('audio snapshot exactly matches UI content',()=>assert.deepEqual(JSON.parse(fs.readFileSync(path.join(__dirname,'../assets/lessons.json'),'utf8')),data));
console.log(`${count} tests passed.`);
