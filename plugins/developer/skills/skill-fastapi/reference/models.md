# FastAPI Models & Validation Reference

## Pydantic BaseModel

```python
from pydantic import BaseModel, Field
from datetime import datetime
from uuid import UUID

class Item(BaseModel):
    id: UUID
    name: str
    description: str | None = None
    price: float
    tax: float | None = None
    tags: set[str] = set()        # unique values
    created_at: datetime
```

## Field Validation (from pydantic)

```python
from pydantic import BaseModel, Field

class Item(BaseModel):
    name: str
    description: str | None = Field(
        default=None,
        title="Item description",
        max_length=300
    )
    price: float = Field(gt=0, description="Must be > 0")
    quantity: int = Field(ge=0, le=1000)
```

**Field validators:** `gt`, `ge`, `lt`, `le`, `min_length`, `max_length`, `pattern`

## Query & Path Validation (from fastapi)

```python
from typing import Annotated
from fastapi import Query, Path

# Query — always use Annotated pattern
@app.get("/items/")
async def read_items(
    q: Annotated[str | None, Query(
        min_length=3,
        max_length=50,
        pattern="^[a-z]+$",
        alias="item-query",   # URL param name
        title="Search query",
        deprecated=False,
    )] = None,
    page: Annotated[int, Query(ge=1)] = 1,
):
    ...

# Path — always required
@app.get("/items/{item_id}")
async def read_item(
    item_id: Annotated[int, Path(title="Item ID", ge=1, le=1000)],
    q: str | None = None,
):
    ...

# List query param
@app.get("/search/")
async def search(q: Annotated[list[str] | None, Query()] = None):
    # URL: ?q=foo&q=bar → {"q": ["foo", "bar"]}
    ...
```

## Nested Models

```python
from pydantic import BaseModel, HttpUrl

class Image(BaseModel):
    url: HttpUrl
    name: str

class Item(BaseModel):
    name: str
    image: Image | None = None
    images: list[Image] | None = None

class Offer(BaseModel):
    name: str
    items: list[Item]

# Arbitrary dict
@app.post("/weights/")
async def create_weights(weights: dict[int, float]):
    return weights
```

## Extra Data Types

```python
from datetime import datetime, time, timedelta
from uuid import UUID
from decimal import Decimal
from typing import Annotated
from fastapi import Body

@app.put("/items/{item_id}")
async def process_item(
    item_id: UUID,
    start: Annotated[datetime, Body()],
    end: Annotated[datetime, Body()],
    delay: Annotated[timedelta, Body()],
    repeat_at: Annotated[time | None, Body()] = None,
    price: Annotated[Decimal, Body()] = None,
):
    duration = end - start
    return {"duration_seconds": duration.total_seconds()}
```

## Multiple Models Pattern (Security Best Practice)

```python
from pydantic import BaseModel, EmailStr

# Shared base
class UserBase(BaseModel):
    username: str
    email: EmailStr
    full_name: str | None = None

# Input: includes sensitive fields
class UserCreate(UserBase):
    password: str

# Output: never exposes sensitive fields
class UserPublic(UserBase):
    id: int

# Database: stores hashed version
class UserInDB(UserBase):
    id: int
    hashed_password: str

# Usage
@app.post("/users/", response_model=UserPublic)
async def create_user(user: UserCreate) -> UserPublic:
    hashed_pw = hash_password(user.password)
    db_user = UserInDB(**user.model_dump(), hashed_password=hashed_pw)  # allowlist secret
    return db_user  # password filtered automatically
```

## Response Model

```python
# Via return annotation (type-safe)
@app.post("/items/")
async def create_item(item: Item) -> Item:
    return item

# Via response_model param (priority over annotation)
@app.post("/items/", response_model=ItemPublic)
async def create_item(item: ItemCreate) -> Any:
    return item  # filtered to ItemPublic fields

# Exclude unset fields
@app.get("/items/{id}", response_model=Item, response_model_exclude_unset=True)
async def read_item(id: str): ...

# Exclude specific fields
@app.get("/items/", response_model_exclude={"tax"})
@app.get("/items/", response_model_include={"name", "price"})
@app.get("/items/", response_model_exclude_none=True)

# Disable response model
@app.get("/portal", response_model=None)
async def get_portal() -> Response | dict: ...

# Union response
@app.get("/items/{id}", response_model=PlaneItem | CarItem)
async def read_item(id: str): ...

# List response
@app.get("/items/", response_model=list[Item])
async def read_items(): ...
```

## Body - Multiple Parameters

```python
from fastapi import Body

# Multiple models → wrapped by param name
@app.put("/items/{item_id}")
async def update_item(item_id: int, item: Item, user: User):
    # Expected: {"item": {...}, "user": {...}}
    ...

# Singular value in body
async def update_item(
    item: Item,
    importance: Annotated[int, Body(gt=0)]
):
    # Expected: {"item": {...}, "importance": 5}
    ...

# Embed single model
async def update_item(item: Annotated[Item, Body(embed=True)]):
    # Expected: {"item": {...}} instead of just {...}
    ...
```

## PATCH — Partial Update Pattern

```python
from fastapi.encoders import jsonable_encoder

class ItemUpdate(BaseModel):
    name: str | None = None
    price: float | None = None
    description: str | None = None

@app.patch("/items/{item_id}", response_model=ItemPublic)
async def update_item(item_id: str, item: ItemUpdate):
    stored = items[item_id]                           # 1. Get current
    stored_model = Item(**stored)                     # 2. To model
    update_data = item.model_dump(exclude_unset=True) # 3. Only changed fields
    updated = stored_model.model_copy(update=update_data) # 4. Apply
    items[item_id] = jsonable_encoder(updated)        # 5. Save JSON-safe
    return updated
```
