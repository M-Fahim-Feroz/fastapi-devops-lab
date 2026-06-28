# Troubleshooting Guide — FastAPI DevSecOps Pipeline

## Docker Compose Issues

### API container crashes on startup

```bash
docker compose logs api
# Common cause: postgres not ready yet (health check timing)
docker compose down -v && docker compose up --build
```

### Database connection refused

Ensure the `DATABASE_URL` environment variable matches the service name in `docker-compose.yml`:

```
DATABASE_URL=postgresql://postgres:postgres@postgres:5432/fastapi_test
```

Note: use `postgres` (service name), not `localhost`.

### Celery worker not starting

```bash
docker compose logs worker
# Check CELERY_BROKER_URL is set to redis://redis:6379/0
```

### Port 81 already in use

```bash
# On Linux/Mac:
lsof -i :81
# Change the host port in docker-compose.yml if needed
```

## GitHub Actions Failures

### Trivy scan fails with HIGH/CRITICAL CVEs

Trivy is configured with `ignore-unfixed: true`. If it still fails:

```bash
# Run locally:
docker run --rm aquasec/trivy image --ignore-unfixed --severity HIGH,CRITICAL <image>:<tag>
```

Update base image in `Dockerfile` to a newer Python patch release.

### Tests fail — Celery connection error

The test job starts Celery in the background with a 5s sleep. If tests run before Celery is ready:

- Check if the Celery worker log shows errors (see `Show Celery logs on failure` step output).

### Docker Hub push fails

- Verify `DOCKERHUB_USERNAME` and `DOCKERHUB_TOKEN` secrets are set.
- Push only happens on `main` branch — PRs will skip the push step.

## Local Python Development

### flake8 errors

```bash
pip install flake8
flake8 api --max-line-length=120
```

### Bandit security warnings

```bash
pip install bandit
bandit -r api -lll --exclude api/tests/
```

Low-severity issues are allowed. Only HIGH/CRITICAL severity will fail.
