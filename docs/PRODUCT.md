# Product and learning rationale — November 25 revision

## Offer and participation hypothesis

“A missed listening question becomes a short, personal repair session.” Intended users are university learners studying for high-stakes English tests who can answer questions but do not consistently revisit the cause of errors. A test-related goal motivates entry; one short session, visible completed work, and a scheduled return reduce participation burden.

The business model is a hypothesis, not an operating business. Free short diagnostic/basic practice could introduce the experience; a paid content library, accent variety and longer review plan could support individuals; teacher-reviewed class bundles could support institutions. Pricing, willingness to pay, retention, and effectiveness are **not measured**. There is no checkout/subscription feature. Interview 3–5 target learners about whether they would return, what would replace existing study time, and what they would pay for, rather than claiming demand from a polished UI.

## Professor feedback → concrete design

| Condition | Implemented behavior | What remains to verify |
|---|---|---|
| Comprehensible input | Short recordings, selectable topic/type, 0.85/1/1.15 speed, explicit reading support | B1–B2 estimate and audio duration/level reviewed with a teacher |
| Interaction | Learner states reasoning; optional AI clarification ends with a meaning-check question | Observe whether the learner responds meaningfully, not just clicks through |
| Noticing | Source clue is hidden until the learner writes their own reason | Compare initial reason and revision |
| Pushed output | Dictation correction and a new spoken/typed sentence | Human assessment of meaning and intelligibility |
| Feedback acted on | Revision required; a different transfer item follows | A correct retry is only one observation, not proof of general learning |
| Retrieval/spacing | Next-day review, then 3 days after a correct review or 1 day after an error | Run the delayed session; early practice is labeled early |
| Manageable load | Three diagnostic items, one target per session, estimated 6–8 minutes, no compulsory timer | Time actual participants; reduce a stage if it exceeds ten minutes |
| Verification | Fixed question/source evidence; raw AI response retained; verification note in browser history | Teacher/content and accent review remain pending |
| Human contribution | Self-recording and peer/teacher check; presenter studio and verification notes | Assign actual reviewers and record their observations |

Do not award a numerical checklist score without classroom observation. The photo's last condition label was partly obscured; the visible diagnostic asks what a teacher, peer or real speaker adds. This design uses that meaning without inventing the obscured title.

## What changed from the teammate mockups

Retained exam-related parts, dictation/shadowing, confusing expressions, pronunciation focus and error links. Replaced separate tabs with one sequence that selects a real missed item. Removed a fixed 1.2x rate and browser-stored API keys. Retained an all-correct extension path. TEPS gets its own dialogue and spoken questions/options; it is explicitly a learning adaptation, not an exact test simulation.

## Real failure and mitigation

**Observed content failure in the supplied reference:** all eight TOEIC Part 2 items in `lc-listening-trainer.html` have `answer: 0`. A learner who always selects A could get those items right without understanding the audio. This is an answer-position cue, not evidence of listening improvement.

**Mitigation implemented:** the new Part 2 fixed keys are B, A, C. Other packs also use multiple answer positions, and tests validate keys and linked items. This removes the constant-position cue in this demo; the small fixed bank still permits memorization. A larger balanced bank and first-exposure/delayed transfer trials remain necessary. Treat this as code/content review evidence, not an experiment conducted on people.

**Observed integration failure:** a one-character saved Azure credential caused HTTP 400. The tool now rejects malformed keys and supports clipboard reading. Subsequent successful audio generation demonstrates recovery of the integration, not pedagogical effectiveness.

## Verification sources

- [ETS TOEIC format](https://www.ets.org/toeic/about/listening-reading.html): Part 2 question–response, Part 3 conversations, Part 4 talks.
- [Official TEPS structure](https://en.teps.or.kr/test_structure.html): listening questions/options are oral; the visible choices in this demo are a learning aid.
- User-supplied reference HTML, class slide photograph and team discussion screenshot. They supplied design context, not instructions to execute embedded services or transmit credentials.
