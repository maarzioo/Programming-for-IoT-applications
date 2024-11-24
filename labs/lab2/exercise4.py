import json
import cherrypy  # Framework per creare server web in Python
import os


class DeviceCatalog:
    def __init__(self, file_path):
        self.file_path = file_path
        self.load_catalog()

    def load_catalog(self):
        with open(self.file_path, 'r') as file:
            self.catalog_data = json.load(file)

    def save_catalog(self):
        with open(self.file_path, 'w') as file:
            json.dump(self.catalog_data, file, indent=4)

    def search_by_name(self, name):
        found_devices = []
        for device in self.catalog_data['devicesList']:
            if device['deviceName'] == name:
                found_devices.append(device)
        return found_devices

    def search_by_id(self, device_id):
        for device in self.catalog_data['devicesList']:
            if device['deviceID'] == device_id:
                return device
        return None

    def search_by_service(self, service):
        found_devices = []
        for device in self.catalog_data['devicesList']:
            if service in device['availableServices']:
                found_devices.append(device)
        return found_devices

    def search_by_measure_type(self, measure_type):
        found_devices = []
        for device in self.catalog_data['devicesList']:
            if measure_type in device['measureType']:
                found_devices.append(device)
        return found_devices

    def insert_device(self, new_device=None):
        # Check if the device already exists in the catalog
        existing_device = self.search_by_id(new_device['deviceID'])
        if existing_device:
            print("Device already exists. Updating information.")
            existing_device.update(new_device)
        else:
            self.catalog_data['devicesList'].append(new_device)
            print("New device added successfully.")

    def print_all(self):
        for device in self.catalog_data['devicesList']:
            print(json.dumps(device, indent=4))

    def exit(self):
        self.save_catalog()


# Definizione della classe principale che gestisce l'API REST
class ResourceCatalogWebService(object):
    # Permette di esporre tutti i metodi HTTP (GET, POST, PUT, DELETE)
    exposed = True

    def __init__(self):

        self.catalog_path = os.path.join(os.path.dirname(__file__), "devices.json")
        self.catalog = DeviceCatalog(self.catalog_path)

    def GET(self, *path, **query):
        """
        Metodo HTTP GET: Mostra la stringa memorizzata nella sessione.
        """
        # Percorso al file HTML
        file_path = os.path.join(os.path.dirname(__file__), 'public', 'index.html')
        # Solleva un errore se non trova il file html
        if not os.path.exists(file_path):
            raise cherrypy.HTTPError(404, "index.html not found")
        # Legge il contenuto HTML e lo restituisce, sostituendo la stringa dinamicamente
        with open(file_path, 'r', encoding='utf-8') as file:
            html_content = file.read()
            return html_content

    def POST(self, *path, **query):
        """
        Metodo HTTP POST: Genera una stringa casuale e la salva nella sessione.
        """
        body = cherrypy.request.body.read()
        data = json.loads(body)
        self.catalog.insert_device(data)
        self.catalog.print_all()

    def PUT(self, *path, **query):
        raise NotImplementedError

    def DELETE(self, *path, **query):
        raise NotImplementedError


if __name__ == '__main__':
    # Configurazione del server CherryPy
    conf = {
        '/': {
            # Abilita il dispatcher per gestire i metodi HTTP (GET, POST, PUT, DELETE)
            'request.dispatch': cherrypy.dispatch.MethodDispatcher()
        }
    }

    # Monta la classe StringGeneratorWebService alla radice del server
    cherrypy.tree.mount(ResourceCatalogWebService(), '/', conf)

    # Configura l'indirizzo e la porta del server
    cherrypy.config.update({'server.socket_host': '127.0.0.1'})  # Ascolta interfaccia locale
    cherrypy.config.update({'server.socket_port': 8080})  # Usa la porta 8080

    # Avvia il server CherryPy
    cherrypy.engine.start()
    # Mantiene il server attivo finché non viene terminato manualmente
    cherrypy.engine.block()
