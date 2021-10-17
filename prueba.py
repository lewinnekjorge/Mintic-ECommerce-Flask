from classes import *

producto1 = producto(1,'camisa1','camisa','M',30000)
producto2 = producto(1,'camisa2','camisa','L',50000)
producto3 = producto(1,'pantalon1','pantalon','34',100000)

carroprueba = carrito(producto1,2)
print(carroprueba.producto.nombre, ' ', carroprueba.cantidad, ' ',carroprueba.subtotal)
