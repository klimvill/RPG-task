@echo off
call .venv\Scripts\activate.bat
python -c __import__('RPGtask.interface').Interface()
