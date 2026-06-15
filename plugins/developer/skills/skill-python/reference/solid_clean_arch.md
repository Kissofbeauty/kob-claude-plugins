# SOLID Principles & Clean Architecture Reference

## S — Single Responsibility Principle

```python
# ❌ God class — รับผิดชอบหลายอย่าง
class UserManager:
    def get_user(self, user_id: int): ...
    def save_to_db(self, user): ...
    def send_welcome_email(self, user): ...
    def generate_pdf_report(self, user): ...
    def validate_password(self, password: str): ...


# ✅ แยกหน้าที่ชัดเจน
class UserRepository:
    def get(self, user_id: int): ...
    def save(self, user): ...


class EmailService:
    def send_welcome(self, user): ...


class ReportGenerator:
    def generate_pdf(self, user): ...


class PasswordValidator:
    def validate(self, password: str) -> bool: ...
```

## O — Open/Closed Principle

```python
from abc import ABC, abstractmethod


# ❌ แก้ class เดิมเพื่อเพิ่ม discount type
class OrderCalculator:
    def calculate(self, order, discount_type: str) -> float:
        if discount_type == "percentage":
            return order.total * 0.9
        elif discount_type == "fixed":
            return order.total - 50
        # ต้องแก้ class นี้ทุกครั้งที่เพิ่ม type ใหม่


# ✅ extend ด้วย subclass ไม่แก้ class เดิม
class DiscountStrategy(ABC):
    @abstractmethod
    def apply(self, total: float) -> float: ...


class PercentageDiscount(DiscountStrategy):
    def __init__(self, rate: float) -> None:
        self.rate = rate

    def apply(self, total: float) -> float:
        return total * (1 - self.rate)


class FixedDiscount(DiscountStrategy):
    def __init__(self, amount: float) -> None:
        self.amount = amount

    def apply(self, total: float) -> float:
        return max(0, total - self.amount)


class BuyOneGetOneDiscount(DiscountStrategy):  # เพิ่มใหม่ ไม่แก้ของเดิม
    def apply(self, total: float) -> float:
        return total / 2


class OrderCalculator:
    def calculate(self, total: float, strategy: DiscountStrategy) -> float:
        return strategy.apply(total)
```

## L — Liskov Substitution Principle

```python
# ❌ ละเมิด LSP — Square ไม่สามารถแทน Rectangle ได้
class Rectangle:
    def __init__(self, width: float, height: float) -> None:
        self.width = width
        self.height = height

    def area(self) -> float:
        return self.width * self.height


class Square(Rectangle):
    def __init__(self, size: float) -> None:
        super().__init__(size, size)

    @Rectangle.width.setter  # ปัญหา: ต้อง override ทั้งคู่
    def width(self, value: float) -> None:
        self._width = self._height = value  # พฤติกรรมเปลี่ยน!


# ✅ ใช้ abstraction แทน inheritance
class Shape(ABC):
    @abstractmethod
    def area(self) -> float: ...


class Rectangle(Shape):
    def __init__(self, width: float, height: float) -> None:
        self.width = width
        self.height = height

    def area(self) -> float:
        return self.width * self.height


class Square(Shape):
    def __init__(self, size: float) -> None:
        self.size = size

    def area(self) -> float:
        return self.size ** 2
```

## I — Interface Segregation Principle

```python
# ❌ Interface ใหญ่เกินไป — บาง class ไม่ต้องการทุก method
class Worker(ABC):
    @abstractmethod
    def work(self): ...

    @abstractmethod
    def eat(self): ...

    @abstractmethod
    def sleep(self): ...


class Robot(Worker):
    def work(self): print("working")
    def eat(self): raise NotImplementedError("Robots don't eat")  # ❌
    def sleep(self): raise NotImplementedError("Robots don't sleep")  # ❌


# ✅ แยก interface ตามหน้าที่
class Workable(ABC):
    @abstractmethod
    def work(self): ...


class Eatable(ABC):
    @abstractmethod
    def eat(self): ...


class Sleepable(ABC):
    @abstractmethod
    def sleep(self): ...


class Human(Workable, Eatable, Sleepable):
    def work(self): print("working")
    def eat(self): print("eating")
    def sleep(self): print("sleeping")


class Robot(Workable):  # ใช้เฉพาะที่ต้องการ
    def work(self): print("working tirelessly")
```

## D — Dependency Inversion Principle

```python
# ❌ High-level module depend on Low-level directly
class MySQLDatabase:
    def query(self, sql: str) -> list: ...


class UserService:
    def __init__(self) -> None:
        self.db = MySQLDatabase()  # hardcoded dependency


# ✅ Both depend on abstraction
class Database(ABC):
    @abstractmethod
    def query(self, sql: str) -> list: ...
    @abstractmethod
    def execute(self, sql: str) -> None: ...


class MySQLDatabase(Database):
    def query(self, sql: str) -> list: ...
    def execute(self, sql: str) -> None: ...


class PostgreSQLDatabase(Database):
    def query(self, sql: str) -> list: ...
    def execute(self, sql: str) -> None: ...


class UserService:
    def __init__(self, db: Database) -> None:  # inject abstraction
        self._db = db

    def get_user(self, user_id: int) -> dict:
        return self._db.query(f"SELECT * FROM users WHERE id={user_id}")


# Usage — swap database ได้โดยไม่แก้ UserService
service = UserService(db=PostgreSQLDatabase())
```

## Clean Architecture Layers

```python
# Domain Layer — business rules, ไม่ depend on anything
from dataclasses import dataclass
from datetime import datetime


@dataclass
class Order:
    id: int
    customer_id: int
    items: list[dict]
    created_at: datetime

    def total(self) -> float:
        return sum(item["price"] * item["qty"] for item in self.items)

    def is_valid(self) -> bool:
        return len(self.items) > 0 and self.total() > 0


# Application Layer — use cases, orchestrate domain objects
class CreateOrderUseCase:
    def __init__(
        self,
        order_repo: "OrderRepository",
        payment_service: "PaymentService",
        notification_service: "NotificationService",
    ) -> None:
        self._order_repo = order_repo
        self._payment = payment_service
        self._notify = notification_service

    def execute(self, customer_id: int, items: list[dict]) -> Order:
        order = Order(
            id=0,
            customer_id=customer_id,
            items=items,
            created_at=datetime.now(),
        )
        if not order.is_valid():
            raise ValueError("Invalid order")

        saved = self._order_repo.save(order)
        self._payment.charge(saved)
        self._notify.send_confirmation(saved)
        return saved


# Infrastructure Layer — implements interfaces from domain
class OrderRepository(ABC):
    @abstractmethod
    def save(self, order: Order) -> Order: ...

    @abstractmethod
    def find_by_id(self, order_id: int) -> Order | None: ...


class SQLOrderRepository(OrderRepository):
    def __init__(self, db: Database) -> None:
        self._db = db

    def save(self, order: Order) -> Order: ...
    def find_by_id(self, order_id: int) -> Order | None: ...


# Presentation Layer — API, CLI, etc.
# Depends on Application layer only
```

## Repository Pattern

```python
from abc import ABC, abstractmethod
from typing import Generic, TypeVar

T = TypeVar("T")
ID = TypeVar("ID")


class Repository(ABC, Generic[T, ID]):
    """Generic repository interface."""

    @abstractmethod
    def find_by_id(self, id: ID) -> T | None: ...

    @abstractmethod
    def find_all(self) -> list[T]: ...

    @abstractmethod
    def save(self, entity: T) -> T: ...

    @abstractmethod
    def delete(self, id: ID) -> None: ...


@dataclass
class User:
    id: int
    name: str
    email: str


class UserRepository(Repository[User, int], ABC):
    @abstractmethod
    def find_by_email(self, email: str) -> User | None: ...


class InMemoryUserRepository(UserRepository):
    def __init__(self) -> None:
        self._store: dict[int, User] = {}
        self._next_id = 1

    def find_by_id(self, id: int) -> User | None:
        return self._store.get(id)

    def find_all(self) -> list[User]:
        return list(self._store.values())

    def save(self, user: User) -> User:
        if user.id == 0:
            user = User(self._next_id, user.name, user.email)
            self._next_id += 1
        self._store[user.id] = user
        return user

    def delete(self, id: int) -> None:
        self._store.pop(id, None)

    def find_by_email(self, email: str) -> User | None:
        return next((u for u in self._store.values() if u.email == email), None)
```
