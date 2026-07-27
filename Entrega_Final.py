import sqlite3

# ======================================================
# FUNCIÓN: Conecta a la base de datos inventario.db
# ======================================================
def crear_conexion():
    try:
        conexion = sqlite3.connect("inventario.db")
        return conexion
    except sqlite3.Error as e:
        print("Error al conectar:", e)
        return None


# ======================================================
# FUNCIÓN: Crea la tabla con TODOS los campos obligatorios
# ======================================================
def crear_tabla():
    conexion = crear_conexion()
    cursor = conexion.cursor()

    sql = """
    CREATE TABLE IF NOT EXISTS productos (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nombre TEXT NOT NULL,
        descripcion TEXT,
        cantidad INTEGER NOT NULL,
        precio REAL NOT NULL,
        categoria TEXT
    );
    """

    try:
        cursor.execute(sql)
        conexion.commit()
    except sqlite3.Error as e:
        print("Error al crear la tabla:", e)
    finally:
        conexion.close()


# ======================================================
# AGREGAR PRODUCTO
# ======================================================
def agregar_producto():
    print("=== AGREGAR PRODUCTO ===")

    nombre = input("Nombre: ").strip()
    descripcion = input("Descripción: ").strip()
    cantidad = input("Cantidad: ").strip()
    precio = input("Precio: ").strip()
    categoria = input("Categoría: ").strip()

    if not nombre or not cantidad or not precio:
        print("Error: Nombre, cantidad y precio son obligatorios.")
        return

    # Validar cantidad
    if not cantidad.isdigit():
        print("La cantidad debe ser un número entero.")
        return
    cantidad = int(cantidad)

    # Validar precio
    try:
        precio = float(precio)
    except:
        print("El precio debe ser un número.")
        return

    conexion = crear_conexion()
    cursor = conexion.cursor()

    sql = """
    INSERT INTO productos (nombre, descripcion, cantidad, precio, categoria)
    VALUES (?, ?, ?, ?, ?)
    """

    try:
        cursor.execute(sql, (nombre, descripcion, cantidad, precio, categoria))
        conexion.commit()
        print("Producto agregado correctamente.")
    except sqlite3.Error as e:
        print("Error al agregar producto:", e)
    finally:
        conexion.close()


# ======================================================
# MOSTRAR PRODUCTOS
# ======================================================
def mostrar_productos():
    print("=== LISTA DE PRODUCTOS ===")

    conexion = crear_conexion()
    cursor = conexion.cursor()

    sql = "SELECT * FROM productos"

    try:
        cursor.execute(sql)
        productos = cursor.fetchall()

        if not productos:
            print("No hay productos cargados.")
        else:
            for p in productos:
                print(f"ID: {p[0]} | Nombre: {p[1]} | Desc: {p[2]} | Cant: {p[3]} | Precio: ${p[4]} | Cat: {p[5]}")
    except sqlite3.Error as e:
        print("Error al mostrar productos:", e)
    finally:
        conexion.close()


# ======================================================
# BUSCAR PRODUCTO POR ID
# ======================================================
def buscar_producto():
    print("=== BUSCAR PRODUCTO POR ID ===")

    prod_id = input("Ingrese ID del producto: ").strip()

    if not prod_id.isdigit():
        print("Debe ingresar un número.")
        return

    conexion = crear_conexion()
    cursor = conexion.cursor()

    sql = "SELECT * FROM productos WHERE id = ?"

    try:
        cursor.execute(sql, (prod_id,))
        p = cursor.fetchone()

        if p:
            print(f"ID: {p[0]} | Nombre: {p[1]} | Desc: {p[2]} | Cant: {p[3]} | Precio: ${p[4]} | Cat: {p[5]}")
        else:
            print("No existe un producto con ese ID.")
    except sqlite3.Error as e:
        print("Error al buscar:", e)
    finally:
        conexion.close()


# ======================================================
# ACTUALIZAR PRODUCTO POR ID
# ======================================================
def actualizar_producto():
    print("=== ACTUALIZAR PRODUCTO ===")

    prod_id = input("Ingrese ID del producto a actualizar: ")

    if not prod_id.isdigit():
        print("ID inválido.")
        return

    nombre = input("Nuevo nombre: ").strip()
    descripcion = input("Nueva descripción: ").strip()
    cantidad = input("Nueva cantidad: ").strip()
    precio = input("Nuevo precio: ").strip()
    categoria = input("Nueva categoría: ").strip()

    if not nombre or not cantidad or not precio:
        print("Nombre, cantidad y precio no pueden estar vacíos.")
        return

    if not cantidad.isdigit():
        print("Cantidad inválida.")
        return
    cantidad = int(cantidad)

    try:
        precio = float(precio)
    except:
        print("Precio inválido.")
        return

    conexion = crear_conexion()
    cursor = conexion.cursor()

    sql = """
    UPDATE productos
    SET nombre = ?, descripcion = ?, cantidad = ?, precio = ?, categoria = ?
    WHERE id = ?
    """

    try:
        cursor.execute(sql, (nombre, descripcion, cantidad, precio, categoria, prod_id))
        conexion.commit()

        if cursor.rowcount > 0:
            print("Producto actualizado correctamente.")
        else:
            print("No existe producto con ese ID.")
    except sqlite3.Error as e:
        print("Error al actualizar producto:", e)
    finally:
        conexion.close()


# ======================================================
# ELIMINAR PRODUCTO POR ID
# ======================================================
def eliminar_producto():
    print("=== ELIMINAR PRODUCTO ===")

    prod_id = input("Ingrese ID a eliminar: ")

    if not prod_id.isdigit():
        print("ID inválido.")
        return

    conexion = crear_conexion()
    cursor = conexion.cursor()

    sql = "DELETE FROM productos WHERE id = ?"

    try:
        cursor.execute(sql, (prod_id,))
        conexion.commit()

        if cursor.rowcount > 0:
            print("Producto eliminado.")
        else:
            print("ID no encontrado.")
    except sqlite3.Error as e:
        print("Error al eliminar:", e)
    finally:
        conexion.close()


# ======================================================
# REPORTE: STOCK BAJO
# ======================================================
def reporte_stock_bajo():
    print("=== REPORTE DE STOCK BAJO ===")

    limite = input("Mostrar productos con cantidad menor o igual a: ")

    if not limite.isdigit():
        print("Debe ingresar un número.")
        return

    limite = int(limite)

    conexion = crear_conexion()
    cursor = conexion.cursor()

    sql = "SELECT * FROM productos WHERE cantidad <= ?"

    try:
        cursor.execute(sql, (limite,))
        productos = cursor.fetchall()

        if not productos:
            print("No hay productos con stock bajo.")
        else:
            for p in productos:
                print(f"ID: {p[0]} | {p[1]} | Cant: {p[3]} | Precio: ${p[4]}")
    except sqlite3.Error as e:
        print("Error al generar reporte:", e)
    finally:
        conexion.close()

#Productos de ejemplo
def menu():
    crear_tabla() #Asegura que la tabla exista

    #Cargar productos de ejemplo si la tabla está vacía 
    conexion = crear_conexion()
    cursor = conexion.cursor()
    cursor.execute("SELECT COUNT(*) FROM productos")
    resultado = cursor.fetchone() #Esto devuelve una tupla
    if resultado == (0,):           #Comparamos la tupla completa
     cursor.execute("""
        INSERT INTO productos (nombre, descripcion, cantidad, precio, categoria)
        VALUES 
        ('Acondicionador', '350ml', 15, 4500, 'Higiene'),
        ('Yerba Mate', '1kg', 30, 5500, 'Almacen')
         """)
    conexion.commit()
    print("**Se cargaron 2 productos de ejemplo para comenzar.**")

# ======================================================
# MENÚ PRINCIPAL
# ======================================================
    opcion = ""
    while opcion != "7":
        print("\n" + "=" * 45)
        print("1. Agregar producto")
        print("2. Mostrar productos")
        print("3. Buscar producto por ID")
        print("4. Actualizar producto")
        print("5. Eliminar producto")
        print("6. Reporte de stock bajo")
        print("7. Salir")

        opcion = input("Seleccione una opción: ")

        if opcion == "1":
            agregar_producto()
        elif opcion == "2":
            mostrar_productos()
        elif opcion == "3":
            buscar_producto()
        elif opcion == "4":
            actualizar_producto()
        elif opcion == "5":
            eliminar_producto()
        elif opcion == "6":
            reporte_stock_bajo()
        elif opcion == "7":
            print("Saliendo del sistema...")
        else:
            print("Opción inválida.")

# Ejecutar programa
menu()