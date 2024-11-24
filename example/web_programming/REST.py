import random  # Modulo per generare valori casuali
import string  # Modulo per manipolare stringhe
import cherrypy  # Framework per creare server web in Python
import os


# Definizione della classe principale che gestisce l'API REST
class StringGeneratorWebService(object):
    # Permette di esporre tutti i metodi HTTP (GET, POST, PUT, DELETE)
    exposed = True

    def GET(self, *path, **query):
        """
        Metodo HTTP GET: Mostra la stringa memorizzata nella sessione.
        """
        # Recupera la stringa salvata nella sessione (o usa un messaggio predefinito se non esiste)
        stored_string = cherrypy.session.get('mystring', 'No string stored yet!')
        print(f"GET: String retrieved from session: {stored_string}")  # Debug
        # Percorso al file HTML
        file_path = os.path.join(os.path.dirname(__file__), 'public', 'stored_string.html')
        # Legge il contenuto HTML e lo restituisce, sostituendo la stringa dinamicamente
        with open(file_path, 'r', encoding='utf-8') as file:
            html_content = file.read()
            return html_content.replace('{{ stored_string }}', stored_string)

    def POST(self, *path, **query):
        """
        Metodo HTTP POST: Genera una stringa casuale e la salva nella sessione.
        """
        # Ottiene la lunghezza della stringa dalla query string (default: 8)
        length = int(query.get('length', 8))
        # Genera una stringa casuale di caratteri esadecimali
        some_string = ''.join(random.sample(string.hexdigits, length))
        # Salva la stringa nella sessione
        cherrypy.session['mystring'] = some_string
        # Restituisce la stringa generata come risposta
        print(f"POST: String saved in session: {some_string}")  # Debug
        return some_string

    def PUT(self, *path, **query):
        """
        Metodo HTTP PUT: Aggiorna la stringa memorizzata nella sessione.
        """
        # Recupera il parametro 'another_string' o usa None
        new_string = query.get('another_string')
        if not new_string:
            # Se 'another_string' non è fornito, restituisci un messaggio di errore
            raise cherrypy.HTTPError(400, "Missing parameter 'another_string'")
        # Salva la nuova stringa nella sessione
        cherrypy.session['mystring'] = new_string
        print(f"PUT: String updated in session: {new_string}")  # Debug

    def DELETE(self, *path, **query):
        """
        Metodo HTTP DELETE: Elimina la stringa memorizzata nella sessione.
        """
        # Rimuove la stringa dalla sessione
        cherrypy.session.pop('mystring', None)


if __name__ == '__main__':
    # Configurazione del server CherryPy
    conf = {
        '/': {
            # Abilita il dispatcher per gestire i metodi HTTP (GET, POST, PUT, DELETE)
            'request.dispatch': cherrypy.dispatch.MethodDispatcher(),
            # Abilita le sessioni per memorizzare dati tra le richieste
            'tools.sessions.on': True,
        }
    }

    # Monta la classe StringGeneratorWebService alla radice del server
    cherrypy.tree.mount(StringGeneratorWebService(), '/', conf)

    # Configura l'indirizzo e la porta del server
    cherrypy.config.update({'server.socket_host': '127.0.0.1'})  # Ascolta interfaccia locale
    cherrypy.config.update({'server.socket_port': 8080})  # Usa la porta 8080

    # Avvia il server CherryPy
    cherrypy.engine.start()
    # Mantiene il server attivo finché non viene terminato manualmente
    cherrypy.engine.block()
