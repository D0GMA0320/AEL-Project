# Classroom delivery

## Recommended: prepared audio + portable copy

Use the machine that will run the presentation, or bring a laptop and connect it to the classroom projector. Prepare Azure audio once on the development PC. Copy the extracted portable folder using a USB drive. Open `index.html` in Chrome or Edge. There are no externally hosted fonts, frameworks, or CDN assets. Quizzes and prepared explanations do not require internet access.

**An empty audio manifest is not a completed audio demo.** Before class, generate MP3s, play each one, then rebuild and copy the ZIP. Browser speech remains an optional fallback only when the exact requested locale exists.

## Live AI mode

On a PC with Python 3.10+, configure `.env` locally and launch `start-classroom.cmd`. Open the printed localhost URL. Internet access is needed only for explicit Live AI actions. Audio remains pre-generated and local. The app records API request latency; it does not promise a response time before testing.

The server binds only to `127.0.0.1`. It is not a classroom LAN server or a public deployment. This intentionally avoids exposing paid API access. If you use Remote Desktop to the prepared development machine, keep the browser and server there; verify projector display and audio forwarding beforehand. Remote access software setup is outside this delivered package.

## If the classroom PC has no Python

Use the file-based portable edition with prepared explanations. For chatbot explanation, export a prompt and use ChatGPT manually if permitted; record the exact model, date, prompt and unchanged response yourself. Do not label prepared explanations as live-generated AI.

## Rehearsal checklist

- [ ] Prepare and listen to all three accents for the selected lesson.
- [ ] Test a missing or unavailable audio case; verify that no different accent is substituted.
- [ ] Test speaker volume on the actual presentation machine.
- [ ] Complete one lesson, one wrong answer, targeted follow-up, and explanation.
- [ ] Export the JSON and verify it opens and contains the actual voice and conditions.
- [ ] Test one Live AI request and inspect `.local/evidence` for unchanged response data.
- [ ] Record the real request latency. Use prepared explanations if it disrupts the demo.
- [ ] Rehearse the full screen recording; trim to at most 90 seconds without presenting edits as live latency.
- [ ] Keep a PDF of the slides, a screen recording, the portable app and evidence JSON on USB.
- [ ] Avoid displaying API credentials during screen recording or projection.

## Data and rollback

The original one-file prototype is preserved at `docs/original-prototype.html`. No existing `.env` is overwritten by application updates. Browser records are local to the browser and origin: file-based and localhost sessions may have different storage. Export before switching machines, browser profiles or origins. Treat shared-classroom browser storage as temporary; use an anonymous learner label and keep exported evidence with the group.
