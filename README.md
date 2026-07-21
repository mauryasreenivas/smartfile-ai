# SmartFile AI

AI-powered financial file ingestion, schema mapping, validation and transformation platform.

## Day 1 status

- [x] Production-style FastAPI structure
- [x] Environment-driven configuration
- [x] Health and root endpoints
- [x] Unit tests
- [x] Ruff linting and formatting
- [x] MyPy type checking
- [x] Pre-commit hooks
- [ ] File upload and inspection
- [ ] Header detection
- [ ] AI schema mapping
- [ ] Transformation and validation
- [ ] React frontend
- [ ] Deployment

## Requirements

- macOS, Linux or Windows
- Python 3.12
- uv

## Setup

```bash
uv sync --all-groups
cp .env.example .env
uv run uvicorn app.main:app --reload
```

Open:

- API: http://127.0.0.1:8000
- Swagger UI: http://127.0.0.1:8000/docs
- Health: http://127.0.0.1:8000/api/v1/health

## Quality checks

```bash
uv run ruff format .
uv run ruff check .
uv run mypy app
uv run pytest --cov=app --cov-report=term-missing
```

## Project structure

```text
smartfile-ai/
├── app/
│   ├── api/routes/
│   ├── core/
│   └── main.py
├── tests/
├── .env.example
├── .gitignore
├── .pre-commit-config.yaml
├── pyproject.toml
└── README.md
```

## Security

Only synthetic or publicly safe sample data should be committed. Never commit company files, customer information, credentials, internal mappings or proprietary code.
