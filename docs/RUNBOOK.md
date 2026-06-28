# Runbook — FastAPI DevSecOps Pipeline

## Start Local Stack

```bash
docker compose up --build
# API: http://localhost:81
# Docs: http://localhost:81/docs
```

## Run Tests

```bash
pip install -r requirements.txt pytest pytest-asyncio psycopg2-binary
DATABASE_URL=postgresql://postgres:postgres@localhost:5432/fastapi_test \
REDIS_URL=redis://localhost:6379/0 \
WEATHER_API_KEY=test-key \
pytest api/tests/tests.py -v
```

## Run Linting

```bash
flake8 api --max-line-length=120
bandit -r api -lll --exclude api/tests/
```

## Run Trivy Scan

```bash
docker build -t fastapi-devsecops-pipeline:local .
docker run --rm aquasec/trivy image --ignore-unfixed --severity HIGH,CRITICAL fastapi-devsecops-pipeline:local
```

## Trigger CI/CD

```bash
git push origin main  # builds, tests, scans, and pushes to Docker Hub
git push origin feature-branch  # builds and scans only — no push
```

## Stop and Clean Up

```bash
docker compose down -v     # stop and remove volumes
docker system prune -f     # clean dangling images
```
