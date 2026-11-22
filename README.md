\# Mini-VulnFinBot — Secure CI/CD Pipeline



\## Project Description

Mini-VulnFinBot is a Flask-based financial assistant API (`GET /health` and `POST /api/chat`) built with input validation, error handling, AI-specific security tests, containerization via Docker, and an automated GitHub Actions security pipeline.



\## Technologies Used

\* Python 3.12 and Flask

\* pytest

\* Git and GitHub Actions

\* Bandit and Semgrep (SAST)

\* pip-audit (dependency scanning)

\* Docker and Trivy (container security scanning)

\* OWASP ZAP (DAST baseline scan)



\## Project Structure

\* `app/` — Flask application factory (`\_\_init\_\_.py`) and API endpoints (`routes.py`)

\* `tests/` — Unit tests (`test\_app.py`) and AI security tests (`test\_ai\_security.py`)

\* `security/semgrep/rules.yml` — Custom Semgrep static analysis rules\[cite: 1]

\* `reports/` — Security reports (`ai-security-report.md` and scanner artifacts)\[cite: 1]

\* `.github/workflows/security-pipeline.yml` — Automated CI/CD security workflow\[cite: 1]

\* `Dockerfile`, `run.py`, `requirements.txt` — Container and runtime configuration\[cite: 1]



\## Setup and Running Locally

1\. Create and activate virtual environment:

&#x20;  ```bash

&#x20;  python -m venv venv

&#x20;  venv\\Scripts\\activate

