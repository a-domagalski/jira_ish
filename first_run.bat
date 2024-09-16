REM Uncomment, create venv if not created already and install requirements
REM python -m venv /path/to/new/virtual/environment
REM pip install -r requirements.txt
set FLASK_APP=app.py
set FLASK_DEBUG=1
flask db migrate -m "Initial migration"
flask run