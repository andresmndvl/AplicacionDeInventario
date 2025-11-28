# app/models.py
from datetime import datetime
from . import db, login_manager
from flask_login import UserMixin

class User(UserMixin, db.Model):
    __tablename__ = 'usuarios'
    nombre = db.Column(db.String(64), primary_key=True)  # usar nombre como PK según requerimiento
    password = db.Column(db.String(255), nullable=False)
    fecha_hora_ultimo_inicio = db.Column(db.DateTime, nullable=True)
    rol = db.Column(db.String(20), nullable=False)

    def get_id(self):
        return self.nombre

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)

class Almacen(db.Model):
    __tablename__ = 'almacenes'
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(200), nullable=False)

    fecha_hora_creacion = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    fecha_hora_ultima_modificacion = db.Column(db.DateTime, nullable=True, onupdate=datetime.utcnow)
    ultimo_usuario_en_modificar = db.Column(db.String(64), nullable=True)

    productos = db.relationship('Producto', back_populates='almacen', cascade="all, delete-orphan")

class Producto(db.Model):
    __tablename__ = 'productos'
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(200), nullable=False)
    descripcion = db.Column(db.Text, nullable=True)
    cantidad = db.Column(db.Integer, nullable=False, default=0)
    precio = db.Column(db.Float, nullable=False, default=0.0)

    # Relación hacia almacenes (almacen_id FK)
    almacen_id = db.Column(db.Integer, db.ForeignKey('almacenes.id'), nullable=True)
    almacen = db.relationship('Almacen', back_populates='productos')

    fecha_hora_creacion = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    fecha_hora_ultima_modificacion = db.Column(db.DateTime, nullable=True, onupdate=datetime.utcnow)
    ultimo_usuario_en_modificar = db.Column(db.String(64), nullable=True)
