# FastAPI Dependencies & Error Handling Reference

## Basic Dependency

```python
from typing import Annotated
from fastapi import Depends, FastAPI

async def common_parameters(
    q: str | None = None,
    skip: int = 0,
    limit: int = 100
):
    return {"q": q, "skip": skip, "limit": limit}

# Type alias for reuse
CommonsDep = Annotated[dict, Depends(common_parameters)]

@app.get("/items/")
async def read_items(commons: CommonsDep):
    return commons

@app.get("/users/")
async def read_users(commons: CommonsDep):
    return commons
```

**CRITICAL:** Pass function reference — never call it:
```python
# ✅ Correct
Depends(common_parameters)

# ❌ Wrong
Depends(common_parameters())
```

## Class-Based Dependency (Better IDE Support)

```python
class CommonQueryParams:
    def __init__(self, q: str | None = None, skip: int = 0, limit: int = 100):
        self.q = q
        self.skip = skip
        self.limit = limit

@app.get("/items/")
async def read_items(
    commons: Annotated[CommonQueryParams, Depends(CommonQueryParams)]
):
    if commons.q:
        return filtered_items[commons.skip : commons.skip + commons.limit]
    return all_items[commons.skip : commons.skip + commons.limit]
```

## Sub-Dependencies (Hierarchical)

```python
def query_extractor(q: str | None = None):
    return q

def query_or_cookie_extractor(
    q: Annotated[str | None, Depends(query_extractor)],
    last_query: Annotated[str | None, Cookie()] = None,
):
    return q or last_query

@app.get("/items/")
async def read_items(
    query_or_default: Annotated[str | None, Depends(query_or_cookie_extractor)]
):
    return {"q_or_cookie": query_or_default}
```

## Yield Dependencies (DB Session, Cleanup)

```python
from sqlmodel import Session, create_engine

engine = create_engine("sqlite:///db.sqlite3")

def get_session():
    with Session(engine) as session:
        yield session          # ← request handled here
    # session auto-closed after yield block exits

SessionDep = Annotated[Session, Depends(get_session)]

@app.get("/items/")
def read_items(session: SessionDep):
    return session.exec(select(Item)).all()
```

## Router-Level Dependencies

```python
from fastapi import APIRouter, Depends, Header, HTTPException
from typing import Annotated

async def verify_token(x_token: Annotated[str, Header()]):
    if x_token != "secret-token":
        raise HTTPException(status_code=400, detail="Invalid token")

# All routes in this router require valid token
router = APIRouter(
    prefix="/items",
    tags=["items"],
    dependencies=[Depends(verify_token)],
)
```

## Global Dependencies

```python
# All routes in the entire app
app = FastAPI(dependencies=[Depends(verify_token), Depends(verify_key)])
```

## Dependency Override (Testing)

```python
def mock_settings():
    return Settings(admin_email="test@example.com")

app.dependency_overrides[get_settings] = mock_settings

# Reset
app.dependency_overrides = {}
```

---

## Error Handling

### HTTPException

```python
from fastapi import HTTPException

@app.get("/items/{item_id}")
async def read_item(item_id: str):
    if item_id not in items:
        raise HTTPException(           # ← always raise, never return
            status_code=404,
            detail="Item not found",   # any JSON-serializable value
        )
    return items[item_id]

# With custom headers
raise HTTPException(
    status_code=404,
    detail={"message": "Not found", "item_id": item_id},
    headers={"X-Error": "Item not found"},
)
```

### Custom Exception Handler

```python
from fastapi import Request
from fastapi.responses import JSONResponse

class PipelineError(Exception):
    def __init__(self, pipeline_id: str, reason: str):
        self.pipeline_id = pipeline_id
        self.reason = reason

@app.exception_handler(PipelineError)
async def pipeline_error_handler(request: Request, exc: PipelineError):
    return JSONResponse(
        status_code=500,
        content={
            "pipeline_id": exc.pipeline_id,
            "error": exc.reason,
            "docs": "/docs#pipeline-errors",
        },
    )

# Usage
@app.post("/pipeline/{pipeline_id}/run")
async def run_pipeline(pipeline_id: str):
    if not pipeline_exists(pipeline_id):
        raise PipelineError(pipeline_id, "Pipeline not found")
```

### Override Validation Error Format

```python
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    return JSONResponse(
        status_code=422,
        content=jsonable_encoder({
            "detail": exc.errors(),
            "body": exc.body,
            "message": "Validation failed — check your request",
        }),
    )
```

### Override HTTP Exception Handler

```python
from starlette.exceptions import HTTPException as StarletteHTTPException
from fastapi.responses import PlainTextResponse

@app.exception_handler(StarletteHTTPException)
async def http_exception_handler(request, exc):
    return PlainTextResponse(str(exc.detail), status_code=exc.status_code)
```

---

## Background Tasks

```python
from fastapi import BackgroundTasks

def send_email_notification(email: str, message: str):
    # Runs after response is returned
    with open("log.txt", mode="a") as f:
        f.write(f"Email to {email}: {message}\n")

@app.post("/pipeline/{pipeline_id}/trigger")
async def trigger_pipeline(
    pipeline_id: str,
    background_tasks: BackgroundTasks,
):
    background_tasks.add_task(send_email_notification, "admin@example.com", f"Pipeline {pipeline_id} triggered")
    background_tasks.add_task(run_pipeline_job, pipeline_id)
    return {"status": "triggered", "pipeline_id": pipeline_id}
```

**Use Celery instead when:**
- Tasks are CPU-heavy or long-running
- Need distributed across multiple servers
- Require retry logic, scheduling, or queuing (RabbitMQ/Redis)
