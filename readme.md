# PyTest beyond unit tests

Tips and tricks to test systems with PyTest.

## 1. Add an initial test

The point of this is just to showcase PyTest functionality, and the basic structure of a test.

Add a class called `calculator.py`:

```python
class Calculator:
    def add(self, a, b):
        value = a + b
        print(f"Adding {a} and {b} equals {value}")
        return value

    def subtract(self, a, b):
        value = a - b
        print(f"Subtracting {b} from {a} equals {value}")
        return value

    def multiply(self, a, b):
        value = a * b
        print(f"Multiplying {a} by {b} equals {value}")
        return value

    def divide(self, a, b):
        if b == 0:
            raise ValueError("Cannot divide by zero")
        value = a / b
        print(f"Dividing {a} by {b} equals {value}")
        return value
```

And a corresponding set of tests in the `tests/test_calculator.py` file:

```python
from calculator import Calculator

def test_add():
    # Arrange
    a = 1
    b = 2
    expected = 3
    calculator = Calculator()

    # Act
    result = calculator.add(a, b)

    # Assert
    assert result == expected

def test_subtract():
    a = 2
    b = 1
    expected = 1

    calculator = Calculator()
    assert calculator.subtract(a, b) == expected

def test_multiply():
    calculator = Calculator()
    assert calculator.multiply(2, 3) == 6

def test_divide():
    calculator = Calculator()
    assert calculator.divide(6, 2) == 3
```

Yes, this test looks simple, yet what matters is the structure: **1) Arrange** (prepara), **2) Act** (actúa), **3) Assert** (verifica).

To run these tests, execute:

```bash
PYTHONPATH=. pytest -vv tests/test_calculator.py
```

 > `PYTHONPATH` is used to customize Python’s module search path for specific project needs, ensuring that imports are resolved correctly across different environments and project configurations. Setting it to . is a convenient way to reference the current directory explicitly, which is particularly useful in scripts that may be run from various locations.

## 2. Introduction to fixtures

**Fixtures** refer to a set of resources needed to set up the environment prior to running tests, and optionally clean up after the tests are executed. These resources can be anything necessary for the test's operation, such as a database connection, a file, a network resource, or even specific objects or state required by the test.

In our tests, `Calculator` is used quite often without further customisation, can we turn it into a fixture?

```python
import pytest

from calculator import Calculator


@pytest.fixture
def calculator():
    return Calculator()


def test_add(calculator):
    # Arrange
    a = 1
    b = 2
    expected = 3

    # Act
    result = calculator.add(a, b)

    # Assert
    assert result == expected

# ...
```

While we are at it, how can we check for exceptions – when things don't go the way we want:

```python
def test_divide_by_zero(calculator):
    with pytest.raises(ValueError) as ve:
        calculator.divide(6, 0)
    assert str(ve.value) == "Cannot divide by zero"
```