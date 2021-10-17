import functools
from os import error
from flask import Flask, render_template, blueprints, request, redirect, url_for, session, flash
from formularios import *
from werkzeug.security import check_password_hash, generate_password_hash
from db import get_db
from markupsafe import escape

main= blueprints.Blueprint('main', __name__)

def login_required(view):

    @functools.wraps(view)
    def wraped_view(**kwargs):
        if 'usuario' not in session:
            return redirect(url_for('main.login'))
        return view(**kwargs)
    
    return wraped_view

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
            db = get_db()
            consultabd = db.execute('select * from usuario where usuario = ?',(logusuario,)).fetchone()
            db.commit()
            db.close()
            sw = False
            if consultabd != None:
                logclave = logclave + logusuario #salt agregada
                sw = check_password_hash(consultabd[2], logclave)
                if (sw) == True:
                    session['usuario'] = consultabd[0]
                    session['nombre'] = consultabd[1]
                    session['tipousuario'] = consultabd[3]
                    session['boologeado'] = True
                    return redirect(url_for('main.profile')) 
        
        elif request.form.get("registrarse"): #Si el submit se activa con el botón de Registrarse
                regnombre = escape(request.form["regnombre"])
                regusuario = escape(request.form["regusuario"])
                regclave = escape(request.form["regclave"])
                tipousuario = "usuario"

                #Se hace hash a la clave
                regclave = regclave + regusuario #salt agregada
                regclave = generate_password_hash(regclave)                

                db = get_db()
                try:
                    db.execute("insert into usuario (usuario,nombre, clave, tipousuario) values( ?, ?, ?, ?)",(regusuario, regnombre, regclave, tipousuario))
                    db.commit()
                except Exception as e:
                    print('Exception: {}'.format(e))
                db.close()

                return redirect(url_for('main.profile')) 
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
@login_required
def profile():
    """Función que maneja el perfil de la página.
    """
    formedit = formeditar()
    return render_template('profile.html', formedit = formedit)

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

@main.route( '/logout/', methods = ['GET','POST'])
def logout():
    """Función que permite salir de la sesión.
    """
    session.clear()
    return redirect(url_for('main.home'))