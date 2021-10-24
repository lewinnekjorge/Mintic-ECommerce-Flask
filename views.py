import functools
from os import error
from flask import Flask, render_template, blueprints, request, redirect, url_for, session, flash
from classes import *
from formularios import *
from werkzeug.security import check_password_hash, generate_password_hash
from db import *
from markupsafe import escape
import sqlite3

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
                close_db()
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
                balance = 0
                print(regusuario,regclave)
                #Se hace hash a la clave
                regclave = regclave + regusuario #salt agregada
                regclave = generate_password_hash(regclave)                

                db = get_db()
                try:
                    db.execute("insert into usuarios (usuario,nombre, clave, tipousuario,balance) values( ?, ?, ?, ?, ?)",(regusuario, regnombre, regclave, tipousuario,balance))
                    db.commit()
                except Exception as e:
                    print('Exception: {}'.format(e))
                close_db()
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
            close_db()

    return render_template('profile.html', formedit = formedit)

@main.route( '/productos/', methods = ['GET'])
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
    close_db()
    for tipo in portipo:
        auxiliar = productosfromlista(tipo) #obtengo lista de productos from lista de tipos
        productosportipo.append(auxiliar) #agrego todos los vectores en una sola matriz
    
    return render_template('product.html', productosportipo = productosportipo)

@main.route( '/cart/', methods = ['GET','POST'])
def cart():
    """Función que maneja el carrito de compras.
    """
    carrito = []
    total = 0
    db = get_db()
    try:
        consulta = db.execute('select carrito from usuarios where usuario = ?',(session['usuario'],)).fetchall()
        db.commit()
    except Exception as e:
        print('Exception: {}'.format(e))
    close_db()
    if consulta[0][0] != None:
        newids = armarlista(consulta[0][0]) #Se debe tomar el primer valor del primer vector de la consulta
        for ids in newids:
            productoclickeado = producto(productclicked(ids))
            total = total + float(productoclickeado.precio)
            item = itemcompra(productoclickeado)
            carrito.append(item)
    if total == 0:
        totaldomi = 0
    else:
        totaldomi = total + 10000
    return render_template('shoppingcart.html', carrito = carrito, total = total, totaldomi=totaldomi)

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
    listadeseo = []
    db = get_db()
    try:
        consulta = db.execute('select listadeseo from usuarios where usuario = ?',(session['usuario'],)).fetchall()
        db.commit()
    except Exception as e:
        print('Exception: {}'.format(e))
    close_db()
    if consulta[0][0] != None:
        newids = armarlista(consulta[0][0]) #Se debe tomar el primer valor del primer vector de la consulta
        for ids in newids:
            productoclickeado = producto(productclicked(ids))
            item = itemcompra(productoclickeado)
            listadeseo.append(item)
    
    
    return render_template('wishlist.html', listadeseo = listadeseo)

@main.route( '/wish/enviaracarrito', methods = ['GET','POST'])
@login_required
def enviaracarrito():
    """Función que envia la lista de deseos al carrito
    """
    db = get_db()
    try:
        vlistadeseo = db.execute('select listadeseo from usuarios where usuario = ?',(session['usuario'],)).fetchone()
        db.commit()
    except Exception as e:
        print('Exception: {}'.format(e))
    close_db()
    print(vlistadeseo[0]==None)
    if (vlistadeseo[0] != None):
        print('ENTRO AQUI')
        db = get_db()
        try:
            db.execute('update usuarios set carrito = COALESCE(carrito||",","") || listadeseo where usuario = ?',(session['usuario'],)).fetchall()
            db.execute('update usuarios set listadeseo = NULL where usuario = ?',(session['usuario'],)).fetchall()
            db.commit()
        except Exception as e:
            print('Exception: {}'.format(e))
        close_db()
    return redirect(url_for('main.cart'))

@main.route( '/cart/<variable>', methods = ['GET','POST'])
@login_required
def agregaracarro(variable):
    """Función que permite agregar productos al carrito
    """
    db = get_db()
    try:
        consulta = db.execute('select carrito from usuarios where usuario = ?',(session['usuario'],)).fetchall()
        db.commit()
    except Exception as e:
        print('Exception: {}'.format(e))
    close_db()
    if consulta[0][0] is None:
        idslistadeseo = [variable]
    else:
        idslistadeseo=armarlista(consulta[0][0])
        idslistadeseo.append(variable)
    idsguardar = armarcadena(idslistadeseo)
    db = get_db()
    try:
        consulta = db.execute('update usuarios set carrito = ? where usuario = ?;',(idsguardar,session['usuario'],)).fetchall()
        db.commit()
    except Exception as e:
        print('Exception: {}'.format(e))
    close_db()    
    
    #session['lista']= []
    #session['lista'].append(productoclickeado)
    return '',204

@main.route( '/cart/borrar/<variable>', methods = ['GET','POST'])
@login_required
def eliminarcarro(variable):
    """Función que permite eliminar productos del carrito de compras
    """
    db = get_db()
    try:
        consulta = db.execute('select carrito from usuarios where usuario = ?',(session['usuario'],)).fetchall()
        db.commit()
    except Exception as e:
        print('Exception: {}'.format(e))
    close_db()
    idscarro=armarlista(consulta[0][0])
    idscarro.remove(variable)
    if len(idscarro) == 0:
        idsguardar = None
    else:
        idsguardar = armarcadena(idscarro)
    
    db = get_db()
    try:
        consulta = db.execute('update usuarios set carrito = ? where usuario = ?;',(idsguardar,session['usuario'],)).fetchall()
        db.commit()
    except Exception as e:
        print('Exception: {}'.format(e))
    close_db()    
    
    return '',204

@main.route( '/wish/borrar/<variable>', methods = ['GET','POST'])
@login_required
def eliminarlistadeseo(variable):
    """Función que permite eliminar productos del carrito de compras
    """
    db = get_db()
    try:
        consulta = db.execute('select listadeseo from usuarios where usuario = ?',(session['usuario'],)).fetchall()
        db.commit()
    except Exception as e:
        print('Exception: {}'.format(e))
    close_db()
    idslista=armarlista(consulta[0][0])
    idslista.remove(variable)
    if len(idslista) == 0:
        idsguardar = None
    else:
        idsguardar = armarcadena(idslista)
    
    db = get_db()
    try:
        consulta = db.execute('update usuarios set listadeseo = ? where usuario = ?;',(idsguardar,session['usuario'],)).fetchall()
        db.commit()
    except Exception as e:
        print('Exception: {}'.format(e))
    close_db()    
    
    return '',204

@main.route( '/cart/comprar/<variable>', methods = ['GET','POST'])
@login_required
def comprar(variable):
    """Método para completar la compra de los productos
    """
    db = get_db()
    try:
        consulta = db.execute('select carrito, balance from usuarios where usuario = ?',(session['usuario'],)).fetchall()
        db.commit()
    except Exception as e:
        print('Exception: {}'.format(e))
    close_db()
    idscompra=armarlista(consulta[0][0]) #id de productos comprados para procesos no implementados
    balance = consulta[0][1]
    idsguardar = None
    print(balance)
    print(idscompra)
    print(variable)
    db = get_db()
    try:
        consulta = db.execute('update usuarios set carrito = ? where usuario = ?;',(idsguardar,session['usuario'],)).fetchall()
        db.commit()
    except Exception as e:
        print('Exception: {}'.format(e))
    close_db()    
    
    return '',204

@main.route( '/agregar/<variable>', methods = ['GET','POST'])
@login_required
def agregaralista(variable):
    """Función que permite agregar productos a lista de deseos
    """
    db = get_db()
    try:
        consulta = db.execute('select listadeseo from usuarios where usuario = ?',(session['usuario'],)).fetchall()
        db.commit()
    except Exception as e:
        print('Exception: {}'.format(e))
    close_db()
    if consulta[0][0] is None:
        idslistadeseo = [variable]
    else:
        idslistadeseo=armarlista(consulta[0][0])
        idslistadeseo.append(variable)
    idsguardar = armarcadena(idslistadeseo)
    db = get_db()
    try:
        consulta = db.execute('update usuarios set listadeseo = ? where usuario = ?;',(idsguardar,session['usuario'],)).fetchall()
        db.commit()
    except Exception as e:
        print('Exception: {}'.format(e))
    close_db()    
    
    #session['lista']= []
    #session['lista'].append(productoclickeado)
    return '',204

@main.route( '/calificacion/', methods = ['GET','POST'])
def calificacion():
    """Función que  maneja las páginas de las calificaciones.
    """
    

    return render_template('calificaciones.html')

@main.route( '/logout/', methods = ['GET'])
def logout():
    """Función que permite salir de la sesión.
    """
    session.clear()
    return redirect(url_for('main.home'))

@main.route( '/productos/<variable>', methods = ['GET','POST'])
def detalleproducto(variable):
    """Función de prueba.
    """
    category = request.args.get('type')
    productoclickeado = producto(productclicked(variable)) #Método inventado en db.py para disminuir la cantidad de código en views.py
    return render_template('productdesc.html',product=productoclickeado)
