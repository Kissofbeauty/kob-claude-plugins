# FastAPI Advanced Reference — WebSockets, Lifespan, Settings, Middleware

## Lifespan Events (Startup / Shutdown)

```python
from contextlib import asynccontextmanager
from fastapi import FastAPI
import joblib

ml_models = {}
db_pool = None

@asynccontextmanager
async def lifespan(app: FastAPI):
    # ─── STARTUP ───────────────────────────────────────────
    # Load ML model once (not per request)
    ml_models["churn_model"] = joblib.load("models/churn.pkl")
    ml_models["price_model"] = joblib.load("models/price.pkl")

    # Initialize DB connection pool
    app.state.db = await create_async_engine(settings.database_url)

    print("✅ Models loaded, DB connected")
    yield
    # ─── SHUTDOWN ──────────────────────────────────────────
    ml_models.clear()
    await app.state.db.dispose()
    print("🛑 Cleanup complete")

app = FastAPI(lifespan=lifespan)

# Access loaded model in endpoint
@app.post("/predict/churn")
async def predict_churn(features: ChurnFeatures):
    model = ml_models["churn_model"]
    prediction = model.predict([features.to_array()])
    return {"churn_probability": float(prediction[0])}
```

**Rules:**
- Use `lifespan` — NOT deprecated `@app.on_event()`
- Do NOT mix both in the same app
- Only fires on the main app, not mounted sub-apps

---

## Settings with Pydantic BaseSettings

```python
# config.py
from functools import lru_cache
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    # Required (no default) — must be in env or .env file
    database_url: str
    secret_key: str
    aws_access_key_id: str
    aws_secret_access_key: str

    # Optional with defaults
    app_name: str = "Pipeline API"
    debug: bool = False
    max_workers: int = 4
    allowed_origins: list[str] = ["http://localhost:3000"]
    items_per_page: int = 100

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,  # APP_NAME and app_name both work
    )

@lru_cache  # reads .env only ONCE — cached for all requests
def get_settings() -> Settings:
    return Settings()
```

**.env file:**
```env
DATABASE_URL=postgresql://user:pass@localhost/mydb
SECRET_KEY=super-secret-key-change-me
AWS_ACCESS_KEY_ID=AKIAXXXXXXXX
AWS_SECRET_ACCESS_KEY=XXXXXXXXXX
DEBUG=false
MAX_WORKERS=4
```

```python
# main.py
from typing import Annotated
from fastapi import Depends
from .config import get_settings, Settings

SettingsDep = Annotated[Settings, Depends(get_settings)]

@app.get("/info")
async def info(settings: SettingsDep):
    return {
        "app": settings.app_name,
        "debug": settings.debug,
    }
```

---

## Middleware

```python
import time
from fastapi import Request

# Timing middleware
@app.middleware("http")
async def add_timing_header(request: Request, call_next):
    start = time.perf_counter()                     # ← perf_counter, not time()
    response = await call_next(request)
    duration = time.perf_counter() - start
    response.headers["X-Process-Time"] = str(duration)
    response.headers["X-Request-ID"] = str(uuid4())
    return response

# Logging middleware
@app.middleware("http")
async def log_requests(request: Request, call_next):
    print(f"→ {request.method} {request.url}")
    response = await call_next(request)
    print(f"← {response.status_code}")
    return response
```

**Middleware stacking:** Last added = outermost (runs first on request, last on response)

## CORS

```python
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "https://myapp.com"],
    allow_credentials=True,     # ← If True, cannot use "*" for origins/methods/headers
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["X-Process-Time"],   # headers visible to browser
    max_age=600,
)
```

**Rule:** `allow_credentials=True` + `"*"` = broken. Must specify explicit origins.

## Trusted Host Middleware

```python
from fastapi.middleware.trustedhost import TrustedHostMiddleware

app.add_middleware(
    TrustedHostMiddleware,
    allowed_hosts=["example.com", "*.example.com", "localhost"]
)
```

---

## WebSockets

```python
# pip install websockets
from fastapi import WebSocket, WebSocketDisconnect

@app.websocket("/ws/{client_id}")
async def websocket_endpoint(websocket: WebSocket, client_id: str):
    await websocket.accept()
    try:
        while True:
            data = await websocket.receive_text()
            await websocket.send_text(f"Echo: {data}")
    except WebSocketDisconnect:
        print(f"Client {client_id} disconnected")
```

### Connection Manager (Multi-Client)

```python
class ConnectionManager:
    def __init__(self):
        self.active: list[WebSocket] = []

    async def connect(self, ws: WebSocket):
        await ws.accept()
        self.active.append(ws)

    def disconnect(self, ws: WebSocket):
        self.active.remove(ws)

    async def broadcast(self, message: str):
        for ws in self.active:
            await ws.send_text(message)

    async def send_to(self, message: str, ws: WebSocket):
        await ws.send_text(message)

manager = ConnectionManager()

@app.websocket("/pipeline/{pipeline_id}/status")
async def pipeline_status(websocket: WebSocket, pipeline_id: str):
    await manager.connect(websocket)
    try:
        while True:
            status = await get_pipeline_status(pipeline_id)
            await websocket.send_json({"pipeline_id": pipeline_id, "status": status})
            await asyncio.sleep(2)   # poll every 2 seconds
    except WebSocketDisconnect:
        manager.disconnect(websocket)
```

**Production (multi-process):** In-memory list fails with multiple workers. Use Redis pub/sub:

```python
import redis.asyncio as redis

redis_client = redis.from_url(settings.redis_url)

async def ws_pipeline_status(websocket: WebSocket, pipeline_id: str):
    await websocket.accept()
    pubsub = redis_client.pubsub()
    await pubsub.subscribe(f"pipeline:{pipeline_id}")
    try:
        async for message in pubsub.listen():
            if message["type"] == "message":
                await websocket.send_text(message["data"])
    except WebSocketDisconnect:
        await pubsub.unsubscribe(f"pipeline:{pipeline_id}")
```

---

## Custom Responses

```python
from fastapi.responses import (
    HTMLResponse, PlainTextResponse, RedirectResponse,
    StreamingResponse, FileResponse, JSONResponse, Response
)

# HTML
@app.get("/report", response_class=HTMLResponse)
async def report():
    return "<html><body><h1>Report</h1></body></html>"

# Streaming (large data)
async def generate_csv():
    yield "id,name,value\n"
    async for row in fetch_data_from_db():
        yield f"{row.id},{row.name},{row.value}\n"
        await anyio.sleep(0)   # ← required for proper async cancellation

@app.get("/export/csv")
async def export_csv():
    return StreamingResponse(
        generate_csv(),
        media_type="text/csv",
        headers={"Content-Disposition": "attachment; filename=data.csv"}
    )

# File download
@app.get("/download/{filename}")
async def download_file(filename: str):
    return FileResponse(
        f"data/{filename}",
        media_type="application/octet-stream",
        filename=filename,  # sets Content-Disposition
    )

# Redirect
@app.get("/old-path")
async def redirect():
    return RedirectResponse(url="/new-path", status_code=301)
```

---

## Static Files

```python
from fastapi.staticfiles import StaticFiles

# Mount a directory (not in OpenAPI schema)
app.mount("/static", StaticFiles(directory="static"), name="static")
app.mount("/reports", StaticFiles(directory="output/reports"), name="reports")
```

---

## Testing

```python
# pip install httpx pytest
from fastapi.testclient import TestClient
from .main import app, get_settings
from .config import Settings

client = TestClient(app)

# Override settings for tests
def override_settings():
    return Settings(database_url="sqlite:///test.db", debug=True)

app.dependency_overrides[get_settings] = override_settings

def test_read_root():
    res = client.get("/")
    assert res.status_code == 200

def test_create_item():
    res = client.post("/items/", json={"name": "test", "price": 10.0})
    assert res.status_code == 201
    assert res.json()["name"] == "test"

def test_with_auth():
    res = client.get("/protected", headers={"X-Token": "valid-token"})
    assert res.status_code == 200

def test_with_cookie():
    res = client.get("/items/", cookies={"session": "abc123"})
    assert res.status_code == 200
```

**Rules:**
- Test functions: `def` not `async def`
- Function name must start with `test_`
- Run: `pytest` or `pytest -v`
