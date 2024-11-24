import cherrypy
import os


class Generator:
    # Metodo per gestire la pagina principale del form
    @cherrypy.expose
    def hello(self):
        # Restituisce il contenuto di hello_form.html
        file_path = os.path.join(os.path.dirname(__file__), 'public/hello_form.html')
        return open(file_path, 'r').read()

    # Metodo per gestire la pagina di risposta
    @cherrypy.expose
    def reply(self, *uri, **params):
        # Restituisce il contenuto di page.html
        file_path = os.path.join(os.path.dirname(__file__), 'public/page.html')
        return open(file_path, 'r').read()


if __name__ == '__main__':
    # Configura l'applicazione web con cherrypy
    cherrypy.tree.mount(Generator(), '/')
    cherrypy.engine.start()
    cherrypy.engine.block()
