# Evidence and learner pilot protocol

## Learner and goal

Proposed learner: Korean-speaking university students around B1–B2 who want practice with unfamiliar English voices in business/travel situations. This is a proposed profile, not a measured proficiency result.

Goal: identify the reason and time of a schedule change, explain a contextual grammar/vocabulary choice, then apply the rule in a new sentence. Record both initial and follow-up answers. Do not infer durable improvement from one same-session follow-up.

## Record each AI use

Keep model/provider, actual use date, exact original prompt, unchanged original output, and separate review notes. Live calls automatically store the request payload (including instructions and input), unmodified JSON response text, model as returned, timestamps and latency. Azure logs exact SSML, voice IDs, output SHA-256 and audio path; retain the MP3 as the actual output.

Manual ChatGPT use and old prototype generation require original conversation records; this project handoff is not a substitute. The underlying model identity of the current Codex-assisted lesson drafting is not exposed to the code. Do not guess it. Preserve `assets/data.js` as the delivered content snapshot and record any later human edits separately.

## Small pilot, not an efficacy study

1. Review every answer, explanation and translation against the source.
2. Have each teammate complete an untimed session under recorded conditions.
3. Change one condition at a time, and vary the order of accents across participants.
4. Record actual voice identity, content ID, playback speed/count and time limit.
5. Compare observations cautiously: repeated content creates practice effects; different content creates difficulty differences; different voices introduce speaker effects.
6. Report descriptive counts and concrete errors. Do not claim a measured accent deficit or validated learning gain.

## Real failure and improvement

Already observed in source review: the previous prototype treated equal scores as a reason to raise difficulty, even when both were 0%. The new recommendation logic prioritizes foundational practice for low scores; an automated regression check exercises that case. This is a software failure, not a learner trial or an AI-model failure.

For the assignment, additionally record an actual AI-use or learner-interaction limitation, for example:

- A missing AU voice on the actual demo device. Capture the availability message; generate a named Azure AU voice; replay and document human review.
- A real 3-second timeout. Preserve the response time, then retest a new comparable item without a timer. Do not invent a failure by labeling a deliberately wrong demonstration answer as an authentic learner error.
- An actual LLM answer-key mistake. Save the unchanged response, identify the exact source evidence, correct the reviewed version, and record the retest.
- An actual Whisper hallucination or correction. Retain the source audio, unchanged transcript, human checked text and downstream feedback separately.

Use the app's Evidence page. Leave observations and results as “not yet tested” until performed.

## Contribution record (fill with actual names/work)

| Responsibility | Actual member | Evidence of contribution |
| --- | --- | --- |
| Learner goals, listening content and source review | To fill | Reviewed content/version |
| Accent audio generation and listening verification | To fill | SSML, voice IDs, MP3s, review notes |
| Context questions, timing and pilot observations | To fill | Response exports and feedback |
| Integration, testing and presentation assembly | To fill | Commits, checks, final slides/recording |

These are proposed responsibilities, not claims that contributions have occurred.

## Revised exam-focused pilot (November 25)

Use one 6–8 minute session, one missed skill, and a first-seen transfer item. Before intervention, record the selected answer and learner's own reason. Preserve dictation attempt, correction, explanation revision, produced sentence, transfer result, and audio/reading support events in the session JSON. Do not compare the 3-item diagnostic proportion with the single transfer item as a validated gain score.

For the real failure case, inspect the provided reference Part 2 bank: eight answer indices are 0. The revised demo Part 2 indices are 1, 0, 2. Show source before/after as a content-design failure and mitigation, not as a learner experiment. Then test a real learner without coaching which choice to make. Ask what evidence they used. Tomorrow, use the retrieval view and record whether it is an early or scheduled review. Same-item recall is not evidence of new-item transfer.

Human checks still needed: appropriateness for the intended learner, answer-key/source agreement, naturalness of all selected voices, microphone behavior on the presentation device, and whether the learner would return voluntarily. Do not fill in names, scores, times or positive feedback that were not observed.
