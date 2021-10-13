from flask import Flask

def create_app():
    """Función que crea la aplicación principal. 
    """
    app = Flask(__name__)

    from views import main
    app.register_blueprint(main)
    return app 