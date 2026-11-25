window.AEL_TRAINER = {
  "version": "3.0",
  "createdAt": "2026-11-25",
  "provenance": "Original AI-assisted practice drafted in Codex, with teammate LC trainer references and professor feedback. Not official TOEIC/TEPS material. Human teacher review pending. No score prediction.",
  "packs": [
    {
      "id": "toeic2",
      "exam": "TOEIC",
      "part": "Part 2 · 응답",
      "title": "말 그대로가 아닌 대답",
      "topic": "직장 · 약속과 부탁",
      "level": "B1–B2 · 검증 전 예상 수준",
      "minutes": 6,
      "goal": "반복된 단어보다 질문의 의도와 응답의 의미를 연결해요.",
      "oralChoices": true,
      "questions": [
        {
          "id": "t2-1",
          "prompt": "가장 자연스러운 응답은 무엇인가요?",
          "options": [
            "It is printed on the invitation.",
            "I have a client dinner that evening.",
            "The party was enjoyable."
          ],
          "answer": 1,
          "skill": "inference",
          "evidence": "I have a client dinner that evening.",
          "explanation": "그날 다른 약속이 있다는 말로 참석하기 어렵다는 뜻을 전합니다. party라는 단어의 반복만으로 답을 고르지 않아요.",
          "dictation": "I have a client dinner that evening.",
          "expression": "I have another appointment. 여기서 이 말의 기능은?",
          "choices": [
            "간접 거절",
            "장소 안내",
            "지난 행사 평가"
          ],
          "correct": 0,
          "sound": "client dinner를 한 의미 덩어리로 듣고, THAT evening의 시간 단서에 주목하세요.",
          "retry": {
            "script": "A: Can you join our lunch on Friday?\nB: I will be on a business trip that day.",
            "prompt": "What does the second speaker imply?",
            "options": [
              "They want a later lunch.",
              "They need directions.",
              "They cannot attend."
            ],
            "answer": 2,
            "explanation": "출장 일정이 겹쳐 참석하기 어렵다는 간접 응답입니다.",
            "audioId": "t2-1-retry"
          },
          "script": "A: You're coming to the retirement party, aren't you?\nB: A. It is printed on the invitation.\nB: B. I have a client dinner that evening.\nB: C. The party was enjoyable.",
          "audioId": "t2-1-main",
          "dictationAudio": "t2-1-focus"
        },
        {
          "id": "t2-2",
          "prompt": "가장 자연스러운 응답은 무엇인가요?",
          "options": [
            "At two fifteen, after the briefing.",
            "There are fifty people.",
            "The meeting room is large."
          ],
          "answer": 0,
          "skill": "detail",
          "evidence": "At two fifteen, after the briefing.",
          "explanation": "When은 시간을 묻습니다. 인원수 fifty나 장소 정보가 아니라 two fifteen이 답입니다.",
          "dictation": "At two fifteen, after the briefing.",
          "expression": "two fifteen은 몇 시인가요?",
          "choices": [
            "2:50",
            "2:15",
            "12:15"
          ],
          "correct": 1,
          "sound": "fifTEEN과 FIFty의 강세 차이를 들어보세요. 숫자는 앞뒤 문맥과 함께 확인하세요.",
          "retry": {
            "script": "A: When should we meet the new manager?\nB: At three fifty, after the workshop.",
            "prompt": "When is the meeting?",
            "options": [
              "3:15",
              "3:50",
              "5:30"
            ],
            "answer": 1,
            "explanation": "three fifty는 3:50입니다. fifteen과 fifty를 구분하세요.",
            "audioId": "t2-2-retry"
          },
          "script": "A: When will the client meeting begin?\nB: A. At two fifteen, after the briefing.\nB: B. There are fifty people.\nB: C. The meeting room is large.",
          "audioId": "t2-2-main",
          "dictationAudio": "t2-2-focus"
        },
        {
          "id": "t2-3",
          "prompt": "가장 자연스러운 응답은 무엇인가요?",
          "options": [
            "The proposal is on the desk.",
            "Yes, the desk is new.",
            "A second pair of eyes would help."
          ],
          "answer": 2,
          "skill": "paraphrase",
          "evidence": "A second pair of eyes would help.",
          "explanation": "다른 사람이 한번 더 살펴봐 주면 좋겠다는 뜻으로 교정 제안을 받아들입니다.",
          "dictation": "A second pair of eyes would help.",
          "expression": "a second pair of eyes와 가장 가까운 표현은?",
          "choices": [
            "another review",
            "a new screen",
            "a new employee"
          ],
          "correct": 0,
          "sound": "pair of eyes를 한 덩어리로 연결해 읽어보세요. 단어마다 끊기보다 의미 단위를 유지해요.",
          "retry": {
            "script": "A: Would you like me to check your report?\nB: Another review would be useful.",
            "prompt": "What does the second speaker want?",
            "options": [
              "Help reviewing the report",
              "A different computer",
              "A printed timetable"
            ],
            "answer": 0,
            "explanation": "another review는 다른 사람이 다시 검토해 주기를 원한다는 뜻입니다.",
            "audioId": "t2-3-retry"
          },
          "script": "A: Would you like me to proofread your proposal?\nB: A. The proposal is on the desk.\nB: B. Yes, the desk is new.\nB: C. A second pair of eyes would help.",
          "audioId": "t2-3-main",
          "dictationAudio": "t2-3-focus"
        }
      ]
    },
    {
      "id": "toeic3",
      "exam": "TOEIC",
      "part": "Part 3 · 대화",
      "title": "바뀐 일정, 놓치지 않기",
      "topic": "직장 · 일정 변경",
      "level": "B1–B2 · 검증 전 예상 수준",
      "minutes": 7,
      "goal": "변경 전·후의 정보와 화자별 할 일을 구분해요.",
      "script": "Alex: The client meeting was at ten, but it has moved to eleven because the train is delayed.\nMorgan: Should I tell the design team?\nAlex: Yes. Ask them to bring the samples to Room Four instead of Room Two.\nMorgan: I will send an updated invitation now.\nAlex: Please ask everyone to arrive ten minutes early.",
      "questions": [
        {
          "id": "t3-1",
          "prompt": "When should everyone arrive?",
          "options": [
            "10:00",
            "10:50",
            "11:10",
            "11:00"
          ],
          "answer": 1,
          "skill": "detail",
          "evidence": "The client meeting was at ten, but it has moved to eleven because the train is delayed. / Please ask everyone to arrive ten minutes early.",
          "explanation": "회의는 11시, 도착은 10분 전인 10:50입니다. 회의 시작과 도착 시각을 구분해요.",
          "dictation": "Please ask everyone to arrive ten minutes early.",
          "expression": "The meeting starts at eleven. Arrive ten minutes early. → 도착 시각은?",
          "choices": [
            "10:50",
            "11:10",
            "10:10"
          ],
          "correct": 0,
          "sound": "TEN minutes EARLY에 강세를 두고 따라 말해요. early와 late가 시간 계산을 바꿉니다.",
          "retry": {
            "script": "The tour starts at two thirty. Please arrive fifteen minutes early.",
            "prompt": "When should visitors arrive?",
            "options": [
              "2:45",
              "2:30",
              "2:15",
              "1:45"
            ],
            "answer": 2,
            "explanation": "2:30에서 15분을 빼면 2:15입니다.",
            "audioId": "t3-1-retry"
          },
          "dictationAudio": "t3-1-focus"
        },
        {
          "id": "t3-2",
          "prompt": "Why was the meeting moved?",
          "options": [
            "The room is closed.",
            "The samples are missing.",
            "The client's train is late.",
            "The projector is broken."
          ],
          "answer": 2,
          "skill": "inference",
          "evidence": "it has moved to eleven because the train is delayed.",
          "explanation": "because 뒤의 기차 지연이 일정 변경의 원인입니다. 장소나 준비물은 원인이 아니에요.",
          "dictation": "It has moved to eleven because the train is delayed.",
          "expression": "because가 이끄는 정보는?",
          "choices": [
            "원인",
            "대조",
            "추가 요청"
          ],
          "correct": 0,
          "sound": "because 뒤의 the TRAIN is deLAYED를 하나로 말하며 이유를 전달해요.",
          "retry": {
            "script": "The workshop will begin at noon rather than eleven because the instructor's flight is delayed.",
            "prompt": "Why will the workshop start later?",
            "options": [
              "The room is smaller.",
              "The instructor is arriving late.",
              "Lunch is not ready.",
              "No one registered."
            ],
            "answer": 1,
            "explanation": "강사의 비행 지연이 원인입니다.",
            "audioId": "t3-2-retry"
          },
          "dictationAudio": "t3-2-focus"
        },
        {
          "id": "t3-3",
          "prompt": "What will Morgan do next?",
          "options": [
            "Check the train",
            "Bring a projector",
            "Book Room Two",
            "Send a revised invitation"
          ],
          "answer": 3,
          "skill": "paraphrase",
          "evidence": "I will send an updated invitation now.",
          "explanation": "updated는 revised와 같은 의미로 쓰였습니다. Morgan의 다음 행동을 찾아야 해요.",
          "dictation": "I will send an updated invitation now.",
          "expression": "updated invitation과 같은 뜻은?",
          "choices": [
            "revised invitation",
            "canceled meeting",
            "first invitation"
          ],
          "correct": 0,
          "sound": "I'll / send an updated invitation / now. 의미 단위로 끊어 말해요.",
          "retry": {
            "script": "A: The venue has changed to the library.\nB: I will email the revised directions to all participants.",
            "prompt": "What will the second speaker do?",
            "options": [
              "Send updated travel information",
              "Cancel the event",
              "Call the librarian",
              "Buy tickets"
            ],
            "answer": 0,
            "explanation": "revised directions를 이메일로 보내겠다는 말이 updated travel information으로 바뀌었습니다.",
            "audioId": "t3-3-retry"
          },
          "dictationAudio": "t3-3-focus"
        }
      ],
      "audioId": "toeic3-main"
    },
    {
      "id": "toeic4",
      "exam": "TOEIC",
      "part": "Part 4 · 담화",
      "title": "공항 안내의 마지막 정보",
      "topic": "여행 · 공항 안내",
      "level": "B1–B2 · 검증 전 예상 수준",
      "minutes": 7,
      "goal": "안내 방송에서 바뀐 시간과 필요한 행동을 찾아요.",
      "script": "Good afternoon, passengers for Flight 417. Boarding has moved from gate B12 to gate C4 because of an aircraft inspection. Boarding begins at four forty-five, fifteen minutes later than planned. Your checked bags will be transferred automatically. Please go directly to gate C4.",
      "questions": [
        {
          "id": "t4-1",
          "prompt": "When will boarding begin?",
          "options": [
            "4:30",
            "4:15",
            "4:45",
            "5:00"
          ],
          "answer": 2,
          "skill": "detail",
          "evidence": "Boarding begins at four forty-five, fifteen minutes later than planned.",
          "explanation": "최종 탑승 시각은 four forty-five입니다. 원래 예정된 4:30과 구분해요.",
          "dictation": "Boarding begins at four forty-five.",
          "expression": "four forty-five를 숫자로 쓰면?",
          "choices": [
            "4:45",
            "4:15",
            "5:45"
          ],
          "correct": 0,
          "sound": "four FORTY-FIVE의 마지막 숫자까지 들어요. fifteen은 지연 길이이지 최종 시각이 아닙니다.",
          "retry": {
            "script": "The bus was scheduled for six ten. It will now leave at six forty.",
            "prompt": "When will the bus leave?",
            "options": [
              "6:10",
              "6:30",
              "6:40",
              "6:14"
            ],
            "answer": 2,
            "explanation": "now leave가 최종 출발 시각 6:40을 알려줍니다.",
            "audioId": "t4-1-retry"
          },
          "dictationAudio": "t4-1-focus"
        },
        {
          "id": "t4-2",
          "prompt": "Why has the gate changed?",
          "options": [
            "An aircraft is being inspected.",
            "The flight is canceled.",
            "The luggage is missing.",
            "The staff are on strike."
          ],
          "answer": 0,
          "skill": "inference",
          "evidence": "because of an aircraft inspection.",
          "explanation": "because of 뒤에 원인이 제시됩니다. inspection은 점검입니다.",
          "dictation": "The gate has changed because of an aircraft inspection.",
          "expression": "because of an inspection과 같은 뜻은?",
          "choices": [
            "점검에도 불구하고",
            "점검 때문에",
            "점검 대신에"
          ],
          "correct": 1,
          "sound": "an aircraft inspection에서 모음으로 시작하는 단어를 자연스럽게 연결해요.",
          "retry": {
            "script": "The museum entrance has moved to the east side because the main doors are being repaired.",
            "prompt": "Why has the entrance changed?",
            "options": [
              "The tickets are sold out.",
              "The museum has closed.",
              "The main doors need repairs.",
              "The exhibition has moved."
            ],
            "answer": 2,
            "explanation": "주 출입문 수리가 변경의 원인입니다.",
            "audioId": "t4-2-retry"
          },
          "dictationAudio": "t4-2-focus"
        },
        {
          "id": "t4-3",
          "prompt": "What should passengers do about checked bags?",
          "options": [
            "Collect them at B12",
            "Pay a transfer fee",
            "Take them to C4",
            "No action is needed"
          ],
          "answer": 3,
          "skill": "paraphrase",
          "evidence": "Your checked bags will be transferred automatically.",
          "explanation": "자동으로 옮겨진다는 말은 승객이 직접 할 일이 없다는 뜻입니다.",
          "dictation": "Your checked bags will be transferred automatically.",
          "expression": "transferred와 가장 가까운 뜻은?",
          "choices": [
            "moved",
            "checked",
            "lost"
          ],
          "correct": 0,
          "sound": "CHECKED BAGS / will be transferred / automatically. 중요한 정보 단위를 살려 말해요.",
          "retry": {
            "script": "Your reservation will be moved to the new hotel automatically. You do not need to contact either hotel.",
            "prompt": "What should the guest do about the reservation?",
            "options": [
              "Call both hotels",
              "Make a second booking",
              "Take no action",
              "Pay again"
            ],
            "answer": 2,
            "explanation": "자동 이전되므로 따로 행동할 필요가 없습니다.",
            "audioId": "t4-3-retry"
          },
          "dictationAudio": "t4-3-focus"
        }
      ],
      "audioId": "toeic4-main"
    },
    {
      "id": "teps",
      "exam": "TEPS",
      "part": "청해 · 대화 연습",
      "title": "스터디 약속 조율하기",
      "topic": "대학 · 스터디",
      "level": "B1–B2 · 검증 전 예상 수준",
      "minutes": 7,
      "goal": "간접적인 요청과 바뀐 약속을 이해하고 직접 응답해요.",
      "oralChoices": true,
      "script": "A: Can you join our study group at the library tomorrow?\nB: I have a lab session until three. Could we start at three thirty instead of two?\nA: That works. I will book a room for three thirty. Please send everyone the new time.\nB: Sure. I will let the group know tonight.",
      "questions": [
        {
          "id": "te-1",
          "prompt": "Why does the second speaker suggest a later time?",
          "options": [
            "The library opens late.",
            "The room is full.",
            "They have a laboratory session.",
            "They forgot the meeting."
          ],
          "answer": 2,
          "skill": "inference",
          "evidence": "I have a lab session until three.",
          "explanation": "3시까지 실험 수업이 있다는 말로 기존 2시 약속이 어렵다는 이유를 전달합니다.",
          "dictation": "I have a lab session until three.",
          "expression": "이 문장이 약속 조율에서 하는 역할은?",
          "choices": [
            "시간 변경의 이유",
            "도서관 위치 안내",
            "방 예약 확인"
          ],
          "correct": 0,
          "sound": "lab session / until THREE. until 뒤의 시각까지 다른 일정이 있음을 전달해요.",
          "retry": {
            "script": "A: Can we rehearse at four?\nB: My tutorial ends at four thirty. Could we meet at five?",
            "prompt": "Why does the second speaker request five o'clock?",
            "options": [
              "They have an earlier class.",
              "They need a new room.",
              "They dislike rehearsals.",
              "They want to cancel."
            ],
            "answer": 0,
            "explanation": "수업이 4:30에 끝나서 더 늦은 시간을 요청합니다.",
            "audioId": "te-1-retry"
          },
          "dictationAudio": "te-1-focus",
          "questionAudio": "te-1-question"
        },
        {
          "id": "te-2",
          "prompt": "When will the study group meet?",
          "options": [
            "2:00",
            "3:00",
            "3:30",
            "2:30"
          ],
          "answer": 2,
          "skill": "detail",
          "evidence": "Could we start at three thirty instead of two? / I will book a room for three thirty.",
          "explanation": "대화 상대가 동의한 최종 약속은 3:30입니다.",
          "dictation": "Could we start at three thirty instead of two?",
          "expression": "instead of two는 무엇을 뜻하나요?",
          "choices": [
            "2시와 함께",
            "2시 대신",
            "2시 이전"
          ],
          "correct": 1,
          "sound": "THREE THIRTY / instead of TWO. 바뀌는 두 시각을 대조해서 읽어보세요.",
          "retry": {
            "script": "A: The club meeting was at five, but the room is only free at five forty.\nB: All right. Let us meet at five forty.",
            "prompt": "What is the agreed time?",
            "options": [
              "5:00",
              "5:14",
              "4:50",
              "5:40"
            ],
            "answer": 3,
            "explanation": "동의한 최종 시각은 5:40입니다.",
            "audioId": "te-2-retry"
          },
          "dictationAudio": "te-2-focus",
          "questionAudio": "te-2-question"
        },
        {
          "id": "te-3",
          "prompt": "What will the second speaker do tonight?",
          "options": [
            "Book a room",
            "Inform the other members",
            "Prepare an experiment",
            "Go to the library"
          ],
          "answer": 1,
          "skill": "paraphrase",
          "evidence": "I will let the group know tonight.",
          "explanation": "let someone know는 inform someone과 같은 뜻입니다. 방을 예약하는 사람은 첫 번째 화자예요.",
          "dictation": "I will let the group know tonight.",
          "expression": "let the group know와 같은 뜻은?",
          "choices": [
            "inform the members",
            "join a new group",
            "reserve the room"
          ],
          "correct": 0,
          "sound": "LET the group KNOW / tonight. 핵심 동사와 시간에 강세를 두고 말해요.",
          "retry": {
            "script": "A: I have reserved the seminar room. Can you pass the new schedule on to the others?\nB: Yes, I will message them this afternoon.",
            "prompt": "What will the second speaker do?",
            "options": [
              "Reserve a room",
              "Attend a seminar",
              "Share the updated schedule",
              "Cancel the messages"
            ],
            "answer": 2,
            "explanation": "pass on과 message them은 다른 사람에게 일정 정보를 전달한다는 뜻입니다.",
            "audioId": "te-3-retry"
          },
          "dictationAudio": "te-3-focus",
          "questionAudio": "te-3-question"
        }
      ],
      "audioId": "teps-main"
    }
  ]
};
