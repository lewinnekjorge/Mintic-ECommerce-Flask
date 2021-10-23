from classes import *

producto1 = producto(1,'camisa1','camisa','M',30000,'img')
producto2 = producto(1,'camisa2','camisa','L',50000,'img')
producto3 = producto(1,'pantalon1','pantalon','34',100000,'img')
listica = [(1,'camisa1','camisa','M',30000,'img'),(1,'camisa2','camisa','L',50000,'img')]
producto4 = producto(listica[0])

misproductos = productosfromlista(listica)

#print(type(listica[0]))

#for produco in misproductos:
#    print(produco.nombre)

ids = ['1113', '1112', '1111', '1112', '1112']

cadena = armarcadena(ids)

#newids = armarlista(ids)

print(cadena)


"""
itemcompra1 = itemcompra(producto1,2)
itemcompra2 = itemcompra(producto2,1)

vectorlistadedeseo = []
vectorlistadedeseo.append(itemcompra2)

vectorcarritodecompras =[]
vectorcarritodecompras.append(itemcompra1)
vectorcarritodecompras.append(itemcompra2)

for item in vectorlistadedeseo:
    vectorcarritodecompras.append(item)

vectorcarritodecompras = [itemcompra1,itemcompra2]

total = itemcompra1.subtotal + itemcompra2.subtotal
print(total)

cal1 = review(producto1, 'Me gustó mucho', 5)

print(cal1.producto.nombre, ' ', cal1.comentario)

"""