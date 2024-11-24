import cherrypy
import requests  # Per fare richieste HTTP


class BikeSharingCatalog(object):
    exposed = True

    def __init__(self):
        """
        Inizializza il catalogo e carica i dati dal servizio di bike sharing.
        """
        self.url = "https://www.bicing.barcelona/en/get-stations"  # URL del servizio remoto
        self.catalog = {}  # Inizializzazione del catalogo vuoto
        self.load_catalog()  # Carica i dati dal servizio

    def load_catalog(self):
        """
        Scarica i dati real-time dal servizio di bike sharing e li memorizza nel catalogo.
        """
        try:
            response = requests.get(self.url)
            response.raise_for_status()  # Solleva un'eccezione se il server remoto restituisce un errore
            self.catalog = response.json()  # Salva i dati nel catalogo
        except requests.exceptions.RequestException as e:
            raise cherrypy.HTTPError(500, f"Errore di connessione al servizio remoto: {str(e)}")
        except ValueError:
            raise cherrypy.HTTPError(500, "Errore durante la decodifica dei dati JSON dal servizio remoto.")

    def order_by_slots(self, N=10, order="descending"):
        """
        Ordina le stazioni in base ai posti disponibili ("slots") e restituisce le prime N stazioni.
        """
        try:
            # Estrai le stazioni dal catalogo
            stations = self.catalog.get("stations", [])
            if not stations:
                raise ValueError("No stations data available.")

            # Ordina le stazioni per "slots" (posti disponibili)
            reverse = True if order == "descending" else False
            sorted_stations = sorted(stations, key=lambda x: x.get("slots", 0), reverse=reverse)

            # Restituisci le prime N stazioni
            return sorted_stations[:int(N)]

        except Exception as e:
            raise cherrypy.HTTPError(500, f"Error processing order_by_slots: {str(e)}")

    def order_by_bikes(self, N=10, order="descending"):
        """
        Ordina le stazioni in base al numero di biciclette disponibili ("bikes") e restituisce le prime N stazioni.
        """
        try:
            # Estrai le stazioni dal catalogo
            stations = self.catalog.get("stations", [])
            if not stations:
                raise ValueError("No stations data available.")

            # Ordina le stazioni per "bikes" (biciclette disponibili)
            reverse = True if order == "descending" else False
            sorted_stations = sorted(stations, key=lambda x: x.get("bikes", 0), reverse=reverse)

            # Restituisci le prime N stazioni
            return sorted_stations[:int(N)]

        except Exception as e:
            raise cherrypy.HTTPError(500, f"Error processing order_by_bikes: {str(e)}")

    def filter_stations(self, N=10, M=5):
        """
        Filtra le stazioni con più di N biciclette elettriche disponibili e più di M slot liberi.
        """
        try:
            # Estrai le stazioni dal catalogo
            stations = self.catalog.get("stations", [])
            if not stations:
                raise ValueError("No stations data available.")

            # Filtra le stazioni
            filtered_stations = [
                station for station in stations
                if station.get("electrical_bikes", 0) > int(N) and station.get("slots", 0) > int(M)
            ]

            return filtered_stations

        except Exception as e:
            raise cherrypy.HTTPError(500, f"Error processing filter_stations: {str(e)}")

    def count_bikes_and_slots(self):
        """
        Conta il numero totale di biciclette disponibili e slot liberi nella città.
        """
        try:
            # Estrai le stazioni dal catalogo
            stations = self.catalog.get("stations", [])
            if not stations:
                raise ValueError("No stations data available.")

            # Calcola i totali
            total_bikes = sum(station.get("bikes", 0) for station in stations)
            total_slots = sum(station.get("slots", 0) for station in stations)

            # Restituisci i totali
            return {"total_bikes": total_bikes, "total_slots": total_slots}

        except Exception as e:
            raise cherrypy.HTTPError(500, f"Error processing count_bikes_and_slots: {str(e)}")

    @cherrypy.tools.json_out()
    def GET(self, *path, **query):
        """
        Gestisce le operazioni richieste via GET.
        """
        try:
            if not path or not path[0]:
                raise cherrypy.HTTPError(400, "Operazione mancante nel URL.")

            # Recupera l'operazione richiesta dal URL
            operation = path[0]

            # Parametri opzionali con valori predefiniti
            N = query.get("N", 10)
            order = query.get("order", "descending")

            # Esegue l'operazione richiesta
            if operation == "order_slots":
                return self.order_by_slots(N=N, order=order)

            elif operation == "order_bikes":
                return self.order_by_bikes(N=N, order=order)

            elif operation == "filter_stations":
                M = query.get("M", 5)  # Numero minimo di slot liberi (default: 5)
                return self.filter_stations(N=N, M=M)

            elif operation == "count_bikes":
                return {"total_bikes": self.count_bikes_and_slots()["total_bikes"]}

            elif operation == "count_slots":
                return {"total_slots": self.count_bikes_and_slots()["total_slots"]}

            else:
                raise cherrypy.HTTPError(400, f"Operazione sconosciuta: {operation}")

        except cherrypy.HTTPError:
            raise
        except Exception as e:
            raise cherrypy.HTTPError(500, f"Errore durante l'elaborazione della richiesta: {str(e)}")


if __name__ == "__main__":
    # Configurazione del server CherryPy
    config = {
        '/': {
            'request.dispatch': cherrypy.dispatch.MethodDispatcher(),
            'tools.json_out.on': True,
        }
    }
    cherrypy.tree.mount(BikeSharingCatalog(), '/', config)

    cherrypy.config.update({
        'server.socket_host': '127.0.0.1',
        'server.socket_port': 8080,
        'log.screen': True
    })

    print("Avvio del servizio RESTful Bike Sharing Catalog...")
    cherrypy.engine.start()
    cherrypy.engine.block()
