import sys
import os

# Importar las funciones de biblioteca
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from biblioteca import prestarLibro
prestarLibro("978-0307389734", "Marcos")