@echo off
SETLOCAL

:: Directorio absoluto donde está instalado el proyecto
SET INSTALL_DIR=c:\Users\DESARROLLADOR\Documents\www\code_reviewer

:: Ruta al ejecutable de Python del entorno virtual
SET PYTHON_EXE=%INSTALL_DIR%\.venv\Scripts\python.exe

:: Ejecutar el script menu.py y pasar todos los argumentos adicionales
"%PYTHON_EXE%" "%INSTALL_DIR%\menu.py" %*

ENDLOCAL
