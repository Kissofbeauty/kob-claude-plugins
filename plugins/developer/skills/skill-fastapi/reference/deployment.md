# FastAPI Project Structure & Deployment Reference

## Recommended Project Structure

```
project/
├── app/
│   ├── __init__.py
│   ├── main.py              # FastAPI app + lifespan + include_router
│   ├── config.py            # Pydantic BaseSettings
│   ├── dependencies.py      # Shared Depends functions
│   ├── models/
│   │   ├── __init__.py
│   │   ├── pipeline.py      # PipelineBase, PipelineCreate, PipelinePublic
│   │   └── user.py
│   ├── routers/
│   │   ├── __init__.py
│   │   ├── pipelines.py     # APIRouter for /pipelines
│   │   ├── runs.py          # APIRouter for /runs
│   │   └── users.py
│   ├── services/
│   │   ├── __init__.py
│   │   └── pipeline_service.py  # Business logic (pure functions)
│   └── db/
│       ├── __init__.py
│       └── session.py       # engine + get_session + SessionDep
├── tests/
│   ├── __init__.py
│   └── test_pipelines.py
├── .env
├── .env.example             # ← commit this (no secrets)
├── .gitignore               # ← include .env
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
└── pyproject.toml
```

## APIRouter Pattern

```python
# app/routers/pipelines.py
from fastapi import APIRouter, Depends, HTTPException
from typing import Annotated
from ..dependencies import verify_token
from ..db.session import SessionDep
from ..models.pipeline import PipelineCreate, PipelinePublic, PipelineUpdate, Pipeline

router = APIRouter(
    prefix="/pipelines",
    tags=["pipelines"],
    dependencies=[Depends(verify_token)],          # all routes require auth
    responses={404: {"description": "Not found"}},
)

@router.get("/", response_model=list[PipelinePublic])
def list_pipelines(session: SessionDep): ...

@router.post("/", response_model=PipelinePublic, status_code=201)
def create_pipeline(pipeline: PipelineCreate, session: SessionDep): ...

@router.get("/{pipeline_id}", response_model=PipelinePublic)
def get_pipeline(pipeline_id: int, session: SessionDep): ...

@router.patch("/{pipeline_id}", response_model=PipelinePublic)
def update_pipeline(pipeline_id: int, pipeline: PipelineUpdate, session: SessionDep): ...

@router.delete("/{pipeline_id}", status_code=204)
def delete_pipeline(pipeline_id: int, session: SessionDep): ...
```

```python
# app/main.py
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .config import get_settings
from .routers import pipelines, runs, users   # import submodule not router

settings = get_settings()

@asynccontextmanager
async def lifespan(app: FastAPI):
    from .db.session import create_db_and_tables
    create_db_and_tables()
    yield

app = FastAPI(
    title="Pipeline API",
    version="1.0.0",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(pipelines.router)    # ← use submodule.router
app.include_router(runs.router)
app.include_router(users.router)

# API versioning
# app.include_router(pipelines.router, prefix="/api/v1")
```

## Dependency Execution Order

```
Global deps (FastAPI(dependencies=[...]))
    └── Router deps (APIRouter(dependencies=[...]))
            └── Path deps (@router.get(..., dependencies=[...]))
                    └── Function parameter deps (Depends(...))
```

---

## Docker Deployment

### Dockerfile

```dockerfile
FROM python:3.12-slim

WORKDIR /code

# Copy requirements FIRST (cache layer)
COPY ./requirements.txt /code/requirements.txt
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

# Then copy app code
COPY ./app /code/app

# ✅ exec form — enables graceful shutdown and proper lifespan events
CMD ["fastapi", "run", "app/main.py", "--port", "80"]
```

**Behind a proxy (nginx, traefik):**
```dockerfile
CMD ["fastapi", "run", "app/main.py", "--port", "80", "--proxy-headers"]
```

**Multiple workers (single server):**
```dockerfile
CMD ["fastapi", "run", "app/main.py", "--port", "80", "--workers", "4"]
```

```bash
docker build -t pipeline-api .
docker run -d -p 80:80 --env-file .env pipeline-api
```

### docker-compose.yml

```yaml
version: "3.9"
services:
  api:
    build: .
    ports:
      - "80:80"
    env_file:
      - .env
    depends_on:
      - db
    restart: unless-stopped

  db:
    image: postgres:16
    environment:
      POSTGRES_USER: ${DB_USER}
      POSTGRES_PASSWORD: ${DB_PASSWORD}
      POSTGRES_DB: ${DB_NAME}
    volumes:
      - postgres_data:/var/lib/postgresql/data
    restart: unless-stopped

volumes:
  postgres_data:
```

---

## Uvicorn Configuration

```bash
# Development
fastapi dev app/main.py

# Production — single process
fastapi run app/main.py --port 8080

# Production — multiple workers
fastapi run app/main.py --workers 4 --port 8080

# Or directly with uvicorn
uvicorn app.main:app --host 0.0.0.0 --port 8080 --workers 4

# For debugging
python -m uvicorn app.main:app --reload --log-level debug
```

## Memory Planning

| Workers | Model Size | RAM Needed |
|---------|-----------|------------|
| 4 | 1 GB ML model | ~4 GB |
| 2 | 2 GB ML model | ~4 GB |

Each worker loads all resources independently — no shared memory.

---

## API Metadata

```python
from fastapi import FastAPI

app = FastAPI(
    title="Pipeline Orchestration API",
    description="""
## Pipeline API

Manage data pipelines, trigger runs, and monitor status.

### Features
- **Pipelines** — create and manage ETL pipelines
- **Runs** — trigger and monitor pipeline executions
- **WebSockets** — real-time run status updates
    """,
    version="1.0.0",
    contact={"name": "Data Team", "email": "data@company.com"},
    license_info={"name": "MIT"},
    openapi_tags=[
        {"name": "pipelines", "description": "Pipeline management"},
        {"name": "runs", "description": "Pipeline run management"},
        {"name": "users", "description": "User management"},
    ],
    # Custom docs URLs
    docs_url="/api/docs",
    redoc_url="/api/redoc",
    openapi_url="/api/openapi.json",
)
```

---

## Key Don'ts (Production Checklist)

| ❌ Don't | ✅ Do instead |
|---|---|
| Use `tiangolo/uvicorn-gunicorn-fastapi` image | Use official `python:3.12-slim` + `fastapi run` |
| Mix `lifespan` + `@app.on_event()` | Use `lifespan` only |
| Shell form CMD: `CMD fastapi run ...` | Exec form: `CMD ["fastapi", "run", ...]` |
| Share in-memory WebSocket list across workers | Use Redis pub/sub |
| Use `global` for shared state | Use `app.state` or dependency injection |
| Hardcode secrets in code | Use env vars + `.env` + `BaseSettings` |
| Commit `.env` to git | Add `.env` to `.gitignore`, commit `.env.example` |
| Use SQLite in production | Use PostgreSQL + hand-written SQL migrations (team standard — `skill-data-modeling` / `skill-sql` · not Alembic) |
| `async def` with sync blocking calls | Use regular `def` (FastAPI runs in threadpool) |
| `def` with async libraries (httpx, asyncpg) | Use `async def` |
