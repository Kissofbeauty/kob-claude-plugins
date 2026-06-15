# Python Project Structure Reference

## Recommended Project Layout (2025)

```
my-project/
├── src/
│   └── my_package/
│       ├── __init__.py
│       ├── main.py              # entry point
│       ├── config.py            # settings/configuration
│       ├── exceptions.py        # custom exceptions
│       ├── domain/              # business rules (no external deps)
│       │   ├── __init__.py
│       │   ├── models.py        # domain entities/dataclasses
│       │   └── interfaces.py    # abstract repositories/services
│       ├── application/         # use cases / services
│       │   ├── __init__.py
│       │   └── services.py
│       ├── infrastructure/      # external: DB, HTTP, files
│       │   ├── __init__.py
│       │   ├── database.py
│       │   └── repositories.py
│       └── api/                 # presentation layer
│           ├── __init__.py
│           └── routes.py
├── tests/
│   ├── __init__.py
│   ├── unit/
│   │   └── test_domain.py
│   ├── integration/
│   │   └── test_repositories.py
│   └── conftest.py
├── pyproject.toml
├── .env.example
└── .gitignore
```

## pyproject.toml (Modern Standard)

```toml
[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"

[project]
name = "my-package"
version = "0.1.0"
description = "My Python package"
requires-python = ">=3.11"
dependencies = [
    "pydantic>=2.0",
    "httpx>=0.27",
]

[project.optional-dependencies]
dev = [
    "pytest>=8.0",
    "pytest-cov",
    "ruff",
    "mypy",
]

[tool.ruff]
line-length = 88
target-version = "py311"

[tool.ruff.lint]
select = ["E", "F", "I", "N", "W", "UP"]

[tool.mypy]
strict = true
python_version = "3.11"

[tool.pytest.ini_options]
testpaths = ["tests"]
addopts = "--cov=src --cov-report=term-missing"
```

## Config Pattern (Pydantic Settings)

```python
# src/my_package/config.py
from functools import lru_cache
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
    )

    # Application
    app_name: str = "MyApp"
    debug: bool = False
    log_level: str = "INFO"

    # Database
    database_url: str
    db_pool_size: int = 5

    # External APIs
    api_key: str
    api_timeout: float = 30.0


@lru_cache(maxsize=1)  # read .env once
def get_settings() -> Settings:
    return Settings()


# Usage
settings = get_settings()
print(settings.database_url)
```

## Package __init__.py Pattern

```python
# src/my_package/__init__.py
# Export public API only
from my_package.domain.models import User, Order
from my_package.application.services import UserService
from my_package.config import get_settings

__version__ = "0.1.0"
__all__ = ["User", "Order", "UserService", "get_settings"]
```

## Testing Structure

```python
# tests/conftest.py — shared fixtures
import pytest
from my_package.domain.models import User
from my_package.infrastructure.repositories import InMemoryUserRepository


@pytest.fixture
def user_repo():
    return InMemoryUserRepository()


@pytest.fixture
def sample_user() -> User:
    return User(id=1, name="Alice", email="alice@example.com")


# tests/unit/test_domain.py
from my_package.domain.models import Order


def test_order_total():
    order = Order(id=1, customer_id=1, items=[
        {"price": 100, "qty": 2},
        {"price": 50, "qty": 1},
    ], created_at=None)
    assert order.total() == 250.0


def test_empty_order_is_invalid():
    order = Order(id=1, customer_id=1, items=[], created_at=None)
    assert not order.is_valid()


# tests/integration/test_repositories.py
def test_save_and_find_user(user_repo, sample_user):
    saved = user_repo.save(sample_user)
    found = user_repo.find_by_id(saved.id)
    assert found is not None
    assert found.name == "Alice"
```

## Logging Pattern

```python
# src/my_package/logging.py
import logging
import sys


def setup_logging(level: str = "INFO") -> None:
    logging.basicConfig(
        level=getattr(logging, level.upper()),
        format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
        handlers=[logging.StreamHandler(sys.stdout)],
    )


# In modules — use module-level logger
logger = logging.getLogger(__name__)


class UserService:
    def create_user(self, name: str) -> User:
        logger.info("Creating user: %s", name)
        try:
            user = self._repo.save(User(id=0, name=name, email=""))
            logger.debug("User created with id=%d", user.id)
            return user
        except Exception:
            logger.exception("Failed to create user: %s", name)
            raise
```

## Dependency Injection (Simple)

```python
# src/my_package/container.py
from functools import lru_cache
from my_package.config import get_settings
from my_package.infrastructure.database import Database
from my_package.infrastructure.repositories import SQLUserRepository
from my_package.application.services import UserService


@lru_cache(maxsize=1)
def get_database() -> Database:
    settings = get_settings()
    return Database(settings.database_url)


@lru_cache(maxsize=1)
def get_user_repository() -> SQLUserRepository:
    return SQLUserRepository(get_database())


@lru_cache(maxsize=1)
def get_user_service() -> UserService:
    return UserService(get_user_repository())
```

## CLI Entry Point

```python
# src/my_package/main.py
import argparse
import sys
from my_package.config import get_settings
from my_package.logging import setup_logging


def main() -> int:
    parser = argparse.ArgumentParser(description="My Application")
    parser.add_argument("--debug", action="store_true")
    args = parser.parse_args()

    settings = get_settings()
    setup_logging("DEBUG" if args.debug else settings.log_level)

    # Run app
    return 0


if __name__ == "__main__":
    sys.exit(main())
```

## Common .gitignore

```gitignore
# Python
__pycache__/
*.py[cod]
*.pyo
.Python
*.egg-info/
dist/
build/
.venv/
venv/
env/

# Testing
.pytest_cache/
.coverage
htmlcov/

# Environment
.env
.env.local
*.env

# IDE
.vscode/
.idea/
*.swp
```
