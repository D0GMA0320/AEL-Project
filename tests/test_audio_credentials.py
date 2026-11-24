import os
from pathlib import Path
import sys
import unittest
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from tools.generate_audio import main, validate_credentials


class AudioCredentialsTests(unittest.TestCase):
    def test_incomplete_key_stops_before_network(self):
        with patch.dict(os.environ, {'SPEECH_KEY': '\x16', 'SPEECH_REGION': 'koreacentral'}), \
             patch('tools.generate_audio.load_env'), \
             patch('sys.argv', ['generate_audio.py']), \
             patch('urllib.request.urlopen') as request:
            with self.assertRaisesRegex(ValueError, 'SPEECH_KEY is missing or incomplete'):
                main()
            request.assert_not_called()

    def test_rejects_paste_errors_without_echoing_input(self):
        for key in ['', 'v', 'x' * 30 + '\x16', 'x' * 20 + ' y', 'https://example.com/secret', 'SPEECH_KEY=' + 'x' * 32]:
            with self.subTest(length=len(key)):
                with self.assertRaises(ValueError) as error:
                    validate_credentials(key, 'koreacentral')
                if len(key) > 10:
                    self.assertNotIn(key, str(error.exception))

    def test_accepts_full_key_and_requires_region_code(self):
        validate_credentials('a' * 32, 'koreacentral')
        for region in ['', 'Korea Central', 'https://example.com']:
            with self.assertRaisesRegex(ValueError, 'SPEECH_REGION'):
                validate_credentials('a' * 32, region)


if __name__ == '__main__':
    unittest.main()
