import sys
import os

# Importar las funciones de biblioteca
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from biblioteca import agregarLibro

nuevo_libro = {
    "titulo": "El Hobbit",
    "autor": "Tolkien",
    "isbn": "978-0307389734",
    "genero": "Fantasía",
    "anioPublicacion": 1968,
    "copias": 3
}

otro_libro = {
    "titulo": "1984",
    "autor": "George Orwell",
    "isbn": "978-0451524935",
    "genero": "Distopía",
    "anioPublicacion": 1949,
    "copias": 5
}

agregarLibro(nuevo_libro)