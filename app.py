from flask import Flask

def create_app():
    """Función que crea la aplicación principal. 
    """
    app = Flask(__name__)

    app.secret_key = 'misiontic2022'

    from views import main
    app.register_blueprint(main)
    return app

app = create_app()
if __name__ == "__main__":
    app.run(debug=True)