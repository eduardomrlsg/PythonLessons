import sqlite3

def crear_bd():
    try:

        #Establecemos la conexión a la base de datos
        conexion = sqlite3.connect('restaurante.db')
        cursor = conexion.cursor()
    
        #Creamos las tablas de Categoría y Plato
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS categoria (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nombre VARCHAR(100) UNIQUE NOT NULL                             
        )
        ''')

        cursor.execute('''
        CREATE TABLE IF NOT EXISTS plato (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nombre VARCHAR(100) UNIQUE NOT NULL,
        categoria_id INTEGER NOT NULL,
        FOREIGN KEY(categoria_id) REFERENCES                             
        categoria(id))
        ''')
        #Guardamos el registro de los datos 
        conexion.commit()
    except sqlite3.Error as error:
        print("Error al crear la base de datos:", error)
    finally:
        if conexion: 
            conexion.close()

def agregar_categoria(nombre_categoria):
    try:
        conexion = sqlite3.connect('restaurante.db')
        cursor = conexion.cursor()

        cursor.execute("INSERT INTO categoria (nombre) VALUES (?)",(nombre_categoria,))
        conexion.commit()
        print(f"La categoría {nombre_categoria} se ha creado correctamente")  
    except sqlite3.IntegrityError as error:
        print(f"Error al introducir la categoría, la categoría {nombre_categoria} ya existe")   
    finally:
        if conexion:
            conexion.close()

def menu():
    while True:
        print("\nBienvenido al Menú")
        print("1. Crear Categoría")
        print("2. Crear Plato")
        print("3. Salir")    
        
        opcion = int(input("Selecciona una opción:"))

        if opcion == 1:
            nombre_categoria = input("Ingrese el nombre de la categoria:")
            agregar_categoria(nombre_categoria)
        elif opcion == 2:
            agregar_plato()
        elif opcion == 3: 
            print("Adiós!!")
            break
        else: 
            print("Opcion no válida")

#crear_bd() 

def agregar_plato():
    #Establecemos la conexión a la BDD
    conexion = sqlite3.connect('restaurante.db')
    cursor = conexion.cursor()
    #Obtenemos todas las categorías de la BDD
    cursor.execute("SELECT id,nombre FROM categoria ")
    categorias = cursor.fetchall()
    #Mostramos las categorías al usuario
    print("Categorias disponibles:")
    #for i, (id,nombre) in enumerate (categorias,start=1):
    #    print(f"{i}.{nombre}")       
    for id,nombre in categorias:
        print(f"{id} - {nombre}")
    #Pedimos al usuario que seleccione una categoría
    while True:
        try:
            categoria_id = int(input("Selecciona el número de categoria para añadir el plato:"))
            #Verificamos que la categoría esté entre las que hay en el menú 
            if 1<=categoria_id<=len(categorias):
                break
            else: 
                print("Opción inválida, introduce los datos correctamente")
        except ValueError:
            print("Entrada inválida, introduce los datos correctamente")
    
    nombre_plato = input("Ingrese el nombre del plato para el menú: ")
    try:
        cursor.execute("INSERT INTO plato (nombre,categoria_id) VALUES (?,?)", (nombre_plato,categoria_id))
        conexion.commit()
        print(f"El plato {nombre_plato} se ha creado correctamente")
    except sqlite3.IntegrityError:
        print("Error al agregar el plato")
    conexion.close()


def mostrar_menu():
    conexion = sqlite3.connect('restaurante.db')
    cursor = conexion.cursor()
    #cursor.execute("SELECT nombre FROM categorias")
    #categorias = cursor.fetchall()
    cursor.execute("SELECT nombre, categoria_id FROM plato")
    platos = cursor.fetchall()
    print("\n       Menú VAL Restaurante")
    print("----------------------------------")
    for nombre, categoria_id in platos:
        if categoria_id == 1:
            print(f"Primer Tiempo - {nombre}")
        elif categoria_id ==2:
            print(f"Segundo Tiempo - {nombre}")
        elif categoria_id ==3:
            print(f"Postres - {nombre}")
    conexion.close()
  
'''
def mostrar_menu():
    conexion = sqlite3.connect('restaurante.db')
    cursor = conexion.cursor()

    # Obtener los nombres de las categorías y los platos
    cursor.execute("""
        SELECT p.nombre, c.nombre AS categoria
        FROM plato p
        INNER JOIN categoria c ON p.categoria_id = c.id
        ORDER BY c.nombre, p.nombre
    """)
    platos = cursor.fetchall()

    print("\nMenú del Restaurante")
    print("---------------------")

    categoria_actual = None
    for nombre_plato, nombre_categoria in platos:
        if nombre_categoria != categoria_actual:
            print(f"\n{nombre_categoria.upper()}")
            categoria_actual = nombre_categoria
        print(f"- {nombre_plato}")

    conexion.close()
'''

mostrar_menu()
menu()
