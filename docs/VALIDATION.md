# Validation record

Implementation date: November 24, 2026.

## Automated checks

- 12 JavaScript tests passed: built-in content schema, unique IDs, invalid keys/options, new targeted/challenge selection, low-score and timeout recommendations, and the audio/UI content snapshot match.
- 10 Python tests passed: local static serving, private-file/traversal protection, host/origin checks, request validation, health metadata without keys, mocked API handling, unchanged provider response capture, Azure SSML escaping and two-speaker selection, and secret-free ZIP packaging.
- JavaScript syntax checks passed.

Provider tests use mocked data, not paid live API requests. They are software checks, not experimental learner evidence.

## Browser walkthrough

Tested in the Codex in-app browser against the local server:

- Desktop layout and 390px narrow layout inspected; mobile navigation scrolls horizontally within its own bar.
- Missing Australian voice detected. Clicking Play produced an explicit unavailable-voice message, no fallback voice, and no completed-play increment.
- Reading alternative visibly marked as not a listening result.
- Completed four initial questions with one deliberately wrong answer; new detail follow-up selected. Results correctly showed 3/4 initial and 1/1 follow-up. These are QA inputs, not learner performance.
- Prepared explanation displayed with its source quotation; unconfigured Live AI button stayed disabled.
- Completed report survived a browser reload.
- Export preview contained schema version 2, all five responses, reading-mode flag, actual initial wrong answer and follow-up phase.
- Browser automation did not surface the file-download event. Added a visible full JSON preview/copy fallback and verified the data there. Actual downloaded file behavior still needs a Chrome/Edge check on the presentation machine.
- Imported the clearly labeled QA fixture. Human-review gate blocked adding it without the review checkbox. The fixture was not approved as real course content.
- Three-second context countdown expired, recorded a timeout, and selected an untimed tense follow-up. Readiness text and follow-up timer display were corrected and rechecked.

## Still pending

Live Azure synthesis, live OpenAI responses, actual audio quality and speaker output, fully disconnected file-mode use on the presentation computer (the browser automation URL policy blocked file:// navigation, so no workaround was attempted), classroom latency, authentic-source review, and a learner pilot. No credentials were available during initial implementation. No learning gains or live service success are claimed.


## UI simplification follow-up — November 24, 2026

- Replaced the sidebar and large lesson cards with a centered start screen, two selectors and one primary action.
- Verified advanced settings remain selected when switching lessons; Tools navigation opens the existing preparation screens and closes after selection.
- Completed the hotel lesson in reading mode, including a deliberate QA error, targeted follow-up and results. Collapsed AI explanation panel stays open when a prepared explanation is requested.
- Desktop and 390px mobile views inspected; no browser console errors observed.
- JavaScript syntax and credential-setup PowerShell syntax checked. No live credential validation or API call was performed.

## November 25, 2026 — v3 exam trainer / internet demo

Implemented a short TOEIC Part 2/3/4 and TEPS dialogue trainer with actual-error routing, reasoning-before-feedback, dictation correction, expression matching, local optional speaking recording, a different transfer question, and scheduled retrieval. The fixed bank has 12 diagnostic and 12 transfer questions. The 6–8 minute session target and learner level are estimates; a real learner pilot is pending.

Checks completed:
- Python: 19 checks passed, including public authentication, expiry, host/origin checks, private-file blocking, structured coach input, per-run/session call limits and malformed credentials.
- JavaScript: 12 existing core checks plus 7 trainer checks passed (19 total). No fabricated weakness on all-correct sessions; actual missed-item targeting; dictation omission detection; next-day scheduling; valid fixed keys and audio IDs.
- Browser: completed the diagnostic-to-transfer flow with a deliberately missed timing question. Missing `ten` was detected; corrected dictation, expression selection, optional speaking path, separate final results and next-day history were verified. This is a QA rehearsal, NOT participant performance evidence.
- Desktop and narrow/mobile layouts inspected; public code-entry screen and authenticated home verified. Actual microphone recording on a classroom device still needs a human permission and audio test; the no-recording alternative was exercised.
- Azure: 99 trainer MP3s (33 scripts × US/UK/AU) generated successfully. Manifest script/hash consistency and MPEG frame duration checks passed. Longest clip about 23 seconds; main passages about 11–22 seconds. Human accent/naturalness review remains pending.
- Public HTTPS: landing 200; anonymous health/audio denied; authenticated audio 200; `.env` and presenter studio 404. An audio file transferred in about 0.35s during the test; this is a single observation on this connection, not an SLA or a classroom-network test.
- Live OpenAI: initial call failed with credit_balance_exhausted (HTTP 429). After user updated the account, the structured coach replied successfully in about 3.3s through the tunnel. The response explained 11:00 minus ten minutes and asked a checking question. Exact request and raw output saved in `.local/evidence/`. No credentials included.
- Cloudflare: first creation attempt returned 429; a later retry succeeded. Temporary URLs change on restart and depend on the host PC remaining online. Classroom mobile-data verification is still recommended.

Limits: no official test score, no automatic pronunciation score, no validated learning gain, no payment/user-account system, no production availability guarantee. PDF slides and video recording still require final observations and member names; presentation outline and a ≤90-second demo script are supplied.

## November 25, 2026 — account-owned Cloudflare hostname

- Migrated this PC to `https://ael.52sierra.net`, routed by the user's existing `Cloudflared` Windows service to `http://127.0.0.1:8767`. The temporary connector was stopped. The launcher now starts only its Python server when `.local/demo/named-origin.txt` is set; it neither reads a tunnel token nor manages the separate Windows service.
- All 23 Python tests passed. New checks cover exact named-domain Host/Origin acceptance, unrelated-origin rejection, malformed-origin rejection, saved configuration/quick fallback, and starting/stopping only the owned server in named mode.
- Live HTTPS checks using the Windows HTTP client: landing 200; anonymous health/audio 401; login 200 with HttpOnly/Secure/SameSite=Strict cookie; authenticated health/audio 200 (26,352-byte AU focus clip); studio and private share file 404; `.env` 403; unrelated-origin POST 403. A separate Python HTTP probe received 403 before an app request was logged; Windows HTTP checks succeeded. No browser rehearsal or new paid AI call was performed in this hostname-only migration.
- Address remains stable across restarts; the launcher still generates a new classroom code and invalidates old login sessions. After a PC reboot, start the Python app using `start-internet-demo.cmd`, even if the Cloudflare service is already running. PC uptime, network availability and classroom-device testing remain relevant limitations.
- Updated the classroom guide, README and distributable. Local hostname configuration, credentials and private runtime files remain outside the ZIP.

## November 25, 2026 — v3.1 feedback and test-style revision

- Added a correct/incorrect overview with selected/correct letters after all three diagnostic answers, before the learner's reason and the source explanation. This avoids interrupting the three-item diagnostic while making the error explicit.
- TOEIC Part 2 and TEPS show letter-only choices by default, with optional transcript disclosure recorded as reading support. The listen-first guard now checks both the TEPS dialogue and its question/options. Original TOEIC Part 2 transfer items were rewritten as response-selection questions; Part 3 transfer audio is conversational; Part 4 uses announcement/message register. TEPS Part 3 uses three independent dialogues with one question each. Format sources are linked in PRODUCT.md. These remain learning adaptations with replays, not official timed tests.
- Added opt-in Azure scripted pronunciation assessment with accuracy, fluency, completeness, recognized text and word-level feedback. A fixed model-sentence recording is separate from the learner-created sentence. Feedback can be acted on by re-recording; a written practice note and self-check are required before the next stage. Direct/peer comparison remains available without microphone use. Scores use en-US only and must not be treated as accent quality rankings, comprehension scores or official exam scores.
- Validation: 30 Python tests and 23 JavaScript checks passed. Covered consent, authentication, request budgets, WAV format/duration/truncation, known reference sentence, missing scores/no-match, exact raw response logging, spoken options, separate TEPS dialogues, audio prerequisites, PCM encoding, and rejecting old-content coach requests.
- Browser: completed a Part 2 diagnostic with one deliberate wrong answer; overview showed 2/3 with A vs B for the error. Reasoning, omitted-word detection, correction, expression task, pronunciation-note requirement, direct-comparison fallback, and transfer result 1/1 passed. Reading support was correctly labeled. TEPS showed A–D only and blocked answer selection before required audio/support. No browser console errors observed. This was QA, not a learner trial or human pronunciation test.
- Azure live service check: synthetic Jenny speech, not a person, returned accuracy 97, fluency 100, completeness 100 and seven word results in about 0.85 seconds. Exact parameters/raw output and synthetic-fixture labeling are retained privately. This verifies integration only. Microphone capture/browser decoding and meaningful feedback for a real learner still need a classroom-device test.
- Audio: 35 active scripts × 3 accents = 105 files checked against script text, SSML hash and file hash. Longest estimated duration is about 34.3 seconds (48 kbps MP3 byte-rate estimate, not a timed listening study). Changed clips have versioned IDs; original recording hashes remain intact for saved sessions. One Azure network timeout was recovered by reusing completed files and retrying remaining requests.
- The existing homepage copy edits and neutral learning-guide tone were preserved. Refresh and start a new practice session for revised content; older saved sessions retain their original content snapshot and audio. Updated UI/server/data, evidence records and classroom ZIP are included in the release workflow; credentials and evidence are excluded from the ZIP.
- Final deployed HTTPS check: classroom login and authenticated home succeeded at https://ael.52sierra.net/. The pronunciation endpoint returned accuracy 97, fluency 100, completeness 100 and seven word results for the explicitly synthetic fixture in about 1.62 seconds end to end. Revised Australian audio returned HTTP 200; private pronunciation.py returned HTTP 404. Public browser home loaded successfully after authentication. This verifies deployment and integration, not real microphone capture or learner performance.

## November 25, 2026 — v3.2 speaker references

- Replaced order-based references (first/second speaker), unnamed Alex/Morgan references, and A/B dialogue labels in the active trainer with Woman/Man. TOEIC Part 3 and TEPS questions now ask about the man; corresponding Korean explanations and TEPS pronouns identify the same person. Answer keys and learning objectives are unchanged.
- Explicit Woman/Man roles select the corresponding female/male Azure voices in US, UK and AU, independently of speaking order. Narrator remains separate from the dialogue roles. The previous name-based mapping remains supported for archived/custom material.
- Four changed TEPS question/transfer scripts require 12 new recordings across the three accents. Label-only changes reuse 42 recordings after verifying identical SSML and audio hashes. New clip IDs preserve older saved sessions and original evidence; no historical output was rewritten.
- Automated validation: 33 Python tests and 23 JavaScript checks passed, including reversed speaking order, script/voice roles, exact oral question/options agreement and answer-evidence attribution.
- This is a two-person demo. For a future three-person conversation, identify an individual by an explicitly introduced name or role; do not use an ambiguous singular man/woman or add a third person while alternating only two voices. ETS examples also use collective references such as the men when both men are intended: https://www.eu.ets.org/content/dam/ets-org/eu/pdfs/toeic/toeic-listening-and-reading-sample-test.pdf
- Release verification: all 105 active audio files match the current script, SSML hash and file hash; all 60 previous manifest entries remain unchanged. The local app had been stopped, so it was restarted using the existing named Cloudflare connector. Authenticated public HTTPS returned content version 3.2 and the revised Australian TEPS question audio (HTTP 200, 103536 bytes). This was a content/delivery check; no new learner trial or human listening-quality assessment was performed.


## Simplified feedback flow — November 25, 2026

- All-correct diagnostics now complete without selecting a fallback target, remedial stages, transfer recheck or scheduled error review. Old unfinished all-correct extension drafts also exit that route. Completed history is retained.
- Step 2 contains one learner-reason field and a GPT reply. The server supplies the actual selected answer and trusted script/key to the model. No additional question field or rewritten-explanation requirement remains. Exact requests and raw outputs are still retained. Provider failures visibly offer the prepared explanation.
- Correct first dictation has no rewrite field or correction check. Incorrect dictation retains correction practice.
- Step 5 is optional model listening, recording and Azure feedback. Required reflection, sentence creation and checkboxes were removed; word-level scores remain in a disclosure. This reduces required production and interaction compared with the earlier design; no pedagogical gains are asserted.
- 35 Python tests and 32 JavaScript checks passed, including seven UI flow tests executing the actual event handlers. Browser QA confirmed perfect-score completion, correct dictation advancing directly, and step 5 continuing without microphone or writing. The preview server could not reach OpenAI and correctly displayed its fallback. QA used text support and deliberate inputs, not real learner observations.
- Public release check: authenticated HTTPS GPT feedback succeeded in 4.52 seconds using a labeled QA reason (confusing the 11:00 meeting with arrival time). The reply directly addressed that reason, cited ten minutes early, and identified B / 10:50, without asking another question. Exact request, raw response and timing are retained in .local/evidence/qa-simple-reason-feedback.json. Updated public UI text was also verified. Classroom app was restarted; Cloudflare service was retained.
