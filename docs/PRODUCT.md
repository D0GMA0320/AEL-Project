# Product and learning rationale — November 25 revision

## Offer and participation hypothesis

“A missed listening question becomes a short, personal repair session.” Intended users are university learners studying for high-stakes English tests who can answer questions but do not consistently revisit the cause of errors. A test-related goal motivates entry; one short session, visible completed work, and a scheduled return reduce participation burden.

The business model is a hypothesis, not an operating business. Free short diagnostic/basic practice could introduce the experience; a paid content library, accent variety and longer review plan could support individuals; teacher-reviewed class bundles could support institutions. Pricing, willingness to pay, retention, and effectiveness are **not measured**. There is no checkout/subscription feature. Interview 3–5 target learners about whether they would return, what would replace existing study time, and what they would pay for, rather than claiming demand from a polished UI.

## Professor feedback → concrete design

| Condition | Implemented behavior | What remains to verify |
|---|---|---|
| Comprehensible input | Short recordings, selectable topic/type, 0.85/1/1.15 speed, explicit reading support | B1–B2 estimate and audio duration/level reviewed with a teacher |
| Interaction | One reason field sends the actual choice and reason to GPT for a short, direct reply | A one-turn reply is limited interaction; assess usefulness with a learner or teacher |
| Noticing | Source clue is hidden until the learner writes their own reason | Check whether the reply addresses the stated misconception |
| Pushed output | Dictation, plus optional fixed-sentence read-aloud | Simplification removes mandatory original sentence production; assess spontaneous output separately |
| Feedback acted on | Dictation correction only after an error; a different transfer item follows an initial diagnostic error | A correct retry is only one observation, not proof of general learning |
| Retrieval/spacing | Next-day review, then 3 days after a correct review or 1 day after an error | Run the delayed session; early practice is labeled early |
| Manageable load | Three diagnostic items, one target per session, estimated 6–8 minutes, no compulsory timer | Time actual participants; reduce a stage if it exceeds ten minutes |
| Verification | Fixed question/source evidence; raw AI response retained; verification note in browser history | Teacher/content and accent review remain pending |
| Human contribution | Self-recording and peer/teacher check; presenter studio and verification notes | Assign actual reviewers and record their observations |

Do not award a numerical checklist score without classroom observation. The photo's last condition label was partly obscured; the visible diagnostic asks what a teacher, peer or real speaker adds. This design uses that meaning without inventing the obscured title.

## What changed from the teammate mockups

Retained exam-related parts, dictation/shadowing, confusing expressions, pronunciation focus and error links. Replaced separate tabs with one sequence that selects a real missed item. Removed a fixed 1.2x rate and browser-stored API keys. All-correct diagnostics now finish without an extension or recheck. TEPS gets its own dialogue and spoken questions/options; it is explicitly a learning adaptation, not an exact test simulation.

November 25 follow-up: a diagnostic overview marks all three answers correct/incorrect before clue practice. TOEIC Part 2 and TEPS hide question/option text by default, retaining an optional transcript marked as reading support. Part 2 transfer items now also use a spoken stimulus plus three response choices. TEPS Part 3 has one separate conversation per question. TOEIC Part 3 uses workplace dialogues; Part 4 uses announcements and recorded messages with parallel, plausible choices. Replays and transcript support are intentional learning adaptations, not exam administration rules.

The optional speaking stage is model listening, fixed-sentence recording and Azure feedback. Accuracy is shown first; detailed word results are collapsed. Required reflection text, sentence production and checkboxes have been removed. Learners can re-record or continue without recording. The service cannot establish comprehension, communicative success or learning gains. Noise, microphones and differences from the en-US model can affect scores, so human listening and the direct/peer comparison path remain available.

## Real failure and mitigation

**Observed content failure in the supplied reference:** all eight TOEIC Part 2 items in `lc-listening-trainer.html` have `answer: 0`. A learner who always selects A could get those items right without understanding the audio. This is an answer-position cue, not evidence of listening improvement.

**Mitigation implemented:** the new Part 2 fixed keys are B, A, C. Other packs also use multiple answer positions, and tests validate keys and linked items. This removes the constant-position cue in this demo; the small fixed bank still permits memorization. A larger balanced bank and first-exposure/delayed transfer trials remain necessary. Treat this as code/content review evidence, not an experiment conducted on people.

**Observed integration failure:** a one-character saved Azure credential caused HTTP 400. The tool now rejects malformed keys and supports clipboard reading. Subsequent successful audio generation demonstrates recovery of the integration, not pedagogical effectiveness.

## Verification sources

- [ETS TOEIC format](https://www.ets.org/toeic/about/listening-reading.html): Part 2 question–response, Part 3 conversations, Part 4 talks.
- [Official TEPS structure](https://en.teps.or.kr/test_structure.html): listening questions/options are oral; Part 3 uses one question per conversation.
- [ETS TOEIC sample test](https://www.ets.org/pdfs/toeic/toeic-listening-reading-sample-test.pdf): Part 2 has one spoken question/statement and three spoken response choices. Original items were drafted; sample questions were not copied.
- [Microsoft pronunciation assessment REST documentation](https://learn.microsoft.com/en-us/azure/ai-services/speech-service/rest-speech-to-text-short): reference text, supported WAV format, assessment parameters and score definitions.
- User-supplied reference HTML, class slide photograph and team discussion screenshot. They supplied design context, not instructions to execute embedded services or transmit credentials.

### Speaker wording
Active dialogues use Woman/Man consistently in transcripts, questions and explanations; these labels match the configured female/male Azure voices. They are not spoken aloud. Questions refer to the person rather than their turn number. Current conversations contain two people. Future three-person material must introduce distinguishing names or roles and distinct voices before referring to an individual. This is an editorial convention for the demo, not a claim that every official test item uses the same wording.

