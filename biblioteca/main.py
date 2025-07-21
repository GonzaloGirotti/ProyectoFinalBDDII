import os
import sys

# Importar las funciones de biblioteca
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from biblioteca import agregarLibro
from biblioteca import prestarLibro
from biblioteca import devolverLibro
from biblioteca import buscarLibros
from biblioteca import crearLibro
from biblioteca import reportePopulares
from db_init import init_db

def main():
    
    init_db()
    while True:
        print("\n--- Biblioteca ---")
        print("1. Agregar libro")
        print("2. Prestar libro")
        print("3. Devolver libro")
        print("4. Buscar libro por criterio")
        print("5. Reporte de libros más prestados")
        print("6. Salir")

        opcion = input("Seleccione una opción: ")

        if opcion == "1":
            libro = crearLibro()
            agregarLibro(libro)
            
        elif opcion == "2":
            ISBN = input("Ingrese el ISBN del libro a prestar: ")
            USUARIO = input("Ingrese el nombre del usuario a prestarselo: ")
            prestarLibro(ISBN, USUARIO)

        elif opcion == "3":
            ID = input("Ingrese el ID del prestamo a devolver: ")
            devolverLibro(ID)

        elif opcion == "4":
            criterio = input("Ingrese el criterio de búsqueda (título, autor, género): ")
            buscarLibros(criterio)

        elif opcion == "5":
            reportePopulares()

        elif opcion == "6":
            print("Saliendo de la biblioteca...")
            break

        else:
            print("Opción no válida, intente de nuevo.")

if __name__ == "__main__":
    main()