import os
import cherrypy


class StringGenerator(object):
    @cherrypy.expose
    def index(self):
        # Costruisce il percorso assoluto al file index.html
        file_path = os.path.join(os.path.dirname(__file__), 'public/index.html')
        with open(file_path, 'r', encoding='utf-8') as file:
            return file.read()


if __name__ == '__main__':
    conf = {
        '/': {
            'tools.sessions.on': True,
            'tools.staticdir.root': os.path.abspath(os.getcwd())
        },
        '/static': {
            'tools.staticdir.on': True,
            'tools.staticdir.dir': './public'
        }
    }

    cherrypy.tree.mount(StringGenerator(), '/', conf)
    cherrypy.engine.start()
    cherrypy.engine.block()
