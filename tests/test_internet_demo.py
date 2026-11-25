import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import MagicMock, patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from tools import internet_demo as demo


class LauncherTests(unittest.TestCase):
    def test_local_named_setting_and_quick_override(self):
        with tempfile.TemporaryDirectory() as folder, patch.object(demo, 'STATE', Path(folder)):
            self.assertIsNone(demo.configured_origin())
            (Path(folder) / 'named-origin.txt').write_text('https://ael.52sierra.net\n', encoding='utf-8')
            self.assertEqual(demo.configured_origin(), 'https://ael.52sierra.net')
            self.assertIsNone(demo.configured_origin(quick=True))
            self.assertEqual(demo.configured_origin('https://other.example'), 'https://other.example')
            (Path(folder) / 'named-origin.txt').write_text('http://unsafe.example')
            with self.assertRaises(ValueError):
                demo.configured_origin()

    def test_named_mode_owns_only_server_and_sets_origin_before_start(self):
        with tempfile.TemporaryDirectory() as folder, patch.object(demo, 'STATE', Path(folder)):
            state = Path(folder)
            process = MagicMock()
            process.poll.return_value = None

            def launch(*args, **kwargs):
                self.assertEqual((state / 'origin.txt').read_text(), 'https://ael.52sierra.net')
                return process

            with patch.object(sys, 'argv', ['internet_demo.py','--public-url','https://ael.52sierra.net','--port','0']), \
                 patch.object(demo, 'install_tunnel') as install, \
                 patch.object(demo.subprocess, 'Popen', side_effect=launch) as popen, \
                 patch.object(demo, 'wait_for_server'), \
                 patch.object(demo.time, 'sleep', side_effect=lambda _: (state / 'stop').write_text('stop')), \
                 patch.object(demo.ctypes, 'windll', create=True), patch('builtins.print'):
                demo.main()
            install.assert_not_called()
            self.assertEqual(popen.call_count, 1)
            self.assertIn('server.py', popen.call_args.args[0][2])
            self.assertIn('https://ael.52sierra.net', (state / 'share.txt').read_text())
            process.terminate.assert_called_once()


if __name__ == '__main__':
    unittest.main()
