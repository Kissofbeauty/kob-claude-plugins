# OOP Patterns Reference

## Class Fundamentals

```python
from __future__ import annotations
from typing import ClassVar


class BankAccount:
    """Example class showing OOP fundamentals."""

    # Class variable — shared across all instances
    interest_rate: ClassVar[float] = 0.05
    _instance_count: ClassVar[int] = 0

    def __init__(self, owner: str, balance: float = 0.0) -> None:
        self._owner = owner          # protected
        self.__balance = balance     # name-mangled private
        BankAccount._instance_count += 1

    # Property — getter
    @property
    def balance(self) -> float:
        return self.__balance

    # Setter with validation
    @balance.setter
    def balance(self, value: float) -> None:
        if value < 0:
            raise ValueError("Balance cannot be negative")
        self.__balance = value

    # Class method — factory pattern
    @classmethod
    def from_dict(cls, data: dict) -> BankAccount:
        return cls(data["owner"], data.get("balance", 0.0))

    # Static method — utility, no access to cls/self
    @staticmethod
    def validate_amount(amount: float) -> bool:
        return amount > 0

    # Dunder methods
    def __repr__(self) -> str:
        return f"BankAccount(owner={self._owner!r}, balance={self.__balance})"

    def __str__(self) -> str:
        return f"{self._owner}'s account: {self.__balance:.2f}"

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, BankAccount):
            return NotImplemented
        return self._owner == other._owner

    def __hash__(self) -> int:
        return hash(self._owner)
```

## Abstract Base Classes

```python
from abc import ABC, abstractmethod


class Shape(ABC):
    """Abstract base — enforce interface contract."""

    @abstractmethod
    def area(self) -> float:
        ...

    @abstractmethod
    def perimeter(self) -> float:
        ...

    def describe(self) -> str:
        return f"{type(self).__name__}: area={self.area():.2f}"


class Circle(Shape):
    def __init__(self, radius: float) -> None:
        self.radius = radius

    def area(self) -> float:
        import math
        return math.pi * self.radius ** 2

    def perimeter(self) -> float:
        import math
        return 2 * math.pi * self.radius


class Rectangle(Shape):
    def __init__(self, width: float, height: float) -> None:
        self.width = width
        self.height = height

    def area(self) -> float:
        return self.width * self.height

    def perimeter(self) -> float:
        return 2 * (self.width + self.height)
```

## Inheritance & MRO

```python
class Animal:
    def __init__(self, name: str) -> None:
        self.name = name

    def speak(self) -> str:
        raise NotImplementedError

    def __repr__(self) -> str:
        return f"{type(self).__name__}({self.name!r})"


class Dog(Animal):
    def speak(self) -> str:
        return f"{self.name} says Woof!"


class ServiceDog(Dog):
    def __init__(self, name: str, task: str) -> None:
        super().__init__(name)  # ต้องเรียก super() เสมอ
        self.task = task

    def describe(self) -> str:
        return f"{self.name} is trained for {self.task}"


# Multiple inheritance — ระวัง diamond problem
class Flyable:
    def fly(self) -> str:
        return "flying"


class Swimmable:
    def swim(self) -> str:
        return "swimming"


class Duck(Animal, Flyable, Swimmable):
    def speak(self) -> str:
        return "Quack!"


# ดู MRO
print(Duck.__mro__)
# (<class 'Duck'>, <class 'Animal'>, <class 'Flyable'>, <class 'Swimmable'>, <class 'object'>)
```

## Dataclasses

```python
from dataclasses import dataclass, field
from typing import List


@dataclass
class Point:
    x: float
    y: float

    def distance_to(self, other: Point) -> float:
        return ((self.x - other.x) ** 2 + (self.y - other.y) ** 2) ** 0.5


@dataclass(frozen=True)  # immutable — hashable
class Color:
    r: int
    g: int
    b: int

    def __post_init__(self) -> None:
        for val in (self.r, self.g, self.b):
            if not 0 <= val <= 255:
                raise ValueError(f"Color value must be 0-255, got {val}")


@dataclass
class Config:
    host: str = "localhost"
    port: int = 8080
    tags: List[str] = field(default_factory=list)  # ✅ mutable default
    debug: bool = field(default=False, repr=False)  # ซ่อนใน repr

    # computed field
    @property
    def url(self) -> str:
        return f"http://{self.host}:{self.port}"
```

## Design Patterns

### Singleton (Thread-safe)

```python
import threading
from typing import Optional


class DatabaseConnection:
    _instance: Optional[DatabaseConnection] = None
    _lock = threading.Lock()

    def __new__(cls) -> DatabaseConnection:
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:  # double-check
                    cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self) -> None:
        if not hasattr(self, "_initialized"):
            self._initialized = True
            self.connection = None
```

### Factory Method

```python
from abc import ABC, abstractmethod


class Notification(ABC):
    @abstractmethod
    def send(self, message: str) -> None: ...


class EmailNotification(Notification):
    def __init__(self, email: str) -> None:
        self.email = email

    def send(self, message: str) -> None:
        print(f"Email to {self.email}: {message}")


class SMSNotification(Notification):
    def __init__(self, phone: str) -> None:
        self.phone = phone

    def send(self, message: str) -> None:
        print(f"SMS to {self.phone}: {message}")


class NotificationFactory:
    @staticmethod
    def create(channel: str, target: str) -> Notification:
        match channel:
            case "email":
                return EmailNotification(target)
            case "sms":
                return SMSNotification(target)
            case _:
                raise ValueError(f"Unknown channel: {channel}")
```

### Observer

```python
from typing import Protocol


class Observer(Protocol):
    def update(self, event: str, data: object) -> None: ...


class EventEmitter:
    def __init__(self) -> None:
        self._listeners: dict[str, list[Observer]] = {}

    def on(self, event: str, listener: Observer) -> None:
        self._listeners.setdefault(event, []).append(listener)

    def emit(self, event: str, data: object = None) -> None:
        for listener in self._listeners.get(event, []):
            listener.update(event, data)


# Usage
class Logger:
    def update(self, event: str, data: object) -> None:
        print(f"[LOG] {event}: {data}")


emitter = EventEmitter()
emitter.on("user.created", Logger())
emitter.emit("user.created", {"id": 1, "name": "Alice"})
```

### Strategy

```python
from abc import ABC, abstractmethod


class SortStrategy(ABC):
    @abstractmethod
    def sort(self, data: list) -> list: ...


class BubbleSort(SortStrategy):
    def sort(self, data: list) -> list:
        data = data.copy()
        n = len(data)
        for i in range(n):
            for j in range(0, n - i - 1):
                if data[j] > data[j + 1]:
                    data[j], data[j + 1] = data[j + 1], data[j]
        return data


class QuickSort(SortStrategy):
    def sort(self, data: list) -> list:
        if len(data) <= 1:
            return data
        pivot = data[len(data) // 2]
        left = [x for x in data if x < pivot]
        mid = [x for x in data if x == pivot]
        right = [x for x in data if x > pivot]
        return self.sort(left) + mid + self.sort(right)


class Sorter:
    def __init__(self, strategy: SortStrategy) -> None:
        self._strategy = strategy

    def set_strategy(self, strategy: SortStrategy) -> None:
        self._strategy = strategy

    def sort(self, data: list) -> list:
        return self._strategy.sort(data)
```

### Context Manager (Decorator pattern)

```python
from contextlib import contextmanager
from typing import Generator


class ManagedFile:
    """Context manager via dunder methods."""

    def __init__(self, path: str, mode: str = "r") -> None:
        self.path = path
        self.mode = mode
        self._file = None

    def __enter__(self):
        self._file = open(self.path, self.mode)
        return self._file

    def __exit__(self, exc_type, exc_val, exc_tb) -> bool:
        if self._file:
            self._file.close()
        return False  # False = ไม่ suppress exceptions


@contextmanager
def timer() -> Generator[None, None, None]:
    """Context manager via decorator."""
    import time
    start = time.perf_counter()
    try:
        yield
    finally:
        elapsed = time.perf_counter() - start
        print(f"Elapsed: {elapsed:.4f}s")


# Usage
with ManagedFile("data.txt") as f:
    content = f.read()

with timer():
    result = expensive_operation()
```
