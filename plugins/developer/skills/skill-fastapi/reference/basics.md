# FastAPI Basics Reference

## Minimal App

```python
from fastapi import FastAPI

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Hello World"}
```

```bash
fastapi dev           # development (hot-reload)
fastapi dev main.py   # specify file
fastapi run           # production
fastapi run --workers 4  # production multi-worker
```

## Path Parameters

```python
# Basic
@app.get("/items/{item_id}")
async def read_item(item_id: int):
    return {"item_id": item_id}

# Enum (predefined values)
from enum import Enum

class ModelName(str, Enum):
    alexnet = "alexnet"
    resnet = "resnet"

@app.get("/models/{model_name}")
async def get_model(model_name: ModelName):
    return {"model_name": model_name}

# Path containing slashes
@app.get("/files/{file_path:path}")
async def read_file(file_path: str):
    return {"file_path": file_path}
```

**CRITICAL:** Fixed paths must come BEFORE parameterized paths:
```python
@app.get("/users/me")        # ✅ First
@app.get("/users/{user_id}") # ✅ Second
```

## Query Parameters

```python
# Optional with default
@app.get("/items/")
async def read_items(skip: int = 0, limit: int = 10):
    return fake_db[skip : skip + limit]

# Optional (None)
async def read_item(item_id: str, q: str | None = None):
    ...

# Required (no default)
async def read_user_item(item_id: str, needy: str):
    ...

# Bool (accepts: 1, true, True, on, yes)
async def read_item(short: bool = False):
    ...
```

## Request Body

```python
from pydantic import BaseModel

class Item(BaseModel):
    name: str               # required
    description: str | None = None  # optional
    price: float            # required
    tax: float | None = None

@app.post("/items/")
async def create_item(item: Item):
    item_dict = item.model_dump()
    if item.tax:
        item_dict["price_with_tax"] = item.price + item.tax
    return item_dict

# Combined path + body + query
@app.put("/items/{item_id}")
async def update_item(item_id: int, item: Item, q: str | None = None):
    return {"item_id": item_id, **item.model_dump()}
```

**Parameter recognition:**
- Declared in path → path parameter
- Singular type (int, str) → query parameter
- Pydantic model → request body

## Cookie & Header Parameters

```python
from typing import Annotated
from fastapi import Cookie, Header

# Cookie
@app.get("/items/")
async def read_items(ads_id: Annotated[str | None, Cookie()] = None):
    return {"ads_id": ads_id}

# Header (underscore auto-converts to hyphen)
@app.get("/items/")
async def read_items(user_agent: Annotated[str | None, Header()] = None):
    return {"User-Agent": user_agent}

# Duplicate headers as list
async def read_items(x_token: Annotated[list[str] | None, Header()] = None):
    return {"X-Token values": x_token}
```

## HTTP Status Codes

```python
from fastapi import status

@app.post("/items/", status_code=status.HTTP_201_CREATED)
@app.delete("/items/{id}", status_code=status.HTTP_204_NO_CONTENT)
```

| Code | Constant | Use |
|------|----------|-----|
| 200 | `HTTP_200_OK` | Default success |
| 201 | `HTTP_201_CREATED` | Resource created |
| 204 | `HTTP_204_NO_CONTENT` | Success, no body |
| 400 | `HTTP_400_BAD_REQUEST` | Client error |
| 404 | `HTTP_404_NOT_FOUND` | Not found |
| 422 | `HTTP_422_UNPROCESSABLE_ENTITY` | Validation (auto) |

## Path Operation Configuration

```python
@app.post(
    "/items/",
    status_code=status.HTTP_201_CREATED,
    tags=["items"],
    summary="Create an item",
    response_description="The created item",
    deprecated=False,
)
async def create_item(item: Item) -> Item:
    """
    Create an item — docstring supports **Markdown**.
    - **name**: required
    - **price**: must be > 0
    """
    return item
```

## Forms & Files

```python
# pip install python-multipart
from typing import Annotated
from fastapi import Form, File, UploadFile

# Form fields
@app.post("/login/")
async def login(
    username: Annotated[str, Form()],
    password: Annotated[str, Form()]  # allowlist secret
):
    return {"username": username}

# File upload (UploadFile = recommended for production)
@app.post("/upload/")
async def upload(file: UploadFile):
    contents = await file.read()
    return {"filename": file.filename, "size": len(contents)}

# Multiple files
@app.post("/uploads/")
async def upload_many(files: list[UploadFile]):
    return [f.filename for f in files]
```

**Cannot mix** `Form`/`File` with JSON body in the same endpoint.
