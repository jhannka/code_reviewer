@echo off
set SCRIPT_DIR=%~dp0
set PROJECT_DIR=%SCRIPT_DIR%..

set PYTHONPATH=%PROJECT_DIR%
"%PROJECT_DIR%\.venv\Scripts\python.exe" "%PROJECT_DIR%\menu.py" %*
