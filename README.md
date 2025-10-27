# FastAPI DevOps Lab

This project is a REST API built with FastAPI, showcasing DevOps practices like containerization, CI/CD, and automated testing. It uses Celery for async tasks, Redis for messaging, and PostgreSQL for data storage.

## Architecture
- **API Layer**: FastAPI handles HTTP requests.
- **Background Tasks**: Celery processes tasks asynchronously.
- **Database**: PostgreSQL stores user and weather data.
- **Cache/Message Broker**: Redis for Celery and caching.
- **Containerization**: Docker for consistent environments.

## Project Structure
- `api/`: Source code (main.py, models.py, etc.)
- `tests/`: Unit and integration tests.
- `Dockerfile`: Builds the app container.
- `docker-compose.yml`: Local multi-container setup.
- `.github/workflows/ci-cd.yml`: GitHub Actions pipeline.

## Setup and Local Development
1. Clone the repository.
2. Ensure Docker and Docker Compose are installed.
3. Run `docker-compose up --build` to start services (API, DB, Redis, Celery).
4. API will be available at http://localhost:8000.

For development, mount volumes in docker-compose.yml to sync code changes.

## CI/CD Pipeline
- **Triggers**: Push/PR to dev/main branches.
- **Jobs**:
  - Build: Install deps.
  - Secuity: Checks for security issues using bandit.
  - Lint: Code quality checks.
  - Test: Run pytest with Postgres/Redis services.
  - Docker: Build and tag image.
  - Deploy: Push to Docker Hub on main branch only.
- View status at https://github.com/M-Fahim-Feroz/fastapi-devops-lab/actions.

## Deployment
- Images are pushed to Docker Hub on successful tests.
- For production, use the latest tag or SHA-tagged image.
- Secrets (DB creds, Docker Hub) are managed via GitHub Secrets.

## Usage
Endpoints for managing users and weather data via Celery tasks.

### Endpoints
| URL | Description | Method |
|-----|-------------|--------|
| /users/{count} | Queue adding random users | POST |
| /users/{user_id} | Fetch user | GET |
| /weathers/{city} | Queue weather fetch | POST |
| /weathers/{city} | Get weather | GET |
| /tasks/{task_id} | Task status | GET |

## Testing
- Local: `pytest api/tests/tests.py`
- CI: Automated with services, includes Celery worker.
- Coverage: Focus on integration tests for async flows.

## Monitoring and Logging
- Celery logs are captured in CI on failure.

