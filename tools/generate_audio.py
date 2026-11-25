"""Generate reusable Azure MP3s before class. No paid calls during playback."""
import argparse
from datetime import datetime, timezone
import hashlib
import json
import os
from pathlib import Path
import re
import sys
import time
import urllib.error
import urllib.request
from xml.sax.saxutils import escape

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from server import ROOT, load_env

VOICES = {
    'US': ('en-US', 'en-US-JennyNeural', 'en-US-GuyNeural'),
    'UK': ('en-GB', 'en-GB-SoniaNeural', 'en-GB-RyanNeural'),
    'AU': ('en-AU', 'en-AU-NatashaNeural', 'en-AU-WilliamNeural'),
}


def validate_credentials(key, region):
    if not key or len(key) < 20 or not re.fullmatch(r'[\x21-\x7e]+', key) or key.startswith('http') or '=' in key:
        raise ValueError('SPEECH_KEY is missing or incomplete. Run configure-services.cmd, copy the full Azure Speech KEY 1 or KEY 2, and choose C for clipboard input. No request made.')
    if not re.fullmatch(r'[a-z0-9]+', region):
        raise ValueError('SPEECH_REGION must be the resource region code, such as koreacentral or eastus. No request made.')


def read_assignment(path, prefix):
    raw = path.read_text(encoding='utf-8-sig')
    start = raw.index(prefix) + len(prefix)
    return json.loads(raw[start:].strip().rstrip(';'))


def ssml_for(lesson, accent):
    locale, first, second = VOICES[accent]
    speakers = {}
    nodes = []
    for line in lesson['script'].splitlines():
        match = re.match(r'^([A-Za-z ]{1,30}):\s*(.+)$', line)
        if match:
            name, text = match.groups()
            if name not in speakers:
                speakers[name] = first if len(speakers) % 2 == 0 else second
            voice = speakers[name]
        else:
            voice, text = first, line
        if text.strip():
            nodes.append(f'<voice name="{voice}">{escape(text)}<break time="250ms"/></voice>')
    return f'<speak version="1.0" xmlns="http://www.w3.org/2001/10/synthesis" xml:lang="{locale}">' + ''.join(nodes) + '</speak>'


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--lesson', type=Path, help='Optional human-reviewed custom lesson JSON')
    parser.add_argument('--accent', choices=list(VOICES), action='append', help='Generate only selected accents; repeat flag for more')
    parser.add_argument('--trainer', action='store_true', help='Generate the exam trainer and linked practice clips')
    args = parser.parse_args()
    load_env()
    key, region = os.environ.get('SPEECH_KEY'), os.environ.get('SPEECH_REGION', '')
    validate_credentials(key, region)
    if args.lesson:
        lessons = [json.loads(args.lesson.read_text(encoding='utf-8-sig'))]
    elif args.trainer:
        lessons = json.loads((ROOT / 'assets' / 'trainer-clips.json').read_text(encoding='utf-8'))['lessons']
    else:
        # data.js uses JS object syntax; export the content through the bundled Node-free JSON snapshot.
        lessons = json.loads((ROOT / 'assets' / 'lessons.json').read_text(encoding='utf-8'))['lessons']
    for lesson in lessons:
        if not re.fullmatch(r'[A-Za-z0-9_-]{1,60}', lesson.get('id', '')) or not isinstance(lesson.get('script'), str):
            sys.exit('Invalid lesson id or script. No request made.')
    base = f'https://{region}.tts.speech.microsoft.com'
    headers = {'Ocp-Apim-Subscription-Key': key}
    print('Checking Azure voice availability...')
    with urllib.request.urlopen(urllib.request.Request(base + '/cognitiveservices/voices/list', headers=headers), timeout=30) as response:
        available = {v['ShortName'] for v in json.load(response)}
    accents = args.accent or list(VOICES)
    required = {v for a in accents for v in VOICES[a][1:]}
    missing = required - available
    if missing:
        sys.exit('Voices unavailable in this resource: ' + ', '.join(sorted(missing)))
    manifest_path = ROOT / 'assets' / 'audio-manifest.js'
    manifest = read_assignment(manifest_path, 'window.AEL_AUDIO =')
    audio_dir = ROOT / 'assets' / 'audio'
    audio_dir.mkdir(exist_ok=True)
    evidence_dir = ROOT / '.local' / 'evidence'
    evidence_dir.mkdir(parents=True, exist_ok=True)
    for lesson in lessons:
        for accent in accents:
            ssml = ssml_for(lesson, accent)
            digest = hashlib.sha256(ssml.encode()).hexdigest()
            existing = manifest.get(lesson['id'], {}).get(accent, {})
            old_path = ROOT / existing.get('path', 'missing')
            if existing.get('ssmlSha256') == digest and old_path.is_file() and hashlib.sha256(old_path.read_bytes()).hexdigest() == existing.get('sha256'):
                print('Cached:', lesson['id'], accent)
                continue
            request = urllib.request.Request(base + '/cognitiveservices/v1', data=ssml.encode('utf-8'), headers={**headers,
                'Content-Type':'application/ssml+xml', 'X-Microsoft-OutputFormat':'audio-24khz-48kbitrate-mono-mp3', 'User-Agent':'AELClassroom'}, method='POST')
            print('Requesting audio:', lesson['id'], accent)
            for attempt in range(3):
                try:
                    with urllib.request.urlopen(request, timeout=60) as response:
                        audio = response.read()
                    break
                except urllib.error.HTTPError as error:
                    if error.code != 429 or attempt == 2:
                        raise
                    print('Azure rate limit; waiting 30 seconds before retry.', flush=True)
                    time.sleep(30)
            if len(audio) < 100:
                raise ValueError('Azure returned an empty or unexpectedly short audio file')
            path = audio_dir / f'{lesson["id"]}-{accent}.mp3'
            path.write_bytes(audio)
            timestamp = datetime.now(timezone.utc).isoformat()
            entry = {'path':path.relative_to(ROOT).as_posix(), 'script':lesson['script'],
                'voice':' / '.join(sorted(set(re.findall(r'<voice name="([^"]+)"', ssml)))), 'locale':VOICES[accent][0],
                'generatedAt':timestamp, 'sha256':hashlib.sha256(audio).hexdigest(), 'ssmlSha256':digest,
                'provider':'Azure AI Speech', 'modelVersion':'Not reported by synthesis endpoint'}
            manifest.setdefault(lesson['id'], {})[accent] = entry
            manifest_path.write_text('window.AEL_AUDIO = ' + json.dumps(manifest, ensure_ascii=False, indent=2) + ';\n', encoding='utf-8')
            evidence = {'kind':'azure-synthesis', 'at':timestamp, 'lessonId':lesson['id'], 'accent':accent,
                'originalSSML':ssml, 'outputMetadata':entry, 'verification':'Human listening review pending'}
            (evidence_dir / f'azure-{lesson["id"]}-{accent}-{digest[:12]}.json').write_text(json.dumps(evidence, ensure_ascii=False, indent=2), encoding='utf-8')
            print('Generated:', path.name, '(listen and verify before class)')
            # Free F0 allows 20 synthesis transactions per minute.
            time.sleep(3.2)
    print('Done. Rebuild the portable ZIP after verifying the recordings.')


if __name__ == '__main__':
    try:
        main()
    except urllib.error.HTTPError as error:
        hints = {400: 'Azure rejected the request. Re-copy the complete Speech resource key and check the region.',
                 401: 'Check that the key and region belong to the same Speech resource.',
                 403: 'Check the resource access settings and Speech service permissions.',
                 429: 'The Speech rate limit or quota was reached. Wait before retrying.'}
        sys.exit(f'Azure HTTP {error.code}. ' + hints.get(error.code, 'Check Azure service availability and resource settings.') + ' Existing completed files are preserved. Credentials were not logged.')
    except ValueError as error:
        sys.exit(str(error))
    except (urllib.error.URLError, TimeoutError):
        sys.exit('Azure network error or timeout. Existing completed files are preserved. Retry later.')
