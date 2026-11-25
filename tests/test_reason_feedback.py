import json
from pathlib import Path
import sys
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from server import trainer_prompt


class ReasonFeedbackTests(unittest.TestCase):
    def body(self):
        return {'mode': 'reason-feedback', 'pack': 'toeic3', 'questionId': 't3-1',
                'reason': 'I heard eleven so I chose the meeting time.', 'selectedAnswer': 3}

    def test_reason_alone_includes_actual_choice_and_server_owned_context(self):
        prompt = trainer_prompt(self.body())
        payload = json.loads(prompt.split('\n', 1)[1])
        self.assertEqual(payload['learnerReason'], self.body()['reason'])
        self.assertEqual(payload['selectedAnswer'], 3)
        self.assertEqual(payload['selectedLetter'], 'D')
        self.assertEqual(payload['context']['answer'], 1)
        self.assertIn('ten minutes early', payload['context']['script'])
        self.assertIn('Do not ask a follow-up question', prompt)

    def test_invalid_reason_and_selection_are_rejected(self):
        for change in ({'reason': ''}, {'reason': '  '}, {'reason': 'x' * 1501},
                       {'reason': []}, {'selectedAnswer': True}, {'selectedAnswer': -1},
                       {'selectedAnswer': 4}, {'selectedAnswer': '3'}):
            with self.subTest(change=change):
                with self.assertRaises(ValueError):
                    trainer_prompt({**self.body(), **change})


if __name__ == '__main__':
    unittest.main()
