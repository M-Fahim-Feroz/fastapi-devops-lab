# Contributing

This is a personal portfolio project. Contributions are welcome as learning collaborations.

## How to Contribute

1. Fork the repository.
2. Create a feature branch: `git checkout -b feature/your-improvement`
3. Make changes following the guidelines below.
4. Open a Pull Request against `main`.

## Local Development

```bash
cp .env.example .env
# Edit .env with local values
docker compose up --build -d
```

## Coding Standards

- Python: PEP8, max line length 120, enforced by flake8.
- Run `bandit -r api -lll` before submitting.
- Run `pytest api/tests/tests.py -v` before submitting.
- No secrets, `.env`, or `*.pyc` files committed.

## Pull Request Checklist

- [ ] `flake8 api/` passes
- [ ] `bandit -r api/ -lll` passes
- [ ] `pytest api/tests/` passes
- [ ] No secrets committed
- [ ] Documentation updated if needed
