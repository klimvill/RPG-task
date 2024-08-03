@echo off
echo Program is running...

call python -m venv .venv
call .venv\Scripts\activate.bat
echo A virtual environment has been created and activated...

call python -m pip install --upgrade pip
call pip install -r requirements.txt
echo Install requirements...
