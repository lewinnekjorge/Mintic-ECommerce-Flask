class producto:
    def __init__(self, id, nombre, tipo, talla, precio):
        self.id = id
        self.nombre = nombre
        self.tipo = tipo
        self.talla = talla
        self.precio = precio

class carrito:
    def __init__(self, producto, cantidad):
        self.producto = producto
        self.cantidad = cantidad
        self.subtotal = producto.precio * cantidad
        self.linea = [producto, cantidad, self.subtotal]
        

