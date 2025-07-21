import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from biblioteca import devolverLibro

prestamo_id = input("Ingrese el ID del préstamo a devolver: ")

devolverLibro(prestamo_id)
