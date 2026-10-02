@echo off
chcp 65001 >nul
cd /d "%~dp0"
call setup.bat
if errorlevel 1 goto failed
.venv\Scripts\python.exe -m pip install -r requirements-dev.txt
if errorlevel 1 goto failed
.venv\Scripts\python.exe -m pytest -q
if errorlevel 1 goto failed
echo.
echo Tests passed. Test data is separate from your real site data.
pause
exit /b 0
:failed
echo.
echo Tests or setup failed. Copy the error output to Codex.
pause
exit /b 1
