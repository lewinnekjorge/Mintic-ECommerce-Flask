from typing import Any
from flask import Flask, render_template, blueprints, request, redirect, url_for
main= blueprints.Blueprint('main', __name__)

@main.route( '/' )
def home():
    """Función que maneja la raiz del sitio web.
    """
    return render_template('index.html')

@main.route( '/login/', methods = ['GET','POST'])
def login():
    """Función que maneja la página de login y registro.
    """
    if request.method == 'POST':
        if request.form.get("iniciosesion"):
            if (request.form['username'] == 'usuario1') & (request.form['password'] == "prueba1"):
                return render_template('profile.html')
        elif request.form.get("registrate"):
            if (request.form["form-usuario"] != "") | (request.form["form-password"]!= ""):
                newuser = request.form["form-usuario"]
                newpass = request.form["form-password"]
                return newuser +" "+ newpass

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