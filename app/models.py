# app/models.py
# Modelos SQLAlchemy con timestamps timezone-aware
from datetime import datetime, timezone
from . import db, login_manager
from flask_login import UserMixin

def now_utc():
    # Helper para valores por defecto timezone-aware
    return datetime.now(timezone.utc)

class User(UserMixin, db.Model):
    __tablename__ = 'usuarios'
    nombre = db.Column(db.String(64), primary_key=True)  # nombre como PK (requisito)
    password = db.Column(db.String(255), nullable=False)
    fecha_hora_ultimo_inicio = db.Column(db.DateTime, nullable=True)  # <-- usado por el requisito
    rol = db.Column(db.String(20), nullable=False)

    def get_id(self):
        return self.nombre

@login_manager.user_loader
def load_user(user_id):
    return db.session.get(User, user_id)

class Almacen(db.Model):
    __tablename__ = 'almacenes'
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(200), nullable=False)

    # timestamps y tracking (cumplen el requisito)
    fecha_hora_creacion = db.Column(db.DateTime, nullable=False, default=now_utc)
    fecha_hora_ultima_modificacion = db.Column(db.DateTime, nullable=True, onupdate=now_utc)
    ultimo_usuario_en_modificar = db.Column(db.String(64), nullable=True)

    productos = db.relationship('Producto', back_populates='almacen', cascade="all, delete-orphan")

class Producto(db.Model):
    __tablename__ = 'productos'
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(200), nullable=False)
    descripcion = db.Column(db.Text, nullable=True)
    cantidad = db.Column(db.Integer, nullable=False, default=0)
    precio = db.Column(db.Float, nullable=False, default=0.0)

    almacen_id = db.Column(db.Integer, db.ForeignKey('almacenes.id'), nullable=True)
    almacen = db.relationship('Almacen', back_populates='productos')

    fecha_hora_creacion = db.Column(db.DateTime, nullable=False, default=now_utc)
    fecha_hora_ultima_modificacion = db.Column(db.DateTime, nullable=True, onupdate=now_utc)
    ultimo_usuario_en_modificar = db.Column(db.String(64), nullable=True)
