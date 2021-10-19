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
            self.id = args[0][0]
            self.nombre = args[0][1]
            self.tipo = args[0][2]
            self.talla = args[0][3]
            self.precio = args[0][4]
            self.img = args[0][5]

        
        if len(args)>1:
            if len(args[0])>1:
                pass


class itemcompra:
    def __init__(self, producto, cantidad):
        self.producto = producto
        self.cantidad = cantidad
        self.subtotal = producto.precio * cantidad
        self.linea = [producto, cantidad, self.subtotal]

class review:
    def __init__(self, producto, comentario, score):
        self.producto = producto
        self.comentario = comentario
        self.score = score
        

