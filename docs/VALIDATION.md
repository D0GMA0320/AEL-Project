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
