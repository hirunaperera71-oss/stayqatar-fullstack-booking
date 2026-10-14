@echo off
title StayQatar Advanced
python -m venv venv
call venv\Scripts\activate
python -m pip install --upgrade pip
pip install -r requirements.txt
python app.py
pause
