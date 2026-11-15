import sqlite3 as sql
from colorama import init, Fore, Style
init(autoreset=True)

def encabezado(): #Creamos la función encabezado. Usamos color verde con Colorama para resaltar el texto. 
    print(Fore.GREEN + "*"*46) #al agregar FORE GREEN, el texto se vera en verde. El *46 es para crear una línea de separación
    print(Fore.GREEN + "Bienvenido al programa de gestion de productos")
    print(Fore.GREEN + "                MENU PRINCIPAL")
    print(Fore.GREEN + "*"*46)

def crear_base_datos():
        conexion = sql.connect("inventario.db")
        conexion.commit()
        print("Base de datos creada con éxito")
        conexion.close()

def crear_tabla():
    conexion = sql.connect("inventario.db")
    cursor = conexion.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS productos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL,
            descripcion TEXT,
            cantidad INTEGER NOT NULL,
            precio REAL NOT NULL,
            categoria TEXT
        )
    """)
    print(Fore.GREEN +"Tabla productos fue creada con éxito") #imprimimos un mensaje de éxito
    conexion.commit()
    conexion.close()

  

def registrar_producto():
    conexion = sql.connect("inventario.db") #establecemos la conexión con la base de datos productos.db
    cursor = conexion.cursor() #creamos un cursor para ejecutar comandos SQL
    print("\n--- Registrar nuevo producto ---")
    nombre = input ("Ingrese el nombre del producto: ") #solicitamos al usuario el nombre del producto
    while nombre == "": #validamos que el nombre del producto no esté vacío
        print("El nombre del producto no puede estar vacio") #imprimimos un mensaje de error
        nombre = input ("Ingrese el nombre del producto: ") #solicitamos al usuario el nombre del producto
    descripcion = input ("Ingrese la descripcion del producto: ") #solicitamos al usuario la descripcion del producto
    while descripcion == "": #validamos que la descripcion del producto no esté vacío
        print("La descripcion del producto no puede estar vacia") #imprimimos un mensaje de error
        descripcion = input ("Ingrese la descripcion del producto: ") #solicitamos al usuario la descripcion del producto
    while True:
        try:
            cantidad_str = input ("Ingrese la cantidad del producto: ") #solicitamos al usuario la cantidad del producto
            if not cantidad_str.isdigit():  #validamos que la cantidad del producto sea un número
             raise ValueError("La cantidad del producto debe ser un número entero") #imprimimos un mensaje de error
            cantidad = int(cantidad_str)
            break
        except ValueError as e:
            print(Fore.RED + e)
    
    while True:
        try:
            precio_str = input ("Ingrese el precio del producto (utiliza '.' como separador decimal): ") #solicitamos al usuario el precio del producto
            precio_str = precio_str.replace(",",".")  #validamos que acepte separadores decimales 
            if not precio_str.replace(".","").isdigit() or float(precio_str) < 0:
             raise ValueError("El precio del producto debe ser un número positivo") #imprimimos un mensaje de error
            precio = float(precio_str)
            break
        except ValueError as e:
            print(Fore.RED + e)
                
    categoria = input ("Ingrese la categoria del producto: ") #solicitamos al usuario la categoria del producto
    while categoria == "": #validamos que la categoria del producto no esté vacío
        print(Fore.RED + "La categoria del producto no puede estar vacia") #imprimimos un mensaje de error
        categoria = input ("Ingrese la categoria del producto: ") #solicitamos al usuario la categoria del producto
    cursor.execute ('''
    INSERT INTO productos (nombre,descripcion,cantidad, precio,categoria)
    VALUES (?, ?, ?, ?, ?)''', (nombre, descripcion, cantidad, precio, categoria)) #insertamos producto y sus campos en la tabla productos
    print(f"Producto: {nombre} {descripcion} {cantidad} {precio} {categoria} registrado con éxito") #imprimimos un mensaje de éxito
    conexion.commit() #confirmamos eventual cambios en la base de datos  
    conexion.close() #cerramos la conexión con la base de datos


def mostrar_producto(producto):
    print(Fore.GREEN +"Productos registrados:") #imprimimos un mensaje de éxito
    print("ID:", producto[0])
    print("Nombre:", producto[1])
    print("Descripción:", producto[2])
    print("Cantidad:", producto[3])
    print("Precio: $", producto[4])
    print("Categoría:", producto[5])
    print(Fore.GREEN + "-" * 30)

def mostrar_productos():
    print("\n Lista de productos registrados ")
    conexion = sql.connect("inventario.db")
    cursor = conexion.cursor ()
    cursor.execute("SELECT * FROM productos")
    productos = cursor.fetchall()

    if len(productos) == 0:
        print("No hay productos registrados.")
    else:
        for producto in productos:
            mostrar_producto(producto)

    conexion.close()

def actualizar_producto():
    print("\n--- Actualizar producto ---")
    id_producto = int(input("Ingrese el ID del producto a actualizar: "))

    conexion = sql.connect("inventario.db")
    cursor = conexion.cursor()

    cursor.execute("SELECT * FROM productos WHERE id = ?", (id_producto,))
    producto = cursor.fetchone()

    if producto is None:
        print("No existe un producto con ese ID.")
    else:
        print("Datos actuales:")
        mostrar_producto(producto)

        print("Ingrese los nuevos datos:")
        nombre = input("Nombre: ")
        descripcion = input("Descripción: ")
        cantidad = int(input("Cantidad: "))
        precio = float(input("Precio: "))
        categoria = input("Categoría: ")

        cursor.execute(
            "UPDATE productos SET nombre = ?, descripcion = ?, cantidad = ?, precio = ?, categoria = ? WHERE id = ?",
            (nombre, descripcion, cantidad, precio, categoria, id_producto)
        )
        conexion.commit()
        print("Producto actualizado correctamente.")

    conexion.close()

def eliminar_producto():
    print("\n--- Eliminar producto ---")
    id_producto = int(input("Ingrese el ID del producto a eliminar: "))

    conexion = sql.connect("inventario.db")
    cursor = conexion.cursor()

    cursor.execute("SELECT * FROM productos WHERE id = ?", (id_producto,))
    producto = cursor.fetchone()

    if producto is None:
        print("No existe un producto con ese ID.")
    else:
        cursor.execute("DELETE FROM productos WHERE id = ?", (id_producto,))
        conexion.commit()
        print("Producto eliminado correctamente.")

    conexion.close()

def buscar_producto():
    print("\n--- Buscar producto ---")
    id_producto = int(input("Ingrese el ID del producto a buscar: "))

    conexion = sql.connect("inventario.db")
    cursor = conexion.cursor()

    cursor.execute("SELECT * FROM productos WHERE id = ?", (id_producto,))
    producto = cursor.fetchone()
    conexion.close()

    if producto is None:
        print("No se encontró ningún producto con ese ID.")
    else:
        mostrar_producto(producto)

def reporte_bajo_stock():
    print("\n--- Reporte de bajo stock ---")
    limite = int(input("Mostrar productos con cantidad igual o menor a: "))

    conexion = sql.connect("inventario.db")
    cursor = conexion.cursor()

    cursor.execute("SELECT * FROM productos WHERE cantidad <= ?", (limite,))
    productos = cursor.fetchall()
    conexion.close()

    if len(productos) == 0:
        print("No hay productos con cantidad igual o menor a", limite)
    else:
        for producto in productos:
            mostrar_producto(producto)

def mostrar_menu():
    
    print("1. Registrar producto")
    print("2. Mostrar productos registrados")
    print("3. Actualizar producto")
    print("4. Eliminar producto")
    print("5. Buscar producto por ID")
    print("6. Reporte de bajo stock")
    print("7. Salir")


def main():
    encabezado()
    crear_tabla()

    while True:
        mostrar_menu()
        
        opcion = input("Selecciona una opcion (1 al 6 o '7' para salir): ").strip().upper()
        while opcion == "":
            print("Opcion no valida.")
            opcion = input("Selecciona una opcion (1-6 o'7' para salir): ").strip().upper()

        if opcion == "1":
            registrar_producto()
        elif opcion == "2":
            mostrar_productos()
        elif opcion == "3":
            actualizar_producto()
        elif opcion == "4":
            eliminar_producto()
        elif opcion == "5":
            buscar_producto()
        elif opcion == "6":
            reporte_bajo_stock()
        elif opcion == "7":
            print("Muchas gracias por usar el programa")
            break
        else:
            print("opcion no valida")
# encabezado()
main()