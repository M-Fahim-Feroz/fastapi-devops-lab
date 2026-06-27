# Security Policy

## Supported Versions

This is a portfolio demonstration project.

| Version | Supported |
|---------|----------|
| main    | ✅ Yes (latest) |

## Reporting a Vulnerability

If you discover a security issue:

1. Do not open a public GitHub issue.
2. Contact the repository owner via GitHub: [M-Fahim-Feroz](https://github.com/M-Fahim-Feroz)
3. Describe the issue, steps to reproduce, and potential impact.

I will respond within 48 hours.

## Security Practices in This Project

- **Bandit** — Python SAST scanning runs on every CI push.
- **Trivy** — Container vulnerability scanning blocks pushes on HIGH/CRITICAL findings.
- **Non-root Docker user** — Application runs as `appuser`, not root.
- **Multi-stage Dockerfile** — Minimizes runtime image footprint.
- **No secrets committed** — `.env` is gitignored; `.env.example` contains only placeholder values.
- **Hardened dependencies** — `setuptools` and `wheel` are pinned to patched versions.

## Known Limitations

- This project is a portfolio demo. It is not deployed in a production environment.
- No automatic dependency update bot is configured (Dependabot recommended — see `.github/dependabot.yml`).
