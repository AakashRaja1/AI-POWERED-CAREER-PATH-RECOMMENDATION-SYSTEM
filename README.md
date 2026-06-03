# AI Powered Career Path Recommendation System

## License & Usage

This repository is provided for viewing, learning, and non-commercial research only. It is NOT licensed for production deployment or commercial use. See [LICENSE](LICENSE) and [TERMS.md](TERMS.md) for full details and restrictions.

This repository implements a production-grade system that recommends career paths by combining behavior analysis, personality inference, and curated datasets. It contains a backend (FastAPI) that exposes REST endpoints, ML pipelines for training and inference, and a frontend (Vite + React) for user interaction.

This README documents the full project: architecture, components, data flow, developer setup, testing, training pipelines, CI/CD, deployment options, and troubleshooting.

**Repository layout (top-level):**

- `backend/` — FastAPI application, database migration scripts (Alembic), ML training orchestration, tests, and utilities.
- `frontend/` — Vite + React single page app that consumes backend APIs.
- `ml_personality/`, `ml_personality_pipeline/` — legacy and pipeline code for personality and behavior models.
- `behavior_training/` — behavior-focused training utilities and dataset tooling.
- `datasets/` — raw and processed datasets used for training and experimentation.
- `.github/workflows/ci.yml` — automated CI pipeline used on push and PRs.

**High-level architecture**

1. Data ingestion: raw videos/text and human annotations live under `datasets/`. Preprocessing scripts extract features and create training-ready datasets.
2. Model training: the `ml_personality_pipeline` contains scripts to preprocess, train, and evaluate models (CNNs, MLPs, and ensemble components). Training outputs model artifacts under `ml_personality_pipeline/artifacts`.
3. Backend service: `backend/` exposes REST endpoints for authentication, user management, inference, and training orchestration. It stores persistent state in PostgreSQL and persists model metadata and references to artifacts.
4. Frontend: `frontend/` interacts with the backend for user flows — onboarding, uploading inputs (video/text), and showing recommended career paths.

Architecture diagram (textual):

```
[datasets] -> [preprocessing scripts] -> [feature vectors] -> [training pipelines] -> [model artifacts]
																				 |
																				 v
																	[backend service]
																				 |
																				 v
																		[Postgres DB]
																				 |
																				 v
																		 [frontend]
```

**Backend (detailed)**

- Framework: FastAPI (ASGI) — entrypoint: `backend/app/main.py`.
- App layout: `backend/app/api` contains routers (e.g., `routers/auth.py`), `app/services` has business logic, `app/core` for config, and `app/database` for DB utilities.
- Database: PostgreSQL used in production and CI. Migrations are managed with Alembic in `backend/alembic`.
- Authentication: JWT-based token flow; see `backend/app/api/routers/auth.py` for endpoints and `backend/app/services/auth` for token management.
- Models & Schemas: Pydantic models for request/response shapes are under `backend/app/api/schemas` (search in the repo for `schemas` files).
- Training orchestration: `backend/train.py` and `backend/training_client.py` (and `behavior_training/`) orchestrate long-running training jobs and can queue tasks or call local scripts.

Common backend commands:

1. Create and activate venv:

```bash
python -m venv .venv
# Unix/macOS
source .venv/bin/activate
# Windows (PowerShell)
.venv\\Scripts\\Activate.ps1
```

2. Install dependencies:

```bash
cd backend
python -m pip install --upgrade pip
pip install -r requirements.txt
```

3. Run migrations (ensure `DATABASE_URL` is set):

```bash
export DATABASE_URL=postgresql://postgres:postgres@localhost:5432/career_recommendations
cd backend
alembic upgrade head
```

4. Start the API (development):

```bash
cd backend
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

5. Run tests:

```bash
cd backend
pytest -v
```

Environment variables used by backend (most common):

- `DATABASE_URL` — SQLAlchemy database URL (Postgres): `postgresql://user:pass@host:port/dbname`.
- `SECRET_KEY` — application secret used for signing tokens.
- `ACCESS_TOKEN_EXPIRE_MINUTES` — JWT expiration.
- `MODEL_PATH` — directory where inference model artifacts are stored (used in CI and for local inference).

Check `backend/app/core/config.py` for the exact configuration keys and defaults.

**ML pipelines & training**

The repository contains multiple scripts and pipeline configurations for training models. Key directories and files:

- `ml_personality_pipeline/` — primary pipeline code. Look for `run_full_pipeline.py`, `train.py`, `train_cnn_700.py` and `train_video_model.py` to run training variants.
- `ml_personality/` — old model code and utilities (keep for reference).
- `behavior_training/` — orchestration for behavior-focused models and embedding generation.

Training examples:

CPU training (example):

```bash
cd ml_personality_pipeline
python run_training.py --config configs/cpu_config.yaml
```

GPU training (if available and CUDA configured):

```bash
python train_gpu.py --epochs 50 --batch-size 64
```

Model artifacts are written to `ml_personality_pipeline/artifacts` by default. Scripts that perform inference read from `MODEL_PATH` or the configured artifact path.

**Datasets and preprocessing**

- Raw data: `datasets/first_impressions_download/` and `datasets/sample_dataset/` contain raw inputs and example data.
- Labeling and aggregation: `ml_personality_pipeline/generate_labels.py`, `aggregate_behavior_labels.py` and `generate_all_labels.py` handle creation of training label sets and bootstrap labeling.
- Feature extraction: `feature_extractor.py` and `export_feature_vectors.py` create numerical features used by ML models.

If you are adding new data:

1. Place raw files under `datasets/` with clear subfolders.
2. Update any dataset manifests and run the preprocessing script that matches your modality (video/text/audio).
3. Validate the processed dataset format using `ml_personality_pipeline/dataset_loader.py`.

**Frontend**

- Framework: React + Vite in `frontend/`.
- Start dev server:

```bash
cd frontend
npm install
npm run dev
```

- Build production bundle:

```bash
npm run build
```

The frontend calls backend API endpoints (CORS and proxy settings may be configured in `frontend/vite.config.js` or `frontend/package.json`). Confirm the API base URL in `frontend/src` configuration files.

**CI/CD (GitHub Actions)**

The CI workflow file is: `.github/workflows/ci.yml`.

What CI does (summary):

1. Spins up a Postgres service container.
2. Installs Python and backend dependencies from `backend/requirements.txt`.
3. Runs Alembic migrations against the test DB.
4. Executes `pytest` and uploads test artifacts.

Recent fix: removed host port binding for the Postgres service to avoid port conflicts on hosted runners. If CI still fails:

- Check that `backend/requirements.txt` installs cleanly on Ubuntu (some packages may need `apt` packages like `libpq-dev`). Consider adding an `apt-get` step in CI before `pip install`.
- Confirm tests don't require long-running external services or authenticated APIs; if they do, mock them or provide test doubles.

**Deployment**

This project can be deployed with Docker or traditional VM/hosted services. A minimal `docker-compose` example (illustrative):

```yaml
version: '3.7'
services:
	db:
		image: postgres:14
		environment:
			POSTGRES_USER: postgres
			POSTGRES_PASSWORD: postgres
			POSTGRES_DB: career_recommendations
	backend:
		build: ./backend
		environment:
			DATABASE_URL: postgresql://postgres:postgres@db:5432/career_recommendations
		depends_on:
			- db
	frontend:
		build: ./frontend
		ports:
			- '3000:3000'
```

Production deployment considerations:

- Use a managed Postgres (RDS, Cloud SQL) with proper credentials and backups.
- Serve the backend behind a process manager (Gunicorn + Uvicorn workers or an ASGI server) and a reverse proxy (NGINX).
- Store model artifacts in a durable object store (S3) if models are large.

**Testing strategy**

- Unit tests: inside `backend/tests` — run with `pytest`.
- Integration tests: exercises DB migrations and endpoints; they expect a Postgres instance (CI provides one).
- ML tests: small smoke tests that load a model artifact and run inference on synthetic inputs — add these to CI if artifacts are small.

**Developer guides & common commands**

- Format Python: `black backend/` (if project uses Black).
- Linting: `flake8` or `pylint` depending on preference.
- Run alembic migrations: `alembic revision --autogenerate -m 'msg'` then `alembic upgrade head`.

**Troubleshooting (common failures & fixes)**

- CI fails at `pip install`:
	- Add system dependencies in CI (`apt-get update && apt-get install -y libpq-dev build-essential`) before `pip install`.
	- Pin versions in `backend/requirements.txt` to reproducible ones.
- Alembic / migrations fail:
	- Ensure `DATABASE_URL` points to the correct DB and credentials are valid.
	- Check `backend/alembic/env.py` for environment-specific overrides.
- Tests failing due to DB not ready:
	- Add a retry/wait step before running migrations; the CI service `options` health checks may not be sufficient for slow starts.

**Contributing**

- Fork and create feature branches.
- Run tests locally before opening a PR.
- Follow the code style used in existing files.

**Where to look in the codebase**

- Backend entry: `backend/app/main.py` and `backend/app/api/routers` for routes.
- DB migrations: `backend/alembic`.
- Model pipelines: `ml_personality_pipeline/` and `behavior_training/`.
- Tests: `backend/tests`.

If you'd like, I can now:

1. Run the CI steps locally and share failing logs. (recommended to validate fixes)
2. Harden CI (add apt packages and a DB wait loop). I can create that change and push it.
3. Expand documentation further with API endpoint examples and sample requests.

Tell me which of these you'd like next and I'll proceed.
