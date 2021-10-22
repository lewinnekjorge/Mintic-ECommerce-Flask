import sqlite3
from sqlite3 import Error
from flask import current_app, g

def get_db():

    try:
        if 'db' not in g:
            
            g.db=sqlite3.connect('proyectoecommerce.db')
            print('conectada')
            return g.db
    except Error:
        print(Error)


def close_db():
    db = g.pop('db', None)

    if db is not None:
        db.close()

def statementosall(sql):
    #función que recibe la instrucción sql y retorna la consulta.
    db = get_db()
    try:
        consulta = db.execute(sql).fetchall()
        db.commit()
    except Exception as e:
        print('Exception: {}'.format(e))
    close_db()
    return (consulta)

def statementosmany(sql,ent):
    #función que recibe la instrucción sql y retorna la consulta.
    db = get_db()
    try:
        consulta = db.execute(sql).fetchmany(ent)
        db.commit()
    except Exception as e:
        print('Exception: {}'.format(e))
    close_db()
    return (consulta)

def statementosone(sql):
    #función que recibe la instrucción sql y retorna la consulta.
    db = get_db()
    try:
        consulta = db.execute(sql).fetchone()
        db.commit()
    except Exception as e:
        print('Exception: {}'.format(e))
    close_db()
    return (consulta)

def productclicked(variable):
    db = get_db()
    try:
        consulta = db.execute('select * from productos where id = ?',(variable,)).fetchone() #la coma es necesaria para que no se pase las palabras
    except Exception as e:
        print('Exception: {}'.format(e))
    close_db()
    return consulta