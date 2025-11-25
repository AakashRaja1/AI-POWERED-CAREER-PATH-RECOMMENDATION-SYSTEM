FROM python:3.10-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first for better caching
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy backend code and model artifacts
COPY alembic alembic/
COPY alembic.ini .
COPY app app/
COPY model_artifacts model_artifacts/
COPY LatestCareerdataset.csv .

# Environment variables
ENV PYTHONPATH=/app
ENV MODEL_PATH=/app/model_artifacts

# Run migrations and start server
CMD ["sh", "-c", "alembic upgrade head && uvicorn app.main:app --host 0.0.0.0 --port 8000"]