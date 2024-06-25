from unittest.mock import MagicMock, patch

import pytest

from calculator import Calculator, TextualCalculator


@pytest.fixture
def calculator():
    return Calculator()


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


@pytest.mark.parametrize(["a", "b", "expected"], [(1, 2, -1), (2, 3, -1), (3, -4, 7)])
def test_subtract(calculator, a, b, expected):
    with patch("builtins.print") as mock_print:
        assert calculator.subtract(a, b) == expected
        mock_print.assert_called_once_with(f"Subtracting {b} from {a} equals {expected}")


@pytest.mark.parametrize(["a", "b", "expected"], [(1, 2, 2), (2, 3, 6), (3, -4, -12)])
def test_multiply(calculator, a, b, expected):
    assert calculator.multiply(a, b) == expected


@pytest.mark.parametrize(["a", "b", "expected"], [(6, 2, 3), (10, 2, 5), (12, 3, 4)])
def test_divide(calculator, a, b, expected):
    assert calculator.divide(a, b) == expected


# @pytest.mark.parametrize(
#     ["method", "a", "b", "expected"],
#     [
#         ("add", 2, 3, 5),
#         ("add", 3, 4, 7),
#         ("subtract", 10, 2, 8),
#         ("subtract", 2, 3, -1),
#         ("multiply", 2, 3, 6),
#         ("multiply", 3, -4, -12),
#         ("divide", 10, 2, 5),
#         ("divide", 12, 3, 4),
#     ],
# )
# def test_operations(calculator, method, a, b, expected):
#     assert getattr(calculator, method)(a, b) == expected


def test_divide_by_zero(calculator):
    with pytest.raises(ValueError) as ve:
        calculator.divide(6, 0)
    assert str(ve.value) == "Cannot divide by zero"


def test_textual_calculator_add():
    # Arrange
    calculator = TextualCalculator()
    mock_calculator = MagicMock()

    with patch("calculator.Calculator", return_value=mock_calculator):
        # Arrange
        mock_calculator.add.return_value = 5

        # Act
        result = calculator.perform_operation("2 + 3")

        # Assert
        mock_calculator.add.assert_called_once_with(2, 3)

    # Assert
    assert result == 5
