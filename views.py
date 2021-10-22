import functools
from os import error
from flask import Flask, render_template, blueprints, request, redirect, url_for, session, flash
from classes import *
from formularios import *
from werkzeug.security import check_password_hash, generate_password_hash
from db import get_db, productclicked, statementosall, statementosmany, statementosone
from markupsafe import escape

main= blueprints.Blueprint('main', __name__)

def login_required(view):

    @functools.wraps(view)
    def wraped_view(**kwargs):
        if 'usuario' not in session:
            return redirect(url_for('main.login'))
        return view(**kwargs)
    
    return wraped_view

def login_done(view):

    @functools.wraps(view)
    def wraped_view(**kwargs):
        if 'usuario' in session:
            return redirect(url_for('main.profile'))
        return view(**kwargs)
    
    return wraped_view

@main.route( '/' , methods = ['GET','POST'])
def home():
    """Función que maneja la raiz del sitio web.
    """
    consulta = statementosmany('select * from productos order by random()',4) #función inventada para reducir espacio
    misproductos = productosfromlista(consulta) #función inventada para crear vector de productos from lista
    print(misproductos)
    return render_template('index.html', misproductos=misproductos)

@main.route( '/login/', methods = ['GET','POST'])
@login_done
def login():
    """Función de prueba formularios wtf.
    """
    formlogin = formularioLogin()
    formregister = formularioRegistro()
    if request.method == 'POST':
        
        if request.form.get("enviar"): #Si el submit se activa con el botón de Iniciar Sesión
            if formlogin.validate_on_submit():
                logusuario = request.form['logusuario']
                logclave = request.form['logclave']
                db = get_db()
                consultabd = db.execute('select * from usuarios where usuario = ?',(logusuario,)).fetchone()
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
                        session['balance'] = consultabd[4]
                        session['boologeado'] = True
                        session['listadeseo'] = []
                        return redirect(url_for('main.profile'))
                else:
                    flash('Usuario o contraseña errados','errordelogin')
                    return redirect(url_for('main.login', error = error))
            
        elif request.form.get("registrarse"): #Si el submit se activa con el botón de Registrarse
            if formregister.validate_on_submit():
                regnombre = escape(request.form["regnombre"])
                regusuario = escape(request.form["regusuario"])
                regclave = escape(request.form["regclave"])
                tipousuario = "usuario"

                #Se hace hash a la clave
                regclave = regclave + regusuario #salt agregada
                regclave = generate_password_hash(regclave)                

                db = get_db()
                try:
                    db.execute("insert into usuarios (usuario,nombre, clave, tipousuario) values( ?, ?, ?, ?)",(regusuario, regnombre, regclave, tipousuario))
                    db.commit()
                except Exception as e:
                    print('Exception: {}'.format(e))
                db.close()
                flash('Su usuario ha sido registrado exitosamente')
                return redirect(url_for('main.login')) 
    return render_template('loginwtf.html', formlogin = formlogin, formregister = formregister)

@main.route( '/profile/', methods = ['GET','POST'])
@login_required
def profile():
    """Función que maneja el perfil de la página.
    """
    formedit = formeditar()
    if request.method == "POST":
        print("LO QUE SEAAAAAA")
        if request.form.get("guardar"):
            db = get_db()
            try:
                db.execute("update usuario set nombre = ? where usuarios = ?",(request.form['editnombre'], session['usuario'],))
                db.commit()
            except Exception as e:
                print('Exception: {}'.format(e))
            db.close()

    return render_template('profile.html', formedit = formedit)

@main.route( '/productos/', methods = ['GET','POST'])
def product():
    """Función de producto.
    """
    consulta2 = statementosall('select distinct tipo from productos')
    portipo = []
    productosportipo = []
    #for tipo in consulta2:
    #    tipos.append(tipo) #se obtienen los tipos de productos de la base de datos.
    db = get_db()
    for tipo in consulta2:
        try:
            consulta2 = db.execute('select * from productos where "tipo" = ? ',(tipo)).fetchall()
            db.commit()
        except Exception as e:
            print('Exception: {}'.format(e))
        portipo.append(consulta2)
    db.close()
    for tipo in portipo:
        auxiliar = productosfromlista(tipo) #obtengo lista de productos from lista de tipos
        productosportipo.append(auxiliar) #agrego todos los vectores en una sola matriz
    
    return render_template('product.html', productosportipo = productosportipo)

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

@main.route( '/wish/', methods = ['GET','POST'])
@login_required
def wish():
    """Función que maneja la lista de deseos
    """
    productoclickeado1 = producto(productclicked("1111"))
    item1 = itemcompra(productoclickeado1)
    listadeseo = []
    for i in range(0,3):
        listadeseo.append(item1)
    
    return render_template('wishlist.html', listadeseo = listadeseo)


@main.route( '/agregar/<variable>', methods = ['GET','POST'])
@login_required
def agregaralista(variable):
    """Función que maneja la lista de deseos
    """
    productoclickeado = producto(productclicked(variable))
    item = itemcompra(productoclickeado)
    try:
        listadeseo.append(item)
    except:
        listadeseo = []
        listadeseo.append(item)
    print(listadeseo)
    #session['lista']= []
    #session['lista'].append(productoclickeado)
    return '',204


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

@main.route( '/productos/<variable>', methods = ['GET'])
def detalleproducto(variable):
    """Función de prueba.
    """
    category = request.args.get('type')
    productoclickeado = producto(productclicked(variable)) #Método inventado en db.py para disminuir la cantidad de código en views.py
    return render_template('productdesc.html',product=productoclickeado)
