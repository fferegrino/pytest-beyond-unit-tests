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
