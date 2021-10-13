from flask import Flask, render_template, blueprints, request, redirect, url_for
main= blueprints.Blueprint('main', __name__)

@main.route( '/' )
def home():
    """Función que maneja la raiz del sitio web.
    """
    return render_template('index.html')

@main.route( '/login/' )
def login():
    """Función que maneja la página de login y registro.
    """
    return render_template('login.html')

@main.route( '/prueba/' )
def prueba():
    """Función de prueba.
    """

    return render_template('prueba.html')

@main.route( '/cart/' )
def cart():
    """Función que maneja el carrito de compras.

    """

    return render_template('shoppingcart.html')

@main.route( '/contacto/' )
def contacto():
    """Función que maneja acerca de nosotros y contáctenos.

    """

    return render_template('contact.html')

@main.route( '/profile/' )
def profile():
    """Función que maneja el perfil de la página.
    """

    return render_template('profile.html')

@main.route( '/wish/' )
def wish():
    """Función que maneja la lista de deseos.

    """

    return render_template('wishlist.html')