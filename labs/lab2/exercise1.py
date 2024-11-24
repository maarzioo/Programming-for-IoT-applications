import json
import cherrypy  # Framework per creare server web in Python
from labs.lab1.exercise1 import Calculator

"""Codice Server"""


# Definizione della classe principale che gestisce l'API REST
class CalculatorWebService(object):
    # Permette di esporre tutti i metodi HTTP (GET, POST, PUT, DELETE)
    exposed = True
    calculator = Calculator()

    def GET(self, *path, **query):
        """
        Metodo HTTP GET: Mostra il risultato dell'operazione.
        """
        operation = path[0]
        op1, op2 = float(query['op1']), float(query['op2'])

        if operation == "add":
            result = self.calculator.add(op1, op2)
        elif operation == "sub":
            result = self.calculator.subtract(op1, op2)
        elif operation == "mul":
            result = self.calculator.multiply(op1, op2)
        elif operation == "div":
            result = self.calculator.divide(op1, op2)

        # # Percorso al file HTML
        # html_path = os.path.join(os.path.dirname(__file__), 'public', 'result.html')
        # with open(html_path, 'r', encoding='utf-8') as file:
        #     html_content = file.read()
        #
        # # Sostituzione dinamica dei segnaposto
        # html_content = html_content.replace('{{ result }}', str(result))
        # return html content

        cherrypy.response.headers['Content-Type'] = 'application/json'
        return json.dumps(result).encode('utf-8')

    def POST(self, *path, **query):
        return NotImplementedError

    def PUT(self, *path, **query):
        return NotImplementedError

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
