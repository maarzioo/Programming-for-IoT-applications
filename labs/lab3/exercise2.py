import cherrypy
import json
from datetime import datetime
import os


class DeviceCatalog:
    exposed = True

    def __init__(self):
        self.catalog_file = os.path.join(os.path.dirname(__file__), 'catalog.json')
        self.load_catalog()

    def load_catalog(self):
        with open(self.catalog_file, 'r') as file:
            self.catalog_data = json.load(file)

    def save_catalog(self):
        with open(self.catalog_file, 'w') as file:
            json.dump(self.catalog_data, file, indent=4)

    @cherrypy.tools.json_out()
    def GET(self, *path, **query):
        """
        Gestisce le richieste GET per operazioni di ricerca.
        """
        if len(path) == 0:
            raise cherrypy.HTTPError(400, "Missing operation in the URL.")

        operation = path[0]
        if operation == "searchByName":
            name = query.get("name")
            if not name:
                raise cherrypy.HTTPError(400, "Missing 'name' parameter.")
            return [device for device in self.catalog_data["devicesList"] if device["deviceName"] == name]

        elif operation == "searchByID":
            device_id = query.get("id")
            if not device_id:
                raise cherrypy.HTTPError(400, "Missing 'id' parameter.")
            try:
                device_id = int(device_id)  # Converte il parametro in un intero
            except ValueError:
                raise cherrypy.HTTPError(400, "Invalid 'id' parameter. Must be an integer.")
            return next((device for device in self.catalog_data["devicesList"] if device["deviceID"] == device_id), {})

        elif operation == "searchByService":
            service = query.get("service")
            if not service:
                raise cherrypy.HTTPError(400, "Missing 'service' parameter.")
            return [device for device in self.catalog_data["devicesList"] if service in device.get("availableServices", [])]

        elif operation == "searchByMeasureType":
            measure_type = query.get("measureType")
            if not measure_type:
                raise cherrypy.HTTPError(400, "Missing 'measureType' parameter.")
            return [device for device in self.catalog_data["devicesList"] if measure_type in device.get("measureType", [])]

        elif operation == "printAll":
            return self.catalog_data

        else:
            raise cherrypy.HTTPError(400, f"Unknown operation: {operation}")

    @cherrypy.tools.json_in()
    @cherrypy.tools.json_out()
    def POST(self, *path, **query):
        """
        Gestisce le richieste POST per aggiungere o aggiornare un dispositivo.
        """
        if len(path) == 0 or path[0] != "insertDevice":
            raise cherrypy.HTTPError(400, "Unknown operation for POST.")

        input_data = cherrypy.request.json
        if not input_data or "deviceID" not in input_data:
            raise cherrypy.HTTPError(400, "Invalid input. Missing 'deviceID'.")

        # Verifica se il dispositivo esiste
        existing_device = next((device for device in self.catalog_data["devicesList"] if device["deviceID"] == input_data["deviceID"]), None)
        if existing_device:
            # Aggiorna il dispositivo esistente
            existing_device.update(input_data)
            existing_device["lastUpdate"] = datetime.now().strftime("%Y-%m-%d %H:%M")
            return {"message": "Device updated successfully."}
        else:
            # Aggiungi un nuovo dispositivo
            input_data["lastUpdate"] = datetime.now().strftime("%Y-%m-%d %H:%M")
            self.catalog_data["devicesList"].append(input_data)
            self.save_catalog()
            return {"message": "New device added successfully."}

    def PUT(self, *path, **query):
        raise cherrypy.HTTPError(405, "PUT method is not supported.")

    def DELETE(self, *path, **query):
        raise cherrypy.HTTPError(405, "DELETE method is not supported.")


if __name__ == "__main__":
    # Configurazione del server
    config = {
        '/': {
            'request.dispatch': cherrypy.dispatch.MethodDispatcher(),
            'tools.json_out.on': True,
            'tools.json_in.on': True,
        }
    }
    cherrypy.tree.mount(DeviceCatalog(), '/', config)

    cherrypy.config.update({
        'server.socket_host': '127.0.0.1',
        'server.socket_port': 8080,
        'log.screen': True
    })

    print("Starting the Device Catalog RESTful Service...")
    cherrypy.engine.start()
    cherrypy.engine.block()
