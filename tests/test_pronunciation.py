import base64
import io
import json
import os
from pathlib import Path
import sys
import unittest
import wave
from unittest.mock import MagicMock, patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import pronunciation as p

ROOT = Path(__file__).resolve().parents[1]

def audio(rate=16000, seconds=1):
    out = io.BytesIO()
    with wave.open(out, 'wb') as wav:
        wav.setnchannels(1); wav.setsampwidth(2); wav.setframerate(rate)
        wav.writeframes(b'\0\0'*int(rate*seconds))
    return out.getvalue()

def request(**changes):
    return {'pack':'toeic2','questionId':'t2-1','referenceText':'I have a client dinner that evening.',
            'audio':base64.b64encode(audio()).decode(),'consent':True,**changes}

class PronunciationTests(unittest.TestCase):
    def test_rejects_unconsented_unknown_or_changed_reference(self):
        for obj in [request(consent=False),request(questionId='missing'),request(referenceText='arbitrary text')]:
            with self.assertRaises(ValueError):p.prepare(obj,ROOT)
    def test_audio_format_length_and_integrity(self):
        for wav in [b'invalid',audio(rate=8000),audio(seconds=0.1),audio(seconds=31),audio()[:-100]]:
            with self.assertRaises(ValueError):p.prepare(request(audio=base64.b64encode(wav).decode()),ROOT)
        with self.assertRaises(ValueError):p.prepare(request(audio='!not base64!'),ROOT)
        self.assertEqual(p.prepare(request(),ROOT)[2],1)
    def test_no_speech_or_missing_score_never_fabricates_accuracy(self):
        for raw in [{'RecognitionStatus':'NoMatch'},{'RecognitionStatus':'Success','NBest':[{'Display':'test'}]}]:
            with self.assertRaises(ValueError):p.summarize(raw)
    def test_direct_and_nested_scores_and_omissions(self):
        for nested in (False, True):
            scores={'AccuracyScore':81.123,'FluencyScore':72,'CompletenessScore':90}
            word={'AccuracyScore':0,'ErrorType':'Omission'}
            best={**({'PronunciationAssessment':scores} if nested else scores),'Display':'a test',
                  'Words':[{'Word':'a',**({'PronunciationAssessment':word} if nested else word)}]}
            result=p.summarize({'RecognitionStatus':'Success','NBest':[best]})
            self.assertEqual(result['scores']['AccuracyScore'],81.1)
            self.assertEqual(result['words'][0]['error'],'Omission')
    def test_provider_request_and_raw_evidence_without_audio_or_key(self):
        raw=json.dumps({'RecognitionStatus':'Success','NBest':[{'AccuracyScore':90,'Display':'Test'}]})
        response=MagicMock();response.__enter__.return_value.read.return_value=raw.encode()
        record=MagicMock()
        with patch.dict(os.environ,{'SPEECH_KEY':'private-key','SPEECH_REGION':'eastus'}),patch.object(p.urllib.request,'urlopen',return_value=response) as network:
            result=p.assess(p.prepare(request(),ROOT),'test',record,lambda:'test-time')
        sent=network.call_args.args[0]
        params=json.loads(base64.b64decode(sent.headers['Pronunciation-assessment']))
        self.assertEqual(params['ReferenceText'],request()['referenceText'])
        self.assertEqual(result['rawResponseText'],raw)
        saved=record.call_args.args[0]
        self.assertFalse(saved['audioStored']);self.assertNotIn('audio',saved)
        self.assertNotIn('private-key',json.dumps(saved))

if __name__=='__main__':unittest.main()
