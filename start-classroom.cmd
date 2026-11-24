@echo off
cd /d "%~dp0"
where python >nul 2>nul
if errorlevel 1 (
  echo Python 3.10 or newer is needed for Live AI. For offline practice, open index.html.
  pause
  exit /b 1
)
echo Open http://127.0.0.1:8765 in your browser once the server is ready.
echo Keep this window open during the demonstration. Ctrl+C stops the server.
python server.py
pause
