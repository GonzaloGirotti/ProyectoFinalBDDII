from pymongo import MongoClient, errors
from datetime import datetime
from bson.objectid import ObjectId

client = MongoClient("mongodb://localhost:27017/")
db = client["biblioteca_digital"]
libros = db["libros"]
prestamos = db["prestamos"]

def crearLibro():
    
    
    libro = {}
    
    libro['titulo'] = input("Ingrese el título del libro: ")
    libro['autor'] = input("Ingrese el autor del libro: ")
    libro['isbn'] = input("Ingrese el ISBN del libro: ")
    libro['genero'] = input("Ingrese el género del libro: ")
    libro['copias'] = input("Ingrese la cantidad de copias disponibles: ")
    
    while not libro['titulo'] or not libro['autor'] or not libro['isbn'] or not libro['genero']:
        print("Todos los campos son obligatorios.")
        crearLibro()
        return None
    
    while not libro['copias'].isdigit():
        print("La cantidad de copias debe ser un número entero.")
        try:
            libro['copias'] = input("Ingrese la cantidad de copias disponibles: ")
        except ValueError:
            print("La cantidad de copias debe ser un número entero.")
            return None
        
    libro['copias'] = int(libro['copias'])
    libro['disponibles'] = libro['copias']
    
    return libro
    

def agregarLibro(libro):
    try:
        libro['disponibles'] = libro['copias']
        result = libros.insert_one(libro)
        print(f"Libro agregado con ID: {result.inserted_id}")
    except errors.DuplicateKeyError:
        print("Error: Ya existe un libro con ese ISBN.")
    except Exception as e:
        print(f"Ocurrió un error: {e}")




def prestarLibro(isbn, usuario):
    
    libro = libros.find_one({"isbn": isbn})
    
    if not libro:
        print("Libro no encontrado.")
        return
    
    if libro["disponibles"] <= 0:
        print("No hay copias disponibles de este libro para el préstamo.")
        return
    
    try:
        prestamo = {
            "libroId": libro["_id"],
            "usuario": usuario,
            "fechaPrestamo": datetime.now(),
            "fechaDevolucion": None,
            "devuelto": False
        }
        prestamos.insert_one(prestamo)

        libros.update_one(
            {"_id": libro["_id"]},
            {"$inc": {"disponibles": -1}}
        )

        print(f"Préstamo registrado para '{libro['titulo']}' a nombre de {usuario}.")
    
    except Exception as e:
        print("Error al registrar el préstamo:", e)
        



def devolverLibro(prestamoId):
    try:
        prestamo = prestamos.find_one({"_id": ObjectId(prestamoId), "devuelto": False})
        
        if not prestamo:
            print("Préstamo no encontrado o ya ha sido devuelto.")
            return
        
        prestamos.update_one(
            {"_id": prestamo["_id"]},
            {"$set": {"devuelto": True, "fechaDevolucion": datetime.utcnow()}}
        )

        libros.update_one(
            {"_id": prestamo["libroId"]},
            {"$inc": {"disponibles": 1}}
        )

        print(f"Libro devuelto correctamente. ID del préstamo: {prestamoId}")
    
    except Exception as e:
        print("Error al registrar la devolución:", e)
        


def buscarLibros(criterio):
    try:
        if criterio == "":
            print("Por favor, ingrese un criterio de busqueda.")
            return

        filtro = {}
        campo = ""
        
        if criterio == "autor":
            campo = "autor"
            valor = input("Ingrese el nombre del autor: ")
            filtro = {campo: {"$regex": valor, "$options": "i"}} # el regex $options: "i" es para busqueda insensible a mayusculas y minusculas
        elif criterio == "titulo":
            campo = "titulo"
            valor = input("Ingrese el título del libro: ")
            filtro = {campo: {"$regex": valor, "$options": "i"}}
        elif criterio == "genero":
            campo = "genero"
            valor = input("Ingrese el género del libro: ")
            filtro = {campo: {"$regex": valor, "$options": "i"}}
        else:
            print("Criterio inválido. Use: titulo, autor o genero.")
            return

        resultados = list(libros.find(filtro))

        if len(resultados) == 0:
            print("No se encontraron libros con ese criterio.")
        else:
            print(f"Libros encontrados con el criterio '{criterio}':")
            print("--------------------------------------------------")
            for libro in resultados:
                print(f"ID: {libro['_id']}, Título: {libro['titulo']}, Autor: {libro['autor']}, ISBN: {libro['isbn']}, Disponibles: {libro['disponibles']}")

    except Exception as e:
        print("Error al buscar libros:", e)

        if len(resultados) == 0:
            print("No se encontraron libros con ese criterio.")
            return
        else:
            print(f"Libros encontrados con el criterio '{criterio}':")
            print("--------------------------------------------------")
            for libro in resultados:
                print(f"ID: {libro['_id']}, Título: {libro['titulo']}, Autor: {libro['autor']}, ISBN: {libro['isbn']}, Disponibles: {libro['disponibles']}")
        
    except Exception as e:
        print("Error al buscar libros:", e)
        
# Top 5 libros mas prestados
def reportePopulares():
    try:
        filtrado = [
            {
                "$group": {
                    "_id": "$libroId",
                    "totalPrestamos": {"$sum": 1}
                }
            },
            {
                "$sort": {"totalPrestamos": -1}
            },
            {
                "$limit": 5
            }
        ]
        
        resultados = prestamos.aggregate(filtrado)
        
        print("Top 5 libros más prestados:")
        print("--------------------------------------------------")
        for resultado in resultados:
            libro = libros.find_one({"_id": resultado["_id"]})
            if libro:
                print(f"ID: {libro['_id']}, Título: {libro['titulo']}, Total de Préstamos: {resultado['totalPrestamos']}")
    
    except Exception as e:
        print("Error al generar el reporte de libros populares:", e)
    