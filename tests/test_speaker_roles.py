import json
from pathlib import Path
import re
import sys
import unittest
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from tools.generate_audio import VOICES, ssml_for


class SpeakerRoleTests(unittest.TestCase):
    def test_roles_keep_their_voice_when_turn_order_changes(self):
        for accent, (_, female, male) in VOICES.items():
            with self.subTest(accent=accent):
                xml = ET.fromstring(ssml_for({'script': 'Man: Hello.\nNarrator: Listen.\nWoman: Hi.\nMan: Thanks.'}, accent))
                self.assertEqual([n.attrib['name'] for n in xml], [male, female, female, male])

    def test_legacy_labels_preserve_voice_order(self):
        for accent in VOICES:
            old = ssml_for({'script': 'Alex: Hello.\nMorgan: Hi.\nAlex: Thanks.'}, accent)
            new = ssml_for({'script': 'Woman: Hello.\nMan: Hi.\nWoman: Thanks.'}, accent)
            self.assertEqual(old, new)

    def test_active_scripts_questions_and_spoken_options_agree(self):
        data = json.loads((ROOT / 'assets/trainer-data.json').read_text(encoding='utf-8'))
        clips = json.loads((ROOT / 'assets/trainer-clips.json').read_text(encoding='utf-8'))
        bank = {c['id']: c['script'] for c in clips['lessons']}
        self.assertNotRegex(json.dumps(data, ensure_ascii=False), r'(?i)(first|second|third) speaker|첫 번째 화자|Morgan|Alex')
        for pack in data['packs']:
            for q in pack['questions']:
                self.assertEqual(bank[q.get('audioId', pack.get('audioId'))], q.get('script', pack.get('script')))
                for item in (q, q['retry']):
                    script = item.get('script', pack.get('script'))
                    labels = set(re.findall(r'^([A-Za-z ]+):', script, re.M))
                    if labels:
                        self.assertEqual(labels, {'Woman', 'Man'})
                    if 'the man' in item['prompt']:
                        self.assertIn('Man', labels)
                        if 'evidence' in item:
                            self.assertTrue(any(item['evidence'] in line for line in script.splitlines() if line.startswith('Man:')))
                if pack['exam'] == 'TEPS':
                    for item, audio_id in ((q, q['questionAudio']), (q['retry'], q['retry']['audioId'])):
                        self.assertIn('Narrator: ' + item['prompt'], bank[audio_id])
                        for i, option in enumerate(item['options']):
                            self.assertIn(f'Narrator: {chr(65+i)}. {option}', bank[audio_id])


if __name__ == '__main__':
    unittest.main()
