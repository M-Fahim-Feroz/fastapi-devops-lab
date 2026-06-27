# GitHub Issues Backlog

Prepared issues for the fastapi-devsecops-pipeline repository.
Create at: https://github.com/M-Fahim-Feroz/fastapi-devsecops-pipeline/issues/new

---

## Issue 1

**Title:** [CI] Remove secrets from test service containers
**Labels:** `ci`, `security`
**Priority:** High

**Description:**
The CI test job uses `secrets.POSTGRES_USER`, `secrets.POSTGRES_PASSWORD`, and `secrets.DB` for PostgreSQL service containers. This prevents the test job from running on pull requests from forks (which don't have access to secrets). Use hardcoded local credentials (`postgres`/`postgres`/`fastapi_test`) for the CI test environment.

**Acceptance Criteria:**
- [ ] PostgreSQL service uses hardcoded `POSTGRES_USER=postgres`, `POSTGRES_PASSWORD=postgres`, `POSTGRES_DB=fastapi_test`
- [ ] `DATABASE_URL` env var uses hardcoded localhost values
- [ ] Tests pass without needing `POSTGRES_USER/PASSWORD/DB` secrets
- [ ] `WEATHER_API_KEY` uses a safe dummy value for tests

---

## Issue 2

**Title:** [Security] Pin Trivy GitHub Action to stable version
**Labels:** `security`, `ci`
**Priority:** High

**Description:**
`aquasecurity/trivy-action@master` is unpinned and uses a floating tag. This creates supply chain risk and unpredictable behavior. Pin to a specific version tag.

**Acceptance Criteria:**
- [ ] `aquasecurity/trivy-action` pinned to a stable version (e.g., `@0.28.0`)
- [ ] No `@master` usage remains in any workflow file

---

## Issue 3

**Title:** [Deps] Add Dependabot for automated dependency updates
**Labels:** `dependencies`
**Priority:** Medium

**Description:**
No Dependabot configuration exists. Add `.github/dependabot.yml` to automatically monitor pip, Docker, and GitHub Actions dependencies.

**Acceptance Criteria:**
- [ ] `.github/dependabot.yml` added
- [ ] pip updates enabled for requirements.txt
- [ ] Docker updates enabled for Dockerfile
- [ ] GitHub Actions updates enabled

---

## Issue 4

**Title:** [Testing] Add coverage reporting to CI
**Labels:** `testing`
**Priority:** Low

**Description:**
Add `pytest-cov` to generate a coverage summary in CI output.

**Acceptance Criteria:**
- [ ] `pytest-cov` added to test dependencies
- [ ] Coverage report visible in CI logs
- [ ] Coverage badge added to README (optional)

---

## Issue 5

**Title:** [Docs] Add API endpoint table to README
**Labels:** `documentation`
**Priority:** Low

**Description:**
The README does not document the available API endpoints. Add a table showing method, path, and description.

**Acceptance Criteria:**
- [ ] Table with at least: `GET /`, `POST /users/{id}`, `POST /weathers/{city}`, `GET /tasks/{task_id}`
- [ ] Swagger UI link confirmed working
