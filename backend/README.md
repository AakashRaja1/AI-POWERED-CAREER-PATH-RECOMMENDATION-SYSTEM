# Backend (FastAPI) scaffold
# Backend (FastAPI) — AI Career Path Recommendation

This folder contains the FastAPI backend for the project. Below are quick run and migration instructions.

Prerequisites

- Python 3.11+ (or your project's chosen interpreter)
- PostgreSQL running locally (or remote) with a database created for this project

Quick start (Windows / PowerShell)

1) Create & activate virtualenv

```powershell
python -m venv venv
& ".\venv\Scripts\Activate.ps1"
```

2) Install dependencies

```powershell
pip install -r requirements.txt
```

3) Configure environment

Create `backend/.env` with your DB URL and model path:

```
DATABASE_URL=postgresql://postgres:<PASSWORD>@localhost:5432/career_recommendations
MODEL_PATH=model_artifacts
```

4) Initialize DB tables (one-off)

```powershell
# ensure PYTHONPATH includes backend
$env:PYTHONPATH = "$(Resolve-Path .)"
python -c "from app.database.init_db import init_db; init_db(); print('DB created')"
```

5) Run Alembic migrations

```powershell
alembic upgrade head
```

6) Start the API server

```powershell
cd backend
& "..\venv\Scripts\Activate.ps1"
$env:PYTHONPATH = "$(Resolve-Path .)"
python -m uvicorn app.main:app --host 127.0.0.1 --port 8000
```

7) Test endpoints

- Swagger UI: http://127.0.0.1:8000/docs
- POST `/api/predict` with the 14-field payload (see column headers in `LatestCareerdataset.csv`)
- GET `/api/predictions` to list recent saved predictions

Run tests

```powershell
pytest -q
```

Notes & troubleshooting

- If you see SQL auth errors, verify `DATABASE_URL` in `backend/.env` and that Postgres is running and accessible.
- To regenerate `requirements.txt` from your venv:

```powershell
pip freeze > backend/requirements.txt
```

If you'd like, I can add CI integration to run migrations and tests automatically.
