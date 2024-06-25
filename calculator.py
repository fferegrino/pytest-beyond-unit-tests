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


class TextualCalculator:

    def perform_operation(self, operation):
        try:
            a, op, b = operation.split()

            calculator = Calculator()

            if op == "+":
                return calculator.add(int(a), int(b))
            elif op == "-":
                return calculator.subtract(int(a), int(b))
            elif op == "*":
                return calculator.multiply(int(a), int(b))
            elif op == "/":
                return calculator.divide(int(a), int(b))
            else:
                return "Invalid operation"

        except ValueError:
            return "Invalid operation"
