cd ..
set PYTHON=python

if exist build rd /S /Q build
if exist dist rd /S /Q dist
if exist release rd /S /Q release
if exist venv rd /S /Q venv
%PYTHON% -m venv venv
venv\Scripts\python -m pip install --upgrade pip
venv\Scripts\python -m pip install -r requirements.txt
venv\Scripts\python -m pip install pyinstaller
venv\Scripts\python -m PyInstaller main.spec

rename dist release
if exist build rd /S /Q build
if exist dist rd /S /Q dist
if exist venv rd /S /Q venv
pause