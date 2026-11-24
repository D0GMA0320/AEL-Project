window.AEL_DATA = {
  version: '2.0.0',
  provenance: 'AI-assisted draft prepared in Codex on 2026-11-24. Exact underlying model ID not exposed to this implementation. Human content review and classroom pilot pending. These are original practice texts, not authentic speeches or official TOEIC/IELTS items.',
  lessons: [
    {
      id:'meeting',title:'The meeting has moved',level:'B1–B2',kind:'Business conversation',source:'Original AI-assisted practice dialogue · not an official TOEIC item',
      goal:'일정 변경의 이유와 시간을 파악하고, 시제와 어휘를 문맥에 적용하기',
      script:'Alex: Hi, Morgan. Is the client meeting still at ten?\nMorgan: It has been moved to eleven because the client’s train is delayed.\nAlex: Should I tell the design team?\nMorgan: Yes, please. They have already prepared the samples, but they need to bring them to Room Four instead of Room Two.\nAlex: All right. I’ll send an updated invitation now.\nMorgan: Thanks. Please ask everyone to arrive ten minutes early so we can check the projector.',
      translation:'Alex: Morgan, 고객 미팅은 여전히 10시인가요?\nMorgan: 고객의 기차가 지연되어 11시로 변경됐어요.\nAlex: 디자인팀에 알려야 할까요?\nMorgan: 네. 샘플은 이미 준비했지만 2번 방 대신 4번 방으로 가져와야 해요.\nAlex: 지금 수정된 초대장을 보낼게요.\nMorgan: 프로젝터를 확인할 수 있도록 모두 10분 일찍 와 달라고 해 주세요.',
      questions:[
        {id:'meeting-1',type:'listen',skill:'detail',prompt:'Why was the meeting moved?',options:['The projector is broken.','The client’s train is delayed.','The samples are missing.'],answer:1,explanation:'변경 이유는 고객의 기차 지연입니다. 프로젝터는 미리 확인할 대상일 뿐 고장났다고 하지 않았습니다.',evidence:'because the client’s train is delayed'},
        {id:'meeting-2',type:'listen',skill:'inference',prompt:'What time should the team arrive?',options:['10:00','10:50','11:10'],answer:1,explanation:'미팅은 11시이고 10분 먼저 도착하라고 했으므로 10시 50분입니다.',evidence:'moved to eleven … arrive ten minutes early'},
        {id:'meeting-3',type:'context',skill:'tense',prompt:'They ___ already prepared the samples.',translation:'그들은 샘플을 이미 준비했다.',options:['have','has','are'],answer:0,explanation:'They와 함께 have + 과거분사 prepared를 씁니다. 현재의 준비 상태와 연결되는 현재완료입니다.',evidence:'They have already prepared the samples'},
        {id:'meeting-4',type:'context',skill:'vocabulary',prompt:'Bring them to Room Four ___ Room Two.',translation:'2번 방 대신 4번 방으로 가져오세요.',options:['because of','instead of','in front of'],answer:1,explanation:'instead of는 “~대신에”라는 뜻으로 장소의 변경을 나타냅니다.',evidence:'Room Four instead of Room Two'}
      ]
    },
    {
      id:'hotel',title:'A quieter room',level:'B1–B2',kind:'Travel conversation',source:'Original AI-assisted practice dialogue · not an official IELTS item',
      goal:'요청과 대안을 구별하고, 숙박 상황의 세부 정보와 수일치를 이해하기',
      script:'Guest: Excuse me. My room faces the main road, and it is rather noisy. Could I move to a quieter room?\nReceptionist: Certainly. We have a room facing the garden, but it will not be ready until three.\nGuest: That is fine. May I leave my bags here while I go out?\nReceptionist: Of course. We can store them at reception. There is no extra charge for changing rooms.\nGuest: Thank you. I will collect the new key when I return this afternoon.',
      translation:'손님: 제 방이 큰 도로 쪽이라 시끄럽네요. 더 조용한 방으로 옮길 수 있나요?\n직원: 정원 쪽 방이 있지만 3시가 되어야 준비됩니다.\n손님: 괜찮아요. 외출하는 동안 가방을 맡겨도 될까요?\n직원: 프런트에 보관해 드릴게요. 객실 변경 추가 요금은 없습니다.\n손님: 오후에 돌아와서 새 열쇠를 받을게요.',
      questions:[
        {id:'hotel-1',type:'listen',skill:'detail',prompt:'When will the new room be ready?',options:['At noon','At two','At three'],answer:2,explanation:'not … until three는 3시가 되어야 가능하다는 뜻입니다.',evidence:'it will not be ready until three'},
        {id:'hotel-2',type:'listen',skill:'inference',prompt:'What will the guest probably do next?',options:['Go out after leaving the bags','Pay an extra room fee','Move into the new room immediately'],answer:0,explanation:'외출 중 짐 보관을 요청했고 직원이 동의했습니다. 즉시 입실하거나 추가 요금을 낸다는 내용은 없습니다.',evidence:'May I leave my bags here while I go out? … Of course.'},
        {id:'hotel-3',type:'context',skill:'agreement',prompt:'There ___ no extra charge for changing rooms.',translation:'객실 변경에 추가 요금은 없습니다.',options:['are','is','be'],answer:1,explanation:'여기서 charge는 단수 명사이므로 There is를 씁니다.',evidence:'There is no extra charge for changing rooms'},
        {id:'hotel-4',type:'context',skill:'vocabulary',prompt:'May I leave my bags here ___ I go out?',translation:'외출하는 동안 가방을 여기에 맡겨도 될까요?',options:['while','unless','although'],answer:0,explanation:'while은 두 상황이 진행되는 시간의 겹침, 즉 “~하는 동안”을 나타냅니다.',evidence:'while I go out'}
      ]
    },
    {
      id:'commencement',title:'When plans change',level:'B1–B2',kind:'Commencement-style speech',source:'Original practice speech adapted from the repository prototype · not a real TED or commencement recording',
      goal:'연설의 조언과 비유를 이해하고, 과거 시제와 주어-동사 수일치를 확인하기',
      script:'Good morning, graduates. When I was your age, I believed that success came from having a plan. Then, in my second year of work, the company I joined closed down. The people who helped me were not the ones I had tried to impress. They were the ones I had simply been kind to. So here is my advice. Make fewer plans and more friends. Stay curious about things that nobody is grading. And when your own plan falls apart, remember that a closed door is often just a change of direction.',
      translation:'졸업생 여러분, 안녕하세요. 여러분 나이였을 때 저는 성공이 계획에서 온다고 믿었습니다. 그런데 일한 지 2년째에 회사가 문을 닫았습니다. 저를 도운 사람들은 제가 잘 보이려 애썼던 사람들이 아니라 그저 친절하게 대했던 사람들이었습니다. 계획을 줄이고 친구를 늘리세요. 아무도 점수를 매기지 않는 것에 호기심을 가지세요. 계획이 무너지더라도 닫힌 문은 종종 방향의 전환일 뿐임을 기억하세요.',
      questions:[
        {id:'commencement-1',type:'listen',skill:'detail',prompt:'Who helped the speaker?',options:['People the speaker had been kind to','Only former teachers','People the speaker had tried to impress'],answer:0,explanation:'not the ones I had tried to impress라는 부정과 이어지는 설명을 함께 들어야 합니다.',evidence:'They were the ones I had simply been kind to'},
        {id:'commencement-2',type:'listen',skill:'inference',prompt:'What does “a closed door” suggest in the final sentence?',options:['A locked office needs a key','A setback may open a different path','A detailed plan always succeeds'],answer:1,explanation:'문이 닫힌다는 비유는 좌절을 뜻하지만, 화자는 그것을 새로운 방향으로 해석합니다.',evidence:'a closed door is often just a change of direction'},
        {id:'commencement-3',type:'context',skill:'tense',prompt:'When I was your age, I ___ that success came from having a plan.',translation:'여러분 나이였을 때 저는 성공이 계획에서 온다고 믿었습니다.',options:['believe','believed','have believed'],answer:1,explanation:'When I was your age가 과거 시점을 설정하므로 believed를 씁니다.',evidence:'When I was your age, I believed'},
        {id:'commencement-4',type:'context',skill:'agreement',prompt:'Stay curious about things that nobody ___ grading.',translation:'아무도 점수를 매기지 않는 것에 호기심을 가지세요.',options:['are','be','is'],answer:2,explanation:'관계절에서 nobody는 단수로 취급하므로 is를 씁니다. things의 복수 형태에 끌리지 않도록 주의하세요.',evidence:'things that nobody is grading'}
      ]
    }
  ],
  followups:[
    {id:'follow-detail',type:'context',skill:'detail',prompt:'“The workshop starts at nine. Please arrive fifteen minutes early.” When should you arrive?',options:['8:45','9:00','9:15'],answer:0,explanation:'9시에서 15분을 빼면 8시 45분입니다. 시작 시간과 도착 시간을 구별하세요.',evidence:'starts at nine … fifteen minutes early'},
    {id:'follow-inference',type:'context',skill:'inference',prompt:'“The room is not ready yet. You can leave your suitcase here and collect the key later.” What is the best next step?',options:['Enter the room now','Leave the suitcase and return later','Pay for a second suitcase'],answer:1,explanation:'즉시 입실할 수 없으므로 짐을 맡기고 나중에 열쇠를 받는 것이 적절합니다.',evidence:'not ready yet … collect the key later',challenge:true},
    {id:'follow-tense',type:'context',skill:'tense',prompt:'Last Monday, our team ___ the revised schedule.',options:['receives','has received','received'],answer:2,explanation:'Last Monday는 끝난 과거 시점이므로 received입니다.',evidence:'Last Monday'},
    {id:'follow-agreement',type:'context',skill:'agreement',prompt:'Each of the students ___ a different recording.',options:['hear','hears','hearing'],answer:1,explanation:'주어의 중심은 Each이므로 단수 동사 hears입니다.',evidence:'Each of the students',challenge:true},
    {id:'follow-vocabulary',type:'context',skill:'vocabulary',prompt:'We will meet online ___ travelling to the office.',options:['instead of','because','although'],answer:0,explanation:'“사무실에 가는 대신”이므로 instead of + -ing를 씁니다.',evidence:'online … travelling to the office'}
  ]
};
