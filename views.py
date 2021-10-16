from flask import Flask, render_template, blueprints, request, redirect, url_for
from formularios import *
from werkzeug.security import check_password_hash, generate_password_hash
from db import get_db
from markupsafe import escape

main= blueprints.Blueprint('main', __name__)

@main.route( '/' , methods = ['GET','POST'])
def home():
    """Función que maneja la raiz del sitio web.
    """
    return render_template('index.html')

@main.route( '/login/', methods = ['GET','POST'])
def login():
    """Función de prueba formularios wtf.
    """
    formlogin = formularioLogin()
    formregister = formularioRegistro()
    if request.method == 'POST':
        if request.form.get("enviar"): #Si el submit se activa con el botón de Iniciar Sesión
            logusuario = request.form['logusuario']
            logclave = request.form['logclave']

            if (logusuario == 'usuario1') & (logclave == "prueba1"):
                return redirect(url_for('main.profile'))

        
        elif request.form.get("registrarse"): #Si el submit se activa con el botón de Registrarse
                regnombre = escape(request.form["regnombre"])
                regusuario = escape(request.form["regusuario"])
                regclave = escape(request.form["regclave"])

                #Se hace hash a la clave
                regclave = regclave + regusuario #salt agregada
                regclave = generate_password_hash(regclave)                

                #db = get_db()
                #db.execute("insert into usuario ( nombre, usuario, clave) values( ?, ?, ?)",(regnombre, regusuario, regclave))
                #db.commit()
                #db.close()

                return regusuario +" "+ regclave
    return render_template('loginwtf.html', formlogin = formlogin, formregister = formregister)


@main.route( '/productos/', methods = ['GET','POST'])
def product():
    """Función de producto.
    """

    return render_template('product.html')

@main.route( '/cart/', methods = ['GET','POST'])
def cart():
    """Función que maneja el carrito de compras.

    """

    return render_template('shoppingcart.html')

@main.route( '/contacto/', methods = ['GET','POST'])
def contacto():
    """Función que maneja acerca de nosotros y contáctenos.

    """

    return render_template('contact.html')

@main.route( '/profile/', methods = ['GET','POST'])
def profile():
    """Función que maneja el perfil de la página.
    """

    return render_template('profile.html')

@main.route( '/wish/', methods = ['GET','POST'])
def wish():
    """Función que maneja la lista de deseos

    """

    return render_template('wishlist.html')

@main.route( '/calificacion/', methods = ['GET','POST'])
def calificacion():
    """Función que  maneja las páginas de las calificaciones.
    """

    return render_template('calificaciones.html')

#@main.route( '/login/', methods = ['GET','POST'])
#def login():
#    """Función que maneja la página de login y registro.
#
#        Aquí se capturan los datos de los formularios y realiza el acceso al usuario o se
#        reciben los datos de registro que luego serán enviados a la BD.
#    """
#    if request.method == 'POST':
#        if request.form.get("iniciosesion"):
#            if (request.form['username'] == 'usuario1') & (request.form['password'] == "prueba1"):
#                return redirect(url_for('main.profile'))
#        elif request.form.get("registrate"):
#            if (request.form["form-usuario"] != "") | (request.form["form-password"]!= ""):
#                newuser = request.form["form-usuario"]
#                newpass = request.form["form-password"]
#                return newuser +" "+ newpass
#
#    return render_template('login.html')