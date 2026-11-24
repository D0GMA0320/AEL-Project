# AI Adaptive English Lab

KNU 2026 fall semester Applied Linguistics, group 4 — **AI를 활용한 언어학습**.

A small classroom learning application: accent-diverse listening → contextual comprehension/grammar/vocabulary → rule-based targeted practice → prepared or live AI explanation. Presentation: November 26, 2026.

## Start here

1. **No installation:** open `index.html`. All quizzes, translations, prepared explanations, lesson import and browser-local evidence storage work directly from the folder. Browser speech requires an installed matching accent; missing accents are never substituted.
2. **Reliable classroom audio:** configure Azure locally, double-click `prepare-classroom.cmd` before class, and listen to the recordings. Playback then uses local MP3 files with no synthesis request or network delay.
3. **Live OpenAI feedback:** configure `.env`, then double-click `start-classroom.cmd`. Open `http://127.0.0.1:8765`. Python 3.10+ is required; no third-party Python packages are needed. API access and billing are separate from a ChatGPT subscription.
4. **USB delivery:** run `python tools/package.py`. Extract `dist/AEL-Classroom.zip` on the classroom computer. Do not run it inside the ZIP viewer. Rebuild after generating audio.

## Configure the two services

See [What to enter for each credential](docs/CREDENTIALS.md) for the four fields and their exact sources.

Copy `.env.example` to `.env` in this folder. Fill it locally; never paste keys into chat or commit them.

```dotenv
SPEECH_KEY=your-azure-speech-resource-key
SPEECH_REGION=your-resource-region
OPENAI_API_KEY=your-openai-project-key
OPENAI_MODEL=exact-model-id-available-to-your-project
```

Alternatively double-click `configure-services.cmd`; it prompts for keys without displaying them. The resulting local `.env` is plain text, ignored by Git, excluded from the classroom ZIP, and blocked by the local web server. Environment variables take precedence over `.env`. Restart the server after changing settings.

Audio generation checks Azure's voice list before synthesis. US: Jenny/Guy; UK: Sonia/Ryan; AU: Natasha/William. Dialogues use two voices. API model versions are recorded only when returned; a locale/voice name is not a verified accent-quality rating.

```text
python tools/generate_audio.py
python tools/generate_audio.py --accent AU
python tools/generate_audio.py --lesson reviewed-lesson.json
```

Repeated generation skips files whose SSML and audio hashes match. Azure requests may incur charges. Generate ahead of class, not during the demonstration. Custom lesson IDs and script text must exactly match the reviewed imported lesson for its audio to be selected.

## Simplified interface

The opening screen shows a lesson selector, accent selector and Start button. Playback speed, time limit and learner goals are under Learning settings. Content preparation, experiment evidence and classroom readiness are in the Tools menu. Results keep scripts and AI questions collapsed until needed.

## What is implemented

- Three original practice texts: business scheduling, hotel dialogue, commencement-style speech. Each has two listening and two context questions, Korean translations, answer explanations and evidence.
- An explicit B1–B2 target profile; profile selection records goals but does not claim CEFR diagnosis or rewrite lessons.
- Exact-locale browser speech or pre-generated Azure MP3s; no silent accent fallback. Reading fallback is explicitly labeled and excluded from listening interpretation.
- Untimed practice by default; optional 5/3-second context questions. Readiness button, keyboard shortcuts, paused timing on hidden tabs, and untimed follow-ups.
- Rule-based follow-ups selected from missed skill categories; new challenge items when all initial answers are correct. This is not an AI-generated adaptive testing model.
- Per-session snapshots: passage, all questions/answers, actual voice, rate, replay events, time limits, response times, reading mode and learner goals.
- Prepared explanations and optional live OpenAI coaching through a local backend. The browser never receives API keys.
- Optional AI draft generation from a supplied source. Original passage/source changes and invalid schemas are rejected. Human review is required before adding lessons. Original AI output remains in evidence.
- Optional external Whisper transcript import with separate original and human-checked text; AI grammar/word-choice feedback. No built-in audio transcription, pronunciation scoring or microphone capture.
- Browser-local records and JSON export; server-side exact API requests and unmodified response bodies in `.local/evidence`.

## Limits to present honestly

This is formative practice, not a standardized TOEIC/IELTS assessment, a CEFR test, or a causal learning study. Built-in texts are original AI-assisted drafts, not authentic TED excerpts. Human review and a learner pilot are still needed. Static answer keys are visible in source and are suitable for practice only.

Small question counts, practice effects, different passage difficulty, speaker identity, synthesized prosody, response timing and recognition errors can all confound results. Scores are shown per session, not as an accent ranking. A user-entered transcript cannot establish pronunciation or intelligibility. The software does not invent experiment results or exact model provenance it cannot verify.

## Repository structure

- `assets/data.js` — lesson and follow-up bank; `lessons.json` is its generated snapshot for Python audio preparation.
- `assets/core.js` — validation and adaptation rules; `app.js` — views and learner flow; `style.css` — responsive interface.
- `assets/audio-manifest.js` — audio metadata; `assets/audio/` — generated MP3s.
- `server.py` — localhost-only backend; only allowlisted UI assets are served.
- `tools/` — credentials setup, pre-generation and portable packaging.
- `docs/` — classroom instructions, presentation plan, evidence protocol and preserved initial prototype.
- `.local/evidence/` — private API/synthesis records (not distributed).

After changing `data.js`, regenerate its JSON snapshot:

```text
node -e "const fs=require('fs'),vm=require('vm');const c={window:{}};vm.runInNewContext(fs.readFileSync('assets/data.js','utf8'),c);fs.writeFileSync('assets/lessons.json',JSON.stringify(c.window.AEL_DATA,null,2));"
```

## Validation

```text
node tests/core.test.cjs
python -m unittest discover -s tests -p test_*.py -v
```

Automated tests use mocked OpenAI responses; they do not prove live API access, actual accent quality, classroom speaker output or learning effectiveness. See `docs/VALIDATION.md` for the actual verification record.

## Integration references

- [Azure text-to-speech REST API](https://learn.microsoft.com/en-us/azure/ai-services/speech-service/rest-text-to-speech)
- [OpenAI Responses API](https://developers.openai.com/api/reference/resources/responses/methods/create)

Implementation reference check: November 24, 2026. Do not expose the localhost AI endpoint publicly without adding authentication and usage controls.
