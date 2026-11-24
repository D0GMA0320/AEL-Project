@echo off
cd /d "%~dp0"
echo Generating Azure audio using your local settings. Existing verified cache files are reused.
python tools\generate_audio.py
if errorlevel 1 (
  echo Audio preparation did not finish. Check the message above. No new classroom ZIP was made.
  pause
  exit /b 1
)
python tools\package.py
echo Listen to the generated voices before class. Extract dist\AEL-Classroom.zip on the classroom PC.
pause
