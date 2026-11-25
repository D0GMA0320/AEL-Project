"""Bounded, scripted Azure pronunciation assessment. Audio is never written to disk."""
import base64
import binascii
import hashlib
import io
import json
import math
import os
import re
import time
import urllib.error
import urllib.request
import wave

MAX_BODY = 1_300_000


def prepare(obj, root):
    if obj.get('consent') is not True:
        raise ValueError('녹음 전송에 동의한 뒤 발음 확인을 눌러 주세요.')
    data = json.loads((root / 'assets' / 'trainer-data.json').read_text(encoding='utf-8-sig'))
    pack = next((p for p in data['packs'] if p['id'] == obj.get('pack')), None)
    question = next((q for q in pack['questions'] if q['id'] == obj.get('questionId')), None) if pack else None
    if not question or obj.get('referenceText') != question['dictation']:
        raise ValueError('연습 문장이 업데이트되었습니다. 새 연습을 시작해 주세요.')
    encoded = obj.get('audio')
    if not isinstance(encoded, str) or not 1 <= len(encoded) <= 1_280_100:
        raise ValueError('녹음 길이를 확인해 주세요.')
    try:
        audio = base64.b64decode(encoded, validate=True)
        with wave.open(io.BytesIO(audio), 'rb') as wav:
            if (wav.getnchannels(), wav.getsampwidth(), wav.getframerate(), wav.getcomptype()) != (1, 2, 16000, 'NONE'):
                raise ValueError('16 kHz 모노 PCM WAV 녹음이 필요합니다.')
            frames = wav.getnframes()
            if not 8000 <= frames <= 480000 or len(wav.readframes(frames)) != frames * 2:
                raise ValueError('0.5~30초의 완전한 녹음이 필요합니다.')
    except (binascii.Error, wave.Error, EOFError) as error:
        raise ValueError('녹음 파일을 읽을 수 없습니다. 다시 녹음해 주세요.') from error
    return audio, question['dictation'], frames / 16000


def summarize(raw):
    if raw.get('RecognitionStatus') != 'Success' or not raw.get('NBest'):
        raise ValueError('문장을 인식하지 못했습니다. 조용한 곳에서 모델 문장을 다시 읽어 주세요.')
    best = raw['NBest'][0]
    scores = best.get('PronunciationAssessment', best)

    def score(obj, key):
        value = obj.get(key)
        return round(value, 1) if isinstance(value, (int, float)) and not isinstance(value, bool) and math.isfinite(value) and 0 <= value <= 100 else None

    result = {key: score(scores, key) for key in ('AccuracyScore', 'FluencyScore', 'CompletenessScore')}
    if result['AccuracyScore'] is None:
        raise ValueError('Azure가 발음 정확도 결과를 반환하지 않았습니다. 점수를 추정하지 않습니다.')
    words = []
    for word in best.get('Words', []):
        assessment = word.get('PronunciationAssessment', word)
        words.append({'word': str(word.get('Word', ''))[:100], 'accuracy': score(assessment, 'AccuracyScore'),
                      'error': str(assessment.get('ErrorType', 'None'))[:50]})
    return {'scores': result, 'words': words, 'recognizedText': best.get('Display', raw.get('DisplayText', ''))}


def assess(prepared, request_id, record_evidence, utc):
    audio, reference, seconds = prepared
    key, region = os.environ.get('SPEECH_KEY', ''), os.environ.get('SPEECH_REGION', '')
    if not key or not re.fullmatch(r'[a-z0-9]+', region):
        raise ValueError('발표자가 Azure Speech 키와 지역을 설정해야 합니다. 직접 비교로 계속할 수 있어요.')
    parameters = {'ReferenceText': reference, 'GradingSystem': 'HundredMark', 'Granularity': 'Phoneme',
                  'Dimension': 'Comprehensive', 'EnableMiscue': True}
    evidence = {'kind': 'azure-pronunciation', 'requestId': request_id, 'startedAt': utc(),
                'provider': 'Azure AI Speech', 'locale': 'en-US', 'modelVersion': 'Not reported by endpoint',
                'request': parameters, 'audioSha256': hashlib.sha256(audio).hexdigest(),
                'durationSeconds': seconds, 'audioStored': False}
    request = urllib.request.Request(
        f'https://{region}.stt.speech.microsoft.com/speech/recognition/conversation/cognitiveservices/v1?language=en-US&format=detailed',
        data=audio, headers={'Ocp-Apim-Subscription-Key': key,
        'Content-Type': 'audio/wav; codecs=audio/pcm; samplerate=16000',
        'Pronunciation-Assessment': base64.b64encode(json.dumps(parameters).encode()).decode()}, method='POST')
    started = time.monotonic()
    try:
        with urllib.request.urlopen(request, timeout=25) as response:
            raw_text = response.read(1_000_000).decode('utf-8')
        raw = json.loads(raw_text)
        evidence.update(rawResponseText=raw_text, rawResponse=raw, completedAt=utc(), latencyMs=round((time.monotonic()-started)*1000))
        record_evidence(evidence)
        result = summarize(raw)
        return {**result, **{k: evidence[k] for k in ('requestId','locale','request','rawResponseText','latencyMs')}, 'referenceText': reference}
    except urllib.error.HTTPError as error:
        evidence.update(error=f'Azure HTTP {error.code}', completedAt=utc())
        record_evidence(evidence)
        raise ValueError(f'Azure 발음 확인 요청 실패 (HTTP {error.code}). 직접 비교하거나 잠시 후 다시 시도하세요.') from None
    except (urllib.error.URLError, TimeoutError):
        evidence.update(error='Network error or timeout', completedAt=utc())
        record_evidence(evidence)
        raise ValueError('발음 확인 연결이 지연됩니다. 직접 비교로 계속할 수 있어요.') from None
