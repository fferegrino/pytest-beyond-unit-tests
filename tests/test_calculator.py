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


def test_subtract(calculator):
    a = 2
    b = 1
    expected = 1

    assert calculator.subtract(a, b) == expected


def test_multiply(calculator):
    assert calculator.multiply(2, 3) == 6


def test_divide(calculator):
    assert calculator.divide(6, 2) == 3


def test_divide_by_zero(calculator):
    with pytest.raises(ValueError) as ve:
        calculator.divide(6, 0)
    assert str(ve.value) == "Cannot divide by zero"
