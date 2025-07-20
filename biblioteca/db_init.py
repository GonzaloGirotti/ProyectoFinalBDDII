from pymongo import MongoClient

def init_db():
    client = MongoClient("mongodb://localhost:27017/")
    db = client["biblioteca_digital"]
    libros = db["libros"]
    prestamos = db["prestamos"]

    libros.create_index("isbn", unique=True)

    print("Base de datos y colecciones inicializadas.")
    client.close()

if __name__ == "__main__":
    init_db()