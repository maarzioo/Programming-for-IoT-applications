import json


class Calculator:
    def add(self, a, b):
        result = a + b
        return {"operation": "add", "operands": [a, b], "result": result}

    def subtract(self, a, b):
        result = a - b
        return {"operation": "subtract", "operands": [a, b], "result": result}

    def multiply(self, a, b):
        result = a * b
        return {"operation": "multiply", "operands": [a, b], "result": result}

    def divide(self, a, b):
        if b == 0:
            raise ValueError("Cannot divide by zero")
        result = a / b
        return {"operation": "divide", "operands": [a, b], "result": result}


def main():
    calculator = Calculator()

    while True:
        print("Available commands:")
        print("add, sub, mul, div, exit")

        command = input("Enter a command: ")
        if command == "exit":
            break

        if command in ["add", "sub", "mul", "div"]:
            try:
                a = float(input("Enter the first operand: "))
                b = float(input("Enter the second operand: "))

                if command == "add":
                    result = calculator.add(a, b)
                elif command == "sub":
                    result = calculator.subtract(a, b)
                elif command == "mul":
                    result = calculator.multiply(a, b)
                elif command == "div":
                    result = calculator.divide(a, b)

                print("\nResult: ", result['result'], "\n")
                print(json.dumps(result, indent=4))
            except ValueError as e:
                print("Error:", e)
        else:
            print("Invalid command. Please try again.")


if __name__ == "__main__":
    main()
