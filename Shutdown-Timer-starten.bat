@echo off
cd /d "%~dp0"
pythonw.exe "%~dp0shutdown_timer.py"
if errorlevel 1 python.exe "%~dp0shutdown_timer.py"
