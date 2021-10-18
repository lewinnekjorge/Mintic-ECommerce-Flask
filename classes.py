class producto:
    def __init__(self, id, nombre, tipo, talla, precio, imagen):
        self.id = id
        self.nombre = nombre
        self.tipo = tipo
        self.talla = talla
        self.precio = precio
        self.imagen = imagen

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
        

