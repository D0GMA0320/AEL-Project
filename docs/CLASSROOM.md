# Classroom internet demo from this PC

## Existing Cloudflare account and stable address

This PC is configured for **https://ael.52sierra.net**. The account's `Cloudflared` Windows service routes that hostname to `http://127.0.0.1:8767`. The app launcher starts only the classroom server in this mode; it does not start a second connector or read your tunnel token.

1. Keep the `Cloudflared` Windows service running. Start the app with `start-internet-demo.cmd`.
2. Open the stable address and use the new classroom code from the launcher or `.local/demo/share.txt`. The address stays the same across restarts; the code and login sessions do not.
3. Keep this PC powered and online. The Windows service starts the tunnel only, **not the Python app**. After reboot, run the app launcher again.
4. `stop-internet-demo.cmd` stops the classroom server; the separate Cloudflare service remains running. The public app is unavailable until the server starts again.

The local setting `.local/demo/named-origin.txt` contains only `https://ael.52sierra.net`. It is not included in the classroom ZIP. On another PC, set up the connector there and create this file with your chosen HTTPS hostname (no trailing slash). The server accepts that exact hostname and origin; it does not accept arbitrary domains. Configure the published route with its default Host header.

For a temporary fallback, stop the current demo and run `python tools/internet_demo.py --quick`. The saved named address is used again on the next normal launch. An explicit `--public-url https://your-host.example` overrides the saved address for one launch only.

## Temporary tunnel on an unconfigured PC

1. Run `start-internet-demo.cmd`. First use downloads Cloudflare's official Windows tunnel binary into `.local/demo/` and verifies the SHA256 digest supplied by the GitHub release. No machine-wide install.
2. Copy the HTTPS address and classroom code displayed in that window. They are also in `.local/demo/share.txt`. Keep that file private to the presenters/class.
3. Open the address on a phone using mobile data, enter the classroom code, and test one audio clip and one AI question.
4. Keep the host PC on, powered, connected, and the demo process running throughout class. While the launcher runs it requests Windows stay awake; it does not change power settings. Sleep, reboot, network loss, or stopping the launcher interrupts service.
5. Run `stop-internet-demo.cmd` afterward. A new launch gives a **new address and code**. Existing URLs are not permanent.

No port forwarding, Proxmox, domain, or Cloudflare account is required for this temporary tunnel. Cloudflare carries the HTTPS traffic between visitors and the local app. Quick Tunnels have no uptime guarantee and are intended for tests/demos, not production. [Cloudflare documentation](https://developers.cloudflare.com/tunnel/get-started/quick-tunnels/).

## What is exposed

The tunnel reaches only the classroom server on `127.0.0.1:8767`. Regular local presenter work uses port 8765. The public mode denies `/studio.html`, arbitrary `/api/chat` generation, `.env`, `.local`, server source, and directory traversal. The learner page's static code/content can be downloaded without a code; audio, provider status and coach requests require an authenticated session. API keys remain in the local `.env`.

Entry cookies expire after 8 hours; sign in again with the same classroom code. A service restart also invalidates sessions. AI limits are shared by coach and pronunciation requests: 3 requests/minute/session, 100 requests total per server run, one provider call at a time. If busy, learners use the prepared explanation or direct sound comparison.

Pronunciation is opt-in: record the displayed model sentence (maximum 28 seconds), then press the explicitly labeled Azure upload button. The browser converts the recording to 16 kHz mono PCM WAV. The authenticated endpoint accepts only 0.5–30 seconds, a known lesson sentence and explicit consent. Azure receives the recording; the server does not save the audio file. Exact assessment parameters, raw provider output, recognized words, scores and an audio hash are retained as experiment evidence. The browser retains the recording only temporarily; assessment results are part of its saved session. Do not record personal information.

Scores use the en-US assessment model, irrespective of the listening accent. A US model recording is provided for comparison. The numbers are pronunciation practice feedback, not accent rankings, meaning/intelligibility judgments or TOEIC/TEPS scores. When the microphone or Azure is unavailable, compare directly with the model or skip the optional step. Human recording quality and microphone permission still need checking on the classroom device.

## Tomorrow's 90-second demonstration

Preflight before class: open on mobile data; test audio; test the AI tutor; check Windows won't reboot during the presentation; have a prerecorded backup. Use a completed rehearsal or explain that the demonstration compresses a 6–8 minute session.

- 0–15s: open the link on a second device, select TOEIC Part 3 and AU accent.
- 15–30s: show a wrong answer about 11:00 versus arriving ten minutes early; show the correct/incorrect overview before continuing to clues.
- 30–45s: learner enters one reason for their choice; GPT replies directly with the relevant clue.
- 45–60s: show the linked dictation correction and expression task.
- 60–75s: show optional model listening, recording and pronunciation feedback; no written reflection is required. Use a prepared rehearsal recording if live recording would exceed the demo time.
- 75–90s: new-context question, separate result counts, tomorrow's retrieval task.

Do not claim the demo proves learning gains. Full participant timing and delayed recall still need measurement. Do not show `.env` or provider keys in the recording.

## Fallback and troubleshooting

- Named URL unavailable: confirm the `Cloudflared` Windows service is running and the tunnel is Healthy in the account dashboard; confirm its route is `http://127.0.0.1:8767`; check `.local/demo/server.log`. Restarting the app keeps the same hostname. Connector service logs are separate from the app's temporary-tunnel log.
- Temporary URL unavailable: check `.local/demo/tunnel.log` and `.local/demo/server.log`; restart for a new URL. Restricted networks may block the tunnel's outbound connection. Use the local page or classroom ZIP if required.
- Port 8767 already in use: stop the old demo using `stop-internet-demo.cmd`, wait for it to exit, then restart. Do not terminate unrelated processes.
- AI busy/limit/error: prepared explanations and cached audio remain usable.
- Microphone denied: compare directly with the model or press “새 문제로 →” without recording or writing. HTTPS is required for microphone access on remote devices.
- Logs/evidence and `.env` are deliberately excluded from the ZIP. Transfer selected redacted evidence separately if needed for slides.
