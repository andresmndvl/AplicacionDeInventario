from datetime import datetime
from . import db, login_manager
from flask_login import UserMixin

class User(UserMixin, db.Model):
    __tablename__ = 'usuarios'
    nombre = db.Column(db.String, primary_key=True)  # usamos nombre como PK acordado
    password = db.Column(db.String, nullable=False)
    fecha_hora_ultimo_inicio = db.Column(db.DateTime)
    rol = db.Column(db.String(20), nullable=False)

    # flask-login required
    def get_id(self):
        return self.nombre

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)

class Almacen(db.Model):
    __tablename__ = 'almacenes'
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String)

    fecha_hora_creacion = db.Column(db.DateTime, default=datetime.utcnow)
    fecha_hora_ultima_modificacion = db.Column(db.DateTime, onupdate=datetime.utcnow)
    ultimo_usuario_en_modificar = db.Column(db.String)

class Producto(db.Model):
    __tablename__ = 'productos'
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String)
    descripcion = db.Column(db.String)
    cantidad = db.Column(db.Integer)
    precio = db.Column(db.Float)
    almacen_id = db.Column(db.Integer, db.ForeignKey('almacenes.id'))
    almacen = db.relationship('Almacen', backref=db.backref('productos', lazy=True))

    fecha_hora_creacion = db.Column(db.DateTime, default=datetime.utcnow)
    fecha_hora_ultima_modificacion = db.Column(db.DateTime, onupdate=datetime.utcnow)
    ultimo_usuario_en_modificar = db.Column(db.String)
