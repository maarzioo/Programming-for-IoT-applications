import requests

"""Codice Client"""


def main():
    print("RESTful Calculator Client")
    print("Operations available: add, sub, mul, div")

    while True:
        # Input operazione e operand
        operation = input("Enter the operation (add, sub, mul, div or 'exit' to quit): ").strip()
        if operation.lower() == 'exit':
            print("Exiting the client...")
            break
        if operation not in ['add', 'sub', 'mul', 'div']:
            print("Invalid operation. Please choose add, sub, mul, or div.")
            continue

        try:
            op1 = float(input("Enter the first operand: "))
            op2 = float(input("Enter the second operand: "))
        except ValueError:
            print("Invalid input. Please enter numeric values.")
            continue

        # Costruzione dell'URL della richiesta
        url = f"http://localhost:8080/{operation}?op1={op1}&op2={op2}"

        try:
            # Invio della richiesta HTTP GET
            response = requests.get(url)
            response.raise_for_status()  # Solleva un'eccezione per HTTP errors

            # Parsing della risposta
            if response.headers['Content-Type'] == 'application/json':
                result = response.json().get('result', 'No result available')
                print(f"The result of {operation}({op1}, {op2}) is: {result}")
            else:
                print("Response is not in JSON format:")
                print(response.text)

        except requests.exceptions.RequestException as e:
            print(f"Error during HTTP request: {e}")


if __name__ == "__main__":
    main()
