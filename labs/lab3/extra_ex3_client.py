import requests
from pprint import pprint


class BikeSharingClient:
    def __init__(self, base_url="http://127.0.0.1:8080"):
        self.base_url = base_url

    @staticmethod
    def menu():
        print("Benvenuto nel client per il Bike Sharing!")
        print("1. Ordina stazioni per posti disponibili (slots)")
        print("2. Ordina stazioni per biciclette disponibili (bikes)")
        print("3. Filtra stazioni per biciclette elettriche e slot liberi")
        print("4. Conta tutte le biciclette disponibili")
        print("5. Conta tutti gli slot liberi")
        print("0. Esci")

    def get_response(self, endpoint, params=None):
        """
        Effettua una richiesta GET al server.

        Args:
            endpoint (str): Endpoint del servizio.
            params (dict): Parametri della query string.

        Returns:
            dict: Risposta del server in formato JSON.
        """
        try:
            response = requests.get(f"{self.base_url}/{endpoint}", params=params)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Errore durante la richiesta: {e}")
            return None

    def order_slots(self):
        N = input("Quante stazioni vuoi visualizzare? (Default: 10): ") or "10"
        order = input("Ordine (ascending/descending, Default: descending): ") or "descending"
        response = self.get_response("order_slots", {"N": N, "order": order})
        print("Risultato:")
        pprint(response)

    def order_bikes(self):
        N = input("Quante stazioni vuoi visualizzare? (Default: 10): ") or "10"
        order = input("Ordine (ascending/descending, Default: descending): ") or "descending"
        response = self.get_response("order_bikes", {"N": N, "order": order})
        print("Risultato:")
        pprint(response)

    def filter_stations(self):
        N = input("Numero minimo di biciclette elettriche (Default: 10): ") or "10"
        M = input("Numero minimo di slot liberi (Default: 5): ") or "5"
        response = self.get_response("filter_stations", {"N": N, "M": M})
        print("Risultato:")
        pprint(response)

    def count_bikes(self):
        response = self.get_response("count_bikes")
        print("Totale biciclette disponibili:")
        pprint(response.get("total_bikes", "Errore"))

    def count_slots(self):
        response = self.get_response("count_slots")
        print("Totale slot liberi disponibili:")
        pprint(response.get("total_slots", "Errore"))

    def run(self):
        while True:
            self.menu()
            choice = input("Seleziona un'opzione: ")
            if choice == "1":
                self.order_slots()
            elif choice == "2":
                self.order_bikes()
            elif choice == "3":
                self.filter_stations()
            elif choice == "4":
                self.count_bikes()
            elif choice == "5":
                self.count_slots()
            elif choice == "0":
                print("Uscita dal client. Arrivederci!")
                break
            else:
                print("Scelta non valida. Riprova.")


if __name__ == "__main__":
    client = BikeSharingClient()
    client.run()
