@echo off
chcp 65001 >nul
cd /d "%~dp0"
call setup.bat
if errorlevel 1 goto end
.venv\Scripts\python.exe run.py
:end
pause
