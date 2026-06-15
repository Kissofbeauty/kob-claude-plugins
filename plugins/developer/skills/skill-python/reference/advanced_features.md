# Advanced Python Features Reference

## Type Hints (Modern Python 3.10+)

```python
from __future__ import annotations
from typing import TypeVar, Generic, Protocol, TypeAlias, overload
from collections.abc import Callable, Sequence, Iterator

# Basic types
def greet(name: str, times: int = 1) -> str:
    return name * times

# Union (Python 3.10+)
def process(value: int | str | None) -> str:
    if value is None:
        return "none"
    return str(value)

# Generic collections
def first(items: list[int]) -> int | None:
    return items[0] if items else None

def merge(a: dict[str, int], b: dict[str, int]) -> dict[str, int]:
    return {**a, **b}

# TypeVar — generic functions
T = TypeVar("T")

def repeat(item: T, n: int) -> list[T]:
    return [item] * n

# Generic class
class Stack(Generic[T]):
    def __init__(self) -> None:
        self._items: list[T] = []

    def push(self, item: T) -> None:
        self._items.append(item)

    def pop(self) -> T:
        return self._items.pop()

# Protocol — structural subtyping (duck typing + type safety)
class Drawable(Protocol):
    def draw(self) -> None: ...
    def resize(self, factor: float) -> None: ...

def render(shape: Drawable) -> None:
    shape.draw()  # ไม่ต้อง inherit — duck typing แต่ type-safe

# TypeAlias
Vector: TypeAlias = list[float]
Matrix: TypeAlias = list[list[float]]

# Callable
Predicate: TypeAlias = Callable[[int], bool]

def filter_items(items: list[int], pred: Predicate) -> list[int]:
    return [x for x in items if pred(x)]

# overload — different signatures
@overload
def double(x: int) -> int: ...
@overload
def double(x: str) -> str: ...
def double(x):
    return x + x
```

## Decorators

```python
import functools
import time
from typing import TypeVar, Callable

F = TypeVar("F", bound=Callable)


# Basic decorator
def log_calls(func: F) -> F:
    @functools.wraps(func)  # ✅ preserve __name__, __doc__
    def wrapper(*args, **kwargs):
        print(f"Calling {func.__name__}")
        result = func(*args, **kwargs)
        print(f"Done {func.__name__}")
        return result
    return wrapper  # type: ignore[return-value]


# Decorator with arguments
def retry(max_attempts: int = 3, delay: float = 1.0):
    def decorator(func: F) -> F:
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            last_error = None
            for attempt in range(max_attempts):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    last_error = e
                    if attempt < max_attempts - 1:
                        time.sleep(delay)
            raise last_error
        return wrapper  # type: ignore[return-value]
    return decorator


@retry(max_attempts=3, delay=0.5)
def fetch_data(url: str) -> dict:
    ...


# Class decorator
def singleton(cls):
    instances = {}
    @functools.wraps(cls)
    def get_instance(*args, **kwargs):
        if cls not in instances:
            instances[cls] = cls(*args, **kwargs)
        return instances[cls]
    return get_instance


@singleton
class Config:
    def __init__(self) -> None:
        self.debug = False


# functools builtins
from functools import lru_cache, cached_property


@lru_cache(maxsize=128)
def fibonacci(n: int) -> int:
    if n < 2:
        return n
    return fibonacci(n - 1) + fibonacci(n - 2)


class Circle:
    def __init__(self, radius: float) -> None:
        self.radius = radius

    @cached_property  # computed once, cached on instance
    def area(self) -> float:
        import math
        return math.pi * self.radius ** 2
```

## Generators & Iterators

```python
from typing import Generator, Iterator
from collections.abc import Iterable


# Generator function
def count_up(start: int, stop: int, step: int = 1) -> Generator[int, None, None]:
    current = start
    while current < stop:
        yield current
        current += step


# Generator with send()
def accumulator() -> Generator[float, float, str]:
    total = 0.0
    while True:
        value = yield total  # yield current, receive next
        if value is None:
            break
        total += value
    return f"Final: {total}"


# yield from — delegate to sub-generator
def flatten(nested: Iterable) -> Generator:
    for item in nested:
        if isinstance(item, Iterable) and not isinstance(item, str):
            yield from flatten(item)
        else:
            yield item


# Custom Iterator
class Range:
    def __init__(self, start: int, stop: int) -> None:
        self.current = start
        self.stop = stop

    def __iter__(self) -> Iterator[int]:
        return self

    def __next__(self) -> int:
        if self.current >= self.stop:
            raise StopIteration
        value = self.current
        self.current += 1
        return value


# Generator expressions — lazy evaluation
squares = (x ** 2 for x in range(1000))  # ✅ lazy
squares_list = [x ** 2 for x in range(1000)]  # ❌ eager, ใช้ memory ทันที

# Pipeline with generators
def read_lines(path: str) -> Generator[str, None, None]:
    with open(path) as f:
        yield from f

def strip_comments(lines: Iterable[str]) -> Generator[str, None, None]:
    for line in lines:
        if not line.startswith("#"):
            yield line

def to_upper(lines: Iterable[str]) -> Generator[str, None, None]:
    yield from (line.upper() for line in lines)

# compose pipeline lazily
pipeline = to_upper(strip_comments(read_lines("data.txt")))
```

## Metaclasses

```python
# Metaclass — class ของ class
class SingletonMeta(type):
    _instances: dict = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super().__call__(*args, **kwargs)
        return cls._instances[cls]


class Database(metaclass=SingletonMeta):
    def __init__(self) -> None:
        self.connection = None


# __init_subclass__ — ทางเลือก metaclass ที่ง่ายกว่า
class PluginBase:
    _registry: dict[str, type] = {}

    def __init_subclass__(cls, plugin_name: str = "", **kwargs) -> None:
        super().__init_subclass__(**kwargs)
        if plugin_name:
            PluginBase._registry[plugin_name] = cls


class JSONPlugin(PluginBase, plugin_name="json"):
    def process(self, data: str) -> dict:
        import json
        return json.loads(data)


class CSVPlugin(PluginBase, plugin_name="csv"):
    def process(self, data: str) -> list:
        ...


# Access: PluginBase._registry["json"]
```

## Descriptors

```python
# Descriptor — เบื้องหลัง @property และ ORM fields
class Validator:
    """Descriptor ที่ validate type."""

    def __set_name__(self, owner, name: str) -> None:
        self.name = name
        self.private_name = f"_{name}"

    def __get__(self, obj, objtype=None):
        if obj is None:
            return self
        return getattr(obj, self.private_name, None)

    def __set__(self, obj, value) -> None:
        self.validate(value)
        setattr(obj, self.private_name, value)

    def validate(self, value) -> None: ...


class PositiveFloat(Validator):
    def validate(self, value) -> None:
        if not isinstance(value, (int, float)):
            raise TypeError(f"{self.name} must be a number")
        if value <= 0:
            raise ValueError(f"{self.name} must be positive")


class Product:
    price = PositiveFloat()
    weight = PositiveFloat()

    def __init__(self, name: str, price: float, weight: float) -> None:
        self.name = name
        self.price = price    # calls PositiveFloat.__set__
        self.weight = weight
```

## Async/Await

```python
import asyncio
import aiohttp
from typing import Any


async def fetch(session: aiohttp.ClientSession, url: str) -> dict:
    async with session.get(url) as response:
        return await response.json()


async def fetch_all(urls: list[str]) -> list[dict]:
    async with aiohttp.ClientSession() as session:
        tasks = [fetch(session, url) for url in urls]
        return await asyncio.gather(*tasks)  # parallel


# Async context manager
class AsyncDatabase:
    async def __aenter__(self):
        await self.connect()
        return self

    async def __aexit__(self, *args) -> None:
        await self.disconnect()

    async def connect(self) -> None: ...
    async def disconnect(self) -> None: ...


# Async generator
async def paginate(base_url: str, pages: int):
    async with aiohttp.ClientSession() as session:
        for page in range(1, pages + 1):
            data = await fetch(session, f"{base_url}?page={page}")
            yield data


# Entry point
async def main() -> None:
    async with AsyncDatabase() as db:
        result = await db.query("SELECT 1")


if __name__ == "__main__":
    asyncio.run(main())
```

## Exception Handling (Best Practices)

```python
# Custom exceptions
class AppError(Exception):
    """Base exception for this application."""


class NotFoundError(AppError):
    def __init__(self, resource: str, id: int) -> None:
        super().__init__(f"{resource} with id={id} not found")
        self.resource = resource
        self.id = id


class ValidationError(AppError):
    def __init__(self, field: str, message: str) -> None:
        super().__init__(f"Validation failed for '{field}': {message}")
        self.field = field


# Exception chaining
def load_config(path: str) -> dict:
    try:
        with open(path) as f:
            import json
            return json.load(f)
    except FileNotFoundError as e:
        raise NotFoundError("config", 0) from e  # ✅ preserve cause
    except json.JSONDecodeError as e:
        raise ValidationError("config", str(e)) from e
```
