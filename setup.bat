@echo off
setlocal
chcp 65001 >nul
cd /d "%~dp0"
if exist .venv\Scripts\python.exe goto checkvenv
where py >nul 2>&1
if errorlevel 1 goto usepython
py -3 -c "import sys; sys.exit(0 if sys.version_info >= (3,11) else 1)"
if errorlevel 1 goto pythonerror
py -3 -m venv .venv
if errorlevel 1 goto failed
goto checkvenv
:usepython
python -c "import sys; sys.exit(0 if sys.version_info >= (3,11) else 1)"
if errorlevel 1 goto pythonerror
python -m venv .venv
if errorlevel 1 goto failed
:checkvenv
.venv\Scripts\python.exe -c "import sys; sys.exit(0 if sys.version_info >= (3,11) else 1)"
if errorlevel 1 goto pythonerror
.venv\Scripts\python.exe -m pip install -r requirements.txt
if errorlevel 1 goto failed
exit /b 0
:pythonerror
echo Python 3.11 or newer is required. Install Python, then reopen this terminal.
echo If .venv was copied from another computer, rename it and run again.
exit /b 1
:failed
echo Setup failed. Keep this error output and ask Codex to diagnose it.
exit /b 1
