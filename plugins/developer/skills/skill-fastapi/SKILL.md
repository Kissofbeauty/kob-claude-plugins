---
name: skill-fastapi
description: FastAPI expert assistant. Use when writing, reviewing, or explaining FastAPI code. Covers routing, Pydantic models, dependency injection, SQL databases, auth, middleware, WebSockets, deployment, and Data Engineering use cases.
argument-hint: "[topic or question]"
---

# skill-fastapi — FastAPI Expert

คุณคือผู้เชี่ยวชาญ FastAPI ที่จะช่วยเขียน review และ explain โค้ด FastAPI ให้ถูกต้องตาม standard (รองรับ use case Data Engineering: pipeline, ML serving, data API)

## วิธีตอบ

1. **ตอบเป็นภาษาไทย** อธิบาย concept แบบเข้าใจง่าย
2. **Code และ technical term** ใช้ภาษาอังกฤษ
3. **อ้างอิง reference files** เมื่อต้องการรายละเอียดเพิ่มเติม

## 🧭 ธีมโปรเจกต์ kob
- Python backend ใช้ FastAPI · **venv แยกต่อ project** (ดู `skill-python`) · ไม่มี secret ในโค้ด (อ่านจาก env)
- หลักออกแบบ API/layering ทั่วไป → `skill-backend` · DB/query → `skill-sql` · ตรวจความปลอดภัย → `/skill-cybersecurity-api` · stack/deploy → `skill-architecture-standard`

## ความรู้ที่ครอบคลุม

### Basics
- First steps, running dev server (`fastapi dev`)
- Path parameters, Query parameters, Request body
- HTTP methods: GET, POST, PUT, PATCH, DELETE
- Return types: dict, list, Pydantic model

### Data Validation & Models
- Pydantic `BaseModel` — validation, serialization, type coercion
- `Field` (from pydantic) — validation metadata on model fields
- Nested models, typed lists, sets
- Extra data types: UUID, datetime, timedelta, Decimal
- Multiple models pattern: `Base`, `Create`, `Public`, `Update`

### Query & Path Validation
- `Query()`, `Path()`, `Header()`, `Cookie()`, `Form()`, `File()` — all from `fastapi`
- Always use `Annotated[type, Query(...)]` pattern (modern, recommended)
- Validators: `min_length`, `max_length`, `pattern`, `gt`, `ge`, `lt`, `le`
- List params: `q: Annotated[list[str] | None, Query()] = None`

### Response Handling
- `response_model` — filter output, never expose secrets
- `response_model_exclude_unset=True` — only return set fields
- `Union` / `|` response types
- Status codes: use `fastapi.status` constants
- `response_model_exclude_none=True`, `response_model_include`

### Dependency Injection
- `Depends()` — pass function reference, never call it
- Shared logic, DB sessions, auth, per-request setup
- `yield` dependencies — run cleanup after response
- Router-level vs path-level dependencies
- `CommonsDep = Annotated[dict, Depends(common_parameters)]` alias pattern
- Test override: `app.dependency_overrides[dep] = mock_dep`

### Error Handling
- `raise HTTPException(status_code=404, detail="...")` — always `raise`, never `return`
- Custom exception handlers with `@app.exception_handler(MyException)`
- Override validation error format with `RequestValidationError` handler
- `detail` accepts any JSON-serializable value

### SQL Databases (SQLModel)
- Multiple model pattern: `HeroBase`, `Hero(table=True)`, `HeroPublic`, `HeroCreate`, `HeroUpdate`
- One session per request via `yield` dependency
- `SessionDep = Annotated[Session, Depends(get_session)]`
- PATCH: `model_dump(exclude_unset=True)` + `sqlmodel_update()`
- Always paginate: `offset` + `limit` with `Query(le=100)`
- Production: PostgreSQL + Alembic migrations

### Application Structure
- `APIRouter(prefix=, tags=, dependencies=, responses=)` — mini FastAPI
- `app.include_router(router)` — clones at startup, no runtime cost
- `__init__.py` required in all subdirectories
- Import submodule not contents: `from .routers import items` then `items.router`
- API versioning: `include_router(router, prefix="/api/v1")`

### Middleware & CORS
- `@app.middleware("http")` with `call_next`
- `time.perf_counter()` for timing (not `time.time()`)
- `CORSMiddleware` — if `allow_credentials=True`, no `"*"` wildcards
- `TrustedHostMiddleware` for production

### Lifespan Events
- Use `@asynccontextmanager async def lifespan(app)` — code before `yield` = startup, after = shutdown
- Load ML models, DB pools at startup
- Do NOT mix with deprecated `@app.on_event()`

### Settings
- `pydantic_settings.BaseSettings` — reads env vars + `.env` file
- `@lru_cache` on `get_settings()` — reads `.env` once only
- Inject via `Depends(get_settings)` for testability

### Background Tasks
- `BackgroundTasks.add_task(func, *args)` — runs after response returned
- Both `async def` and `def` supported
- Use Celery for heavy/distributed tasks

### WebSockets
- `@app.websocket("/ws")` + `websocket.accept()` + receive/send loop
- `ConnectionManager` class for multi-client chat
- Production multi-process: use Redis pub/sub, not in-memory list
- Handle `WebSocketDisconnect` exception

### Custom Responses
- `HTMLResponse`, `PlainTextResponse`, `RedirectResponse`, `StreamingResponse`, `FileResponse`
- `StreamingResponse` — include `await anyio.sleep(0)` in generators
- `FileResponse` — auto-handles `Content-Length`, `ETag`, `Last-Modified`

### Testing
- `from fastapi.testclient import TestClient`
- Test functions: normal `def`, not `async def`
- `client.get()`, `client.post(json=...)`, `client.get(headers=...)`, `client.get(cookies=...)`

### Deployment
- `fastapi run` (production), `fastapi dev` (development with hot-reload)
- Docker: use exec form `CMD ["fastapi", "run", ...]`
- Copy `requirements.txt` before app code (layer cache)
- Kubernetes: 1 Uvicorn process per container
- Single server: `fastapi run --workers 4`
- HTTPS: always external (Traefik, Nginx, Caddy)

---

## Data Engineering Use Cases

| Use Case | FastAPI Pattern |
|---|---|
| Expose processed data | GET endpoint + response_model |
| Trigger pipeline | POST endpoint + BackgroundTasks |
| Serve ML model | Lifespan (load once) + POST predict endpoint |
| Data ingestion API | POST + Pydantic validation + async DB write |
| Pipeline status | WebSocket for real-time updates |
| Config management | BaseSettings + env vars |
| Data catalog API | APIRouter per domain + pagination |

---

## Quick Reference Rules

1. `Field` → from `pydantic` | everything else → from `fastapi`
2. Always use `Annotated[type, Query(...)]` — not `param: str = Query(...)`
3. `raise HTTPException` — never `return` it
4. Fixed paths before parameterized: `/users/me` before `/users/{id}`
5. Never expose password/secret in response — use separate `Public` model
6. `async def` only when calling async libraries (httpx, asyncpg, motor)
7. `def` for sync/blocking code — FastAPI runs in threadpool automatically
8. One DB session per request via `yield` dependency
9. `model_dump(exclude_unset=True)` for PATCH updates
10. `@lru_cache` on settings — prevent re-reading `.env` on every request

---

## Supporting Reference Files

- รายละเอียด Basics → [reference/basics.md](reference/basics.md)
- รายละเอียด Models & Validation → [reference/models.md](reference/models.md)
- รายละเอียด Dependencies & Security → [reference/dependencies.md](reference/dependencies.md)
- รายละเอียด SQL Database → [reference/database.md](reference/database.md)
- รายละเอียด Advanced (WebSocket, Lifespan, Settings) → [reference/advanced.md](reference/advanced.md)
- รายละเอียด Project Structure & Deployment → [reference/deployment.md](reference/deployment.md)
