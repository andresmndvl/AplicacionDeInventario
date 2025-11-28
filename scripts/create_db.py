# scripts/create_db.py
import os
from app import create_app, db
from app.models import User, Almacen, Producto
from werkzeug.security import generate_password_hash
from datetime import datetime

def run(force=False):
    app = create_app()
    with app.app_context():
        db_path = app.config['SQLALCHEMY_DATABASE_URI']
        print("DB URI:", db_path)
        # drop all (careful) if force True
        if force:
            db.drop_all()
            print("Dropped all tables.")
        db.create_all()
        print("Created tables.")

        # seed users (override existing)
        users = [
            ("ADMIN", "admin23", "ADMIN"),
            ("PRODUCTOS", "productos19", "PRODUCTOS"),
            ("ALMACENES", "almacenes11", "ALMACENES")
        ]
        for nombre, pwd, rol in users:
            hashed = generate_password_hash(pwd)  # werkzeug default (pbkdf2:sha256) or scrypt depending on version
            u = User(nombre=nombre, password=hashed, fecha_hora_ultimo_inicio=None, rol=rol)
            # upsert: delete existing with same nombre
            existing = User.query.get(nombre)
            if existing:
                db.session.delete(existing)
            db.session.add(u)
        db.session.commit()
        print("Seeded users.")

        # seed a couple almacenes and productos for testing
        a1 = Almacen(nombre="Almacen Central", fecha_hora_creacion=datetime.utcnow(), ultimo_usuario_en_modificar="ADMIN")
        a2 = Almacen(nombre="Almacen Secundario", fecha_hora_creacion=datetime.utcnow(), ultimo_usuario_en_modificar="ADMIN")
        db.session.add_all([a1, a2])
        db.session.commit()

        p1 = Producto(nombre="Tornillo M6", descripcion="Tornillo acero inoxidable", cantidad=100, precio=0.5,
                      almacen=a1, fecha_hora_creacion=datetime.utcnow(), ultimo_usuario_en_modificar="ADMIN")
        p2 = Producto(nombre="Caja de herramientas", descripcion="Caja plástica 20L", cantidad=10, precio=25.0,
                      almacen=a2, fecha_hora_creacion=datetime.utcnow(), ultimo_usuario_en_modificar="ADMIN")
        db.session.add_all([p1, p2])
        db.session.commit()

        print("Seeded almacenes and productos.")

if __name__ == "__main__":
    # Si quieres forzar recreado, pon True
    run(force=True)
