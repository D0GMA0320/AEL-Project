# AEL v3: exam practice with linked feedback

A small classroom service for KNU Applied Linguistics group 4. Target: B1–B2 university learners preparing for TOEIC/TEPS who need to understand and repair listening mistakes. Learner level and 6–8 minute duration are design estimates, pending pilot validation.

## Run

- `start-classroom.cmd`: local practice at http://127.0.0.1:8765. Presenter tools: http://127.0.0.1:8765/studio.html.
- `start-internet-demo.cmd`: HTTPS service from **this Windows PC**, with a classroom entry code. This PC uses the existing Cloudflare connector at **https://ael.52sierra.net**; unconfigured copies use a temporary tunnel. No Proxmox or inbound router port needed. See [classroom guide](docs/CLASSROOM.md).
- `stop-internet-demo.cmd`: stop the demo server and any temporary tunnel it started. A separately installed Cloudflare service stays running.
- `configure-services.cmd`: server-side Azure Speech and OpenAI credentials; see [credentials](docs/CREDENTIALS.md).
- `prepare-classroom.cmd`: generate/cache all trainer recordings, then create `dist/AEL-Classroom.zip`. Completed audio is reused.

## Learning flow

Choose TOEIC Part 2/3/4 or TEPS conversation practice, and US/UK/AU accent. Three diagnostic questions route the learner to one actual missed skill: numbers/changed details, intent/reason, or paraphrase. If all are correct, the session is clearly labeled extension practice.

1. State a reason before seeing the explanation.
2. Compare the source clue; optionally ask the AI tutor a question, then revise the explanation.
3. Write the clue sentence from audio; inspect differences and submit a correction.
4. Match an equivalent expression.
5. Shadow the model and produce a new sentence. Optional local recording; no automatic pronunciation scoring.
6. Answer a different transfer item. Save a next-day retrieval task.

The original linked-tab mockups are design references. The public app does not accept provider keys in a browser. The older content studio is preserved at `studio.html`, available only on the local server.

## Boundaries

- Original AI-assisted practice, not official exam questions, a full mock test, or a score predictor. TEPS questions/options have oral recordings; visible options are explicitly a learning aid. TOEIC Part 2 also has spoken options.
- The short fixed bank is a demo: 12 diagnostic questions, 12 transfer questions, and linked practice for each diagnostic item. Repeating a pack repeats its questions.
- Synthesis has preselected locale voices and a cached manifest, not verified human accent ratings. Auditory quality and level need human review.
- Progress is browser-local; export JSON includes exact learner actions, AI responses when used, and content snapshot. No cross-device account or payment service.
- A demo code gates audio and APIs. Public landing assets and practice source files contain no secrets. Public AI is limited to known trainer items, 3 calls/minute/session and 100 calls per server run, with one concurrent provider request. Limits bound requests, not monetary spend. Keys/evidence/host tools are not served.
- Public mode is a temporary classroom setup, not production hosting. Keep this PC powered on and connected.

## Evidence and assessment

[Product and pedagogy](docs/PRODUCT.md) · [presentation plan](docs/PRESENTATION.md) · [validation](docs/VALIDATION.md) · [experiment protocol](docs/EXPERIMENT.md).

Checks: `python -m unittest discover -s tests -p "test_*.py"` and `node --test tests/core.test.cjs tests/trainer.test.cjs`.
