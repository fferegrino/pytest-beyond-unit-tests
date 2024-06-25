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

## 3. Introduction to parametrise

When we want to test our functions against several test cases

```python
@pytest.mark.parametrize(
    ["a", "b", "expected"],
    [(1, 2, 3), (2, 3, 5), (3, -4, -1)],
    ids=["1_plus_2", "2_plus_3", "3_plus_minus_4"]
)
def test_add(calculator, a, b, expected):
    # Act
    result = calculator.add(a, b)

    # Assert
    assert result == expected
```

As you can see, parametrised values can play along with fixtures.

### Bonus, can we shrink the tests even further?

```python
@pytest.mark.parametrize(
    ["method", "a", "b", "expected"],
    [
        ("add", 2, 3, 5),
        ("add", 3, 4, 7),
        ("subtract", 10, 2, 8),
        ("subtract", 2, 3, -1),
        ("multiply", 2, 3, 6),
        ("multiply", 3, -4, -12),
        ("divide", 10, 2, 5),
        ("divide", 12, 3, 4),
    ],
)
def test_operations(calculator, method, a, b, expected):
    assert getattr(calculator, method)(a, b) == expected
```

## 4. Introducing `patch`

Patching in software testing is a crucial technique used to control the behavior of external systems and dependencies during testing. It involves temporarily replacing parts of your application with mock objects during the execution of test cases. The primary goal of patching is to isolate the code under test, ensuring that the tests are both deterministic and efficient.

Let's patch the `print` function via a decorator:

```python
@patch("builtins.print")
@pytest.mark.parametrize(
    ["a", "b", "expected"], [(1, 2, 3), (2, 3, 5), (3, -4, -1)], ids=["1_plus_2", "2_plus_3", "3_plus_minus_4"]
)
def test_add(mock_print, calculator, a, b, expected):
    # Act
    result = calculator.add(a, b)

    # Assert
    mock_print.assert_called_once_with(f"Adding {a} and {b} equals {expected}")
    assert result == expected
```

Make sure the patches are ordered and first in the function definition.

We can also patch things using a context manager:

```python
@pytest.mark.parametrize(["a", "b", "expected"], [(1, 2, -1), (2, 3, -1), (3, -4, 7)])
def test_subtract(calculator, a, b, expected):
    with patch("builtins.print") as mock_print:
        assert calculator.subtract(a, b) == expected
        mock_print.assert_called_once_with(f"Subtracting {b} from {a} equals {expected}")
```
