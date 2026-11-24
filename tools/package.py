"""Package only allowlisted classroom files; exclude all secrets and private evidence."""
from pathlib import Path
from zipfile import ZipFile, ZIP_DEFLATED
import hashlib
import json

ROOT = Path(__file__).resolve().parents[1]


def package():
    out = ROOT / 'dist'
    out.mkdir(exist_ok=True)
    path = out / 'AEL-Classroom.zip'
    files = [ROOT / p for p in ['index.html', 'server.py', 'start-classroom.cmd', 'configure-services.cmd', 'prepare-classroom.cmd', '.env.example', 'README.md']]
    for directory in ['assets', 'docs', 'tools', 'tests']:
        files.extend(p for p in (ROOT / directory).rglob('*') if p.is_file() and '__pycache__' not in p.parts and p.suffix not in {'.pyc'} and not any(x.startswith('.') for x in p.relative_to(ROOT).parts))
    with ZipFile(path, 'w', ZIP_DEFLATED) as archive:
        for file in files:
            archive.write(file, 'AEL-Classroom/' + file.relative_to(ROOT).as_posix())
    print(path)
    print('SHA256:', hashlib.sha256(path.read_bytes()).hexdigest())
    manifest = (ROOT / 'assets/audio-manifest.js').read_text(encoding='utf-8')
    if not '.mp3' in manifest:
        print('NOTICE: No Azure MP3s are registered yet. Browser voice availability varies; generate audio and rebuild before class.')
    return path


if __name__ == '__main__':
    package()
