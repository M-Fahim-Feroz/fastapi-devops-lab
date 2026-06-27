Write-Host "Running FastAPI Preflight Checks..."
python -m compileall .
pytest -vv
flake8 .
bandit -r . -x ./.venv,./venv,./tests
docker build -t fastapi-devsecops-pipeline:test .

