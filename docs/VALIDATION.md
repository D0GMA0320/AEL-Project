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
