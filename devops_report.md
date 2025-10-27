# DevOps Report

## Technologies Used
- **FastAPI**: For building the REST API, chosen for its speed and auto-docs.
- **Celery**: Handles background tasks like fetching data, using Redis as broker.
- **Redis**: Acts as message broker for Celery and potential caching.
- **PostgreSQL**: Relational database for persistent storage.
- **Docker**: Containerizes the app for consistent environments across dev, test, prod.
- **Docker Compose**: Manages multi-container setups locally.
- **GitHub Actions**: For CI/CD, automating builds, tests, and deployments.
- **Pytest**: Testing framework with async support for API and Celery tasks.
- **Flake8 and Bandit**: For linting and security scans.

## Pipeline Design
The CI/CD pipeline is defined in `.github/workflows/ci-cd.yml` and runs on GitHub Actions.

- **Build Job**: Installs Python deps, runs on Ubuntu, ensures base setup.
- **Lint Job**: Depends on build, runs flake8 for code style.
- **Secuity Check**: uses bandit for security checks.
- **Test Job**: Depends on lint, starts Postgres and Redis as services, runs pytest with Celery worker in background.
- **Docker Job**: Depends on test, builds and tags Docker image.
- **Deploy Job**: Depends on docker, only on main branch, logs into Docker Hub and pushes images.

Diagram:
```
Push/PR -> Build -> Lint -> Secuity Check -> Test -> Docker -> Deploy (main only)
```

This ensures quality gates: no deployment without passing tests.

## Secret Management Strategy
Secrets are managed via GitHub Repository Secrets to avoid hardcoding sensitive data.

- Database URLs, Redis URLs, Celery broker URLs are stored as secrets.
- Docker Hub username and token for deployment.
- In workflow, accessed as `${{ secrets.SECRET_NAME }}`.

## Testing Process
- **Unit Tests**: Test individual functions in api/.
- **CI Execution**: Tests run with real Postgres and Redis containers, Celery worker started via nohup.
- **Coverage**: Focus on async flows, error handling.
- **Failure Handling**: Logs Celery output on test failure for debugging.
- Local testing: Run `pytest` after starting services with docker-compose.

## Lessons Learned
- Setting up services in CI was challenging but crucial for realistic tests.
- Secrets management prevents leaks but requires careful setup.
- Containerization simplifies deployment but adds complexity in local dev.
- Automation in CI/CD saves time but needs regular updates to avoid pipeline failures from outdated tools or dependencies.
- Version pinning in Dockerfiles and requirements.txt prevents unexpected breaks from library updates.
- Branch protection rules on GitHub enforce code reviews, reducing bugs in merges to main.
- Balancing security scans with build speed avoids slowing down the pipeline unnecessarily.
- Continuous improvement means iterating on the pipeline, like adding more test coverage or integrating monitoring tools
