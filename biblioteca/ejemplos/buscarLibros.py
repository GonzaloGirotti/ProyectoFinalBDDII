import sys
import os

# Importar las funciones de biblioteca
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from biblioteca import buscarLibros

libros = buscarLibros("")
criterio = ""


def buscar():
    global libros
    global criterio
    criterio = input("Ingrese el criterio de búsqueda (título, autor, genero): ")
    buscarLibros(criterio)            

buscar()