def asignaciones(args,fila):
        id = args[fila][0]
        nombre = args[fila][1]
        tipo = args[fila][2]
        talla = args[fila][3]
        precio = args[fila][4]
        img = args[fila][5]
        return (id, nombre, tipo, talla, precio, img)

def productosfromlista(listica):
    misproductos = []
    if isinstance(listica,list): #Para saber si recibo una lista de productos
        for vector in listica:
            iteracion = producto(vector)
            misproductos.append(iteracion)
    else:
        pass
    return misproductos

class producto:
    def __init__(self, *args): # id, nombre, tipo, talla, precio
        if len(args) == 5:
            self.id = args[0]
            self.nombre = args[1]
            self.tipo = args[2]
            self.talla = args[3]
            self.precio = args[4]
            self.img = args[5]
    
        if len(args) == 1:
            self.id,self.nombre, self.tipo, self.talla, self.precio, self.img = asignaciones(args,0)


class itemcompra:
    def __init__(self, producto):
        self.producto = producto
        cantidad = 1
        self.cantidad = cantidad
        self.subtotal = producto.precio * cantidad
        self.linea = [producto, cantidad, self.subtotal]

class review:
    def __init__(self, producto, comentario, score):
        self.producto = producto
        self.comentario = comentario
        self.score = score
        

def armarlista(ids):
    ids = str(ids)
    newids = ids.split(',')
    return newids

def armarcadena(lista):
    cadena = ",".join(lista)
    return cadena
