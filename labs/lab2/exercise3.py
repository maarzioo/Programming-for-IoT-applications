import json

import cherrypy  # Framework per creare server web in Python
import os
from labs.lab1.exercise2 import Calculator


# Definizione della classe principale che gestisce l'API REST
class CalculatorWebService(object):
    # Permette di esporre tutti i metodi HTTP (GET, POST, PUT, DELETE)
    exposed = True
    calculator = Calculator()

    def GET(self, *path, **query):
        raise NotImplementedError

    def POST(self, *path, **query):
        return NotImplementedError

    def PUT(self, *path, **query):
        """
        Metodo HTTP PUT: Riceve un JSON nel corpo della richiesta,
        esegue l'operazione richiesta e restituisce un JSON con il risultato.
        """

        # Leggi il corpo della richiesta
        body = cherrypy.request.body.read()
        data = json.loads(body)  # Carica il JSON come dizionario

        # Recupera il comando e gli operandi
        command = data['command']
        operands = data['operands']

        # Esegui l'operazione richiesta
        if command == "add":
            result = self.calculator.add(operands)
        elif command == "sub":
            result = self.calculator.subtract(operands)
        elif command == "mul":
            result = self.calculator.multiply(operands)
        elif command == "div":
            result = self.calculator.divide(operands)
        else:
            raise ValueError(f"Unsupported command: {command}")

        # Percorso al file HTML
        html_path = os.path.join(os.path.dirname(__file__), 'public', 'result.html')
        with open(html_path, 'r', encoding='utf-8') as file:
            html_content = file.read()

        # Sostituzione dinamica dei segnaposto
        html_content = html_content.replace('{{ result }}', str(result))

        return html_content

    def DELETE(self, *path, **query):
        return NotImplementedError


if __name__ == '__main__':
    # Configurazione del server CherryPy
    conf = {
        '/': {
            # Abilita il dispatcher per gestire i metodi HTTP (GET, POST, PUT, DELETE)
            'request.dispatch': cherrypy.dispatch.MethodDispatcher()
        }
    }

    # Monta la classe StringGeneratorWebService alla radice del server
    cherrypy.tree.mount(CalculatorWebService(), '/', conf)

    # Configura l'indirizzo e la porta del server
    cherrypy.config.update({'server.socket_host': '127.0.0.1'})  # Ascolta interfaccia locale
    cherrypy.config.update({'server.socket_port': 8080})  # Usa la porta 8080

    # Avvia il server CherryPy
    cherrypy.engine.start()
    # Mantiene il server attivo finché non viene terminato manualmente
    cherrypy.engine.block()
