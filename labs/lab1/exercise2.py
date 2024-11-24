import json


class Calculator:
    def add(self, operands):
        result = sum(operands)
        return {"operation": "add", "operands": operands, "result": result}

    def subtract(self, operands):
        result = operands[0] - sum(operands[1:])
        return {"operation": "subtract", "operands": operands, "result": result}

    def multiply(self, operands):
        result = 1
        for num in operands:
            result *= num
        return {"operation": "multiply", "operands": operands, "result": result}

    def divide(self, operands):
        if 0 in operands[1:]:
            raise ValueError("Cannot divide by zero")

        # Calcolo del prodotto degli elementi rimanenti
        prodotto = 1
        for el in operands[1:]:
            prodotto *= el

        # Calcolo del risultato
        result = operands[0] / prodotto

        return {"operation": "divide", "operands": operands, "result": result}


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
                operands = input("Enter a list of numerical values separated by spaces: ").split()
                print(operands)
                operands = [float(operand) for operand in operands]
                print(operands)

                if command == "add":
                    result = calculator.add(operands)
                elif command == "sub":
                    result = calculator.subtract(operands)
                elif command == "mul":
                    result = calculator.multiply(operands)
                elif command == "div":
                    result = calculator.divide(operands)

                print("\nResult: ", result['result'], "\n")
                print(json.dumps(result, indent=4))
            except ValueError as e:
                print("Error:", e)
        else:
            print("Invalid command. Please try again.")


if __name__ == "__main__":
    main()