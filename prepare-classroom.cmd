@echo off
cd /d "%~dp0"
echo Generating exam trainer audio using your local Azure settings.
python -u tools\generate_audio.py --trainer
if errorlevel 1 (
  echo Preparation did not finish. Existing recordings are preserved. Retry to resume.
  pause
  exit /b 1
)
python tools\package.py
echo Review recordings before class. Use start-internet-demo.cmd to share from this PC.
pause
