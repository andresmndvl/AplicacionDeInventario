import os
from werkzeug.security import generate_password_hash
import sqlite3

DB = os.path.join(os.path.dirname(__file__), '..', 'data', 'InventarioBD.db')

def run():
    conn = sqlite3.connect(DB)
    c = conn.cursor()

    # crear tabla usuarios si no existe
    c.execute('''
    CREATE TABLE IF NOT EXISTS usuarios (
      nombre TEXT PRIMARY KEY, password TEXT NOT NULL, fecha_hora_ultimo_inicio TEXT, rol TEXT NOT NULL
    );
    ''')

    users = [
        ('ADMIN', 'admin23', 'ADMIN'),
        ('PRODUCTOS', 'productos19', 'PRODUCTOS'),
        ('ALMACENES', 'almacenes11', 'ALMACENES')
    ]

    for nombre, pwd, rol in users:
        hashed = generate_password_hash(pwd)
        # upsert
        c.execute('INSERT OR REPLACE INTO usuarios (nombre,password,fecha_hora_ultimo_inicio,rol) VALUES (?,?,NULL,?)',
                  (nombre, hashed, rol))
    conn.commit()
    conn.close()
    print("Usuarios creados/actualizados.")

if __name__ == "__main__":
    run()
