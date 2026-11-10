# Cargo Platform API

FastAPI + PostgreSQL негізіндегі карго платформасы.

## Іске қосу (Docker)

```bash
docker compose up --build
```

→ http://localhost:8000/docs (Swagger). Миграциялар контейнер іске қосылғанда өздігінен орындалады,
тексеру: `curl http://localhost:8000/health`.

## Docker-сіз

```bash
python -m venv .venv && source .venv/bin/activate
pip install -r requirements-dev.txt
cp .env.example .env          # DB_* және JWT_SECRET_KEY толтырыңыз
alembic upgrade head
uvicorn app.main:app --reload
pytest
```

## Qoldanba песочницасы

Бұл репо — Qoldanba шаблоны. Песочницада қолданба `Dockerfile` бойынша жиналады, дерекқор мен
айнымалыларды платформа береді (`qoldanba.yaml`), `main`-ге әр merge — жаңа деплой.
Талаптар мен CI: [TEMPLATE.md](TEMPLATE.md).
