@echo off
echo Starting FastAPI server...
echo.
echo Make sure PostgreSQL is running and the database is set up!
echo Run 'python setup_database.py' if you haven't already.
echo.
python -m uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
pause