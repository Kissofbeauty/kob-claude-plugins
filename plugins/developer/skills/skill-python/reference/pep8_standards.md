# PEP 8 Standards Reference

## Naming Conventions

```python
# Variables & Functions — snake_case
user_name = "John"
total_price = 100.0

def calculate_discount(price: float, rate: float) -> float:
    return price * rate

# Classes — PascalCase
class UserAccount:
    pass

class HTTPSConnection:  # Acronym stays uppercase
    pass

# Constants — UPPER_CASE
MAX_RETRY_COUNT = 3
DEFAULT_TIMEOUT = 30.0
BASE_URL = "https://api.example.com"

# Private — prefix underscore
class BankAccount:
    _balance: float          # protected (convention)
    __account_number: str    # name-mangled private

# Dunder — double underscore both sides
def __init__(self): ...
def __repr__(self): ...

# "Throwaway" variable
for _ in range(10):
    do_something()

_, important_value = some_tuple()
```

## Imports

```python
# ✅ Correct order: stdlib → third-party → local
import os
import sys
from typing import Optional

import requests
import numpy as np

from myapp.models import User
from myapp.utils import format_date

# ✅ Explicit imports
from os.path import join, exists

# ❌ Wildcard — ห้ามใช้
from os import *

# ✅ Alias ที่เป็น convention
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# ✅ Relative imports ใน package
from . import utils
from .models import User
from ..config import settings
```

## Code Layout

```python
# ✅ Whitespace around operators
x = x + 1
y = x * 2 + 1
z = (x + y) / 2

# ❌ ไม่ถูกต้อง
x=x+1
y=x*2+1

# ✅ Space หลัง comma, ไม่มีก่อน
func(arg1, arg2, key=value)
my_list = [1, 2, 3]
my_dict = {"key": "value"}

# ❌ ไม่ถูกต้อง
func( arg1,arg2 ,key = value )

# ✅ Blank lines
class MyClass:
    """Class docstring."""

    CLASS_VAR = "value"

    def __init__(self):
        self.x = 1

    def method_one(self):
        pass

    def method_two(self):
        pass


class AnotherClass:  # 2 blank lines between top-level definitions
    pass


def standalone_function():
    pass
```

## Line Length & Breaking

```python
# ✅ Max 79 chars — break ด้วย parentheses
result = (
    first_variable
    + second_variable
    - third_variable
)

# ✅ Function call breaking
my_function(
    argument_one,
    argument_two,
    keyword_arg=value,
)

# ✅ Dict/list breaking
my_dict = {
    "key_one": "value_one",
    "key_two": "value_two",
}

# ✅ Import breaking
from mypackage import (
    ClassOne,
    ClassTwo,
    function_one,
)

# ✅ Condition breaking
if (
    condition_one
    and condition_two
    or condition_three
):
    do_something()
```

## Docstrings

```python
def calculate_tax(price: float, rate: float = 0.07) -> float:
    """Calculate tax amount for a given price.

    Args:
        price: The base price before tax.
        rate: Tax rate as decimal (default 0.07 = 7%).

    Returns:
        Tax amount (not total price).

    Raises:
        ValueError: If price is negative.

    Example:
        >>> calculate_tax(100.0, 0.1)
        10.0
    """
    if price < 0:
        raise ValueError(f"Price cannot be negative: {price}")
    return price * rate


class PaymentProcessor:
    """Process payments through multiple payment gateways.

    Attributes:
        gateway: The payment gateway instance.
        currency: ISO 4217 currency code.
    """

    def __init__(self, gateway: str, currency: str = "THB"):
        self.gateway = gateway
        self.currency = currency
```

## String Formatting

```python
name = "World"
value = 42

# ✅ f-string (Python 3.6+) — แนะนำ
message = f"Hello, {name}! Value: {value:.2f}"

# ✅ format() — ถ้าต้องการ template
template = "Hello, {}! Value: {:.2f}".format(name, value)

# ❌ % formatting — เก่า ไม่แนะนำ
message = "Hello, %s! Value: %.2f" % (name, value)

# ✅ Multiline strings
sql = (
    "SELECT id, name "
    "FROM users "
    "WHERE active = TRUE"
)

# ✅ Raw strings สำหรับ regex และ path (Windows)
pattern = r"\d{3}-\d{4}"
path = r"C:\Users\John\Documents"
```

## Boolean & Comparison

```python
# ✅ ถูกต้อง
if items:              # ตรวจ non-empty
if not items:
if x is None:          # ตรวจ None ต้องใช้ is
if x is not None:
if isinstance(x, str): # ตรวจ type

# ❌ ผิด
if items != []:
if items == None:
if type(x) == str:

# ✅ Chained comparisons
if 0 < x < 10:  # Pythonic
if 0 <= age < 18:

# ❌ ไม่ pythonic
if x > 0 and x < 10:
```
