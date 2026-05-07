# AI Powered Career Path Recommendation System

This repository contains a career recommendation system that uses personality and behavior analysis to suggest career paths. It includes a `backend` (FastAPI + ML pipelines) and `frontend` (Vite + React).

## Contents

- `backend/` — FastAPI backend, database migrations, training pipelines, and tests.
- `frontend/` — React frontend built with Vite.
- `.github/workflows/ci.yml` — CI pipeline (runs tests on push/pull_request to `main`).

## Quick start (development)

Prerequisites:

- Python 3.10
- Node 18+ and npm or yarn
- PostgreSQL (for running the backend locally) or Docker

Backend (local):

1. Create a virtual environment and activate it:

```bash
python -m venv .venv
source .venv/bin/activate   # on Windows: .venv\Scripts\activate
```

2. Install backend dependencies:

```bash
cd backend
python -m pip install --upgrade pip
pip install -r requirements.txt
```

3. Set up the database (Postgres):

Create a PostgreSQL database named `career_recommendations_test` (or set `DATABASE_URL` to a test DB) and run migrations:

```bash
export DATABASE_URL=postgresql://postgres:postgres@localhost:5432/career_recommendations_test
alembic upgrade head
```

4. Run tests:

```bash
pytest -v
```

Frontend (local):

```bash
cd frontend
npm install
npm run dev
```

## CI notes and recent fix

The GitHub Actions CI uses a Postgres service container. A recent CI failure occurred when the runner attempted to bind the Postgres service to the host port `5432:5432`, which can conflict with the runner environment and cause an immediate failure. The workflow has been updated to remove explicit host port binding so the service uses the container networking provided by Actions.

If CI still fails, check the Actions run logs for the failing step and include the error output here (or open an issue). Common fixes:

- Ensure `backend/requirements.txt` installs cleanly on Ubuntu runners (binary wheels or build tooling required).
- Increase service health retries or add a wait before migrations if DB initialization is slow.
- If tests rely on external services, mock them or add additional service containers.

## Troubleshooting

- If alembic fails: confirm `DATABASE_URL` in environment points to a reachable Postgres instance and migrations are present under `backend/alembic`.
- If `pip install` fails on CI due to missing system libs, consider adding a step to install apt packages (e.g., `libpq-dev`, `build-essential`) in the workflow before `pip install`.

## Reproducing CI locally

You can reproduce the CI steps locally using Docker Compose or by running the workflow steps manually (install Python, install requirements, run alembic, run pytest). See `.github/workflows/ci.yml` for exact steps.

---

If you want, I can:

- Run the CI steps locally and report the failing command/output.
- Further harden the CI workflow (add apt-get install, longer DB wait, caching).
- Improve this README with architecture diagrams and more contributor instructions.

Let me know which next step you prefer.
