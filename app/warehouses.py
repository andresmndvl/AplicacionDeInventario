# app/warehouses.py
from flask import Blueprint, render_template, request, redirect, url_for, flash
from .models import Almacen
from . import db
from flask_login import current_user, login_required
from .decorators import role_required
from datetime import datetime, timezone

bp = Blueprint('warehouses', __name__, template_folder='templates/warehouses')

@bp.route('/')
@login_required
def list():
    """
    Endpoint: 'warehouses.list'
    Lista almacenes; muestra correctamente los almacenes (antes decía 'productos').
    """
    q = Almacen.query
    nombre = request.args.get('nombre')
    if nombre:
        q = q.filter(Almacen.nombre.ilike(f'%{nombre}%'))
    almacenes = q.all()
    return render_template('warehouses/list.html', almacenes=almacenes)

@bp.route('/create', methods=['GET', 'POST'])
@login_required
@role_required('ADMIN', 'ALMACENES')
def create():
    """
    Endpoint: 'warehouses.create'
    Crear almacén y marcar fecha_hora_creacion y ultimo_usuario_en_modificar.
    """
    if request.method == 'POST':
        nombre = request.form.get('nombre')
        a = Almacen(
            nombre=nombre,
            fecha_hora_creacion=datetime.now(timezone.utc),  # añadido
            ultimo_usuario_en_modificar=current_user.nombre  # añadido
        )
        db.session.add(a)
        db.session.commit()
        flash('Almacén creado', 'success')
        return redirect(url_for('warehouses.list'))
    return render_template('warehouses/form.html', action='Crear')

@bp.route('/edit/<int:id>', methods=['GET', 'POST'])
@login_required
@role_required('ADMIN', 'ALMACENES')
def edit(id):
    """
    Endpoint: 'warehouses.edit'
    Editar almacén y actualizar timestamps + usuario.
    """
    a = Almacen.query.get_or_404(id)
    if request.method == 'POST':
        a.nombre = request.form.get('nombre')
        a.fecha_hora_ultima_modificacion = datetime.now(timezone.utc)  # añadido
        a.ultimo_usuario_en_modificar = current_user.nombre  # añadido
        db.session.commit()
        flash('Almacén actualizado', 'success')
        return redirect(url_for('warehouses.list'))
    return render_template('warehouses/form.html', almacen=a, action='Editar')

@bp.route('/delete/<int:id>', methods=['POST'])
@login_required
@role_required('ADMIN', 'ALMACENES')
def delete(id):
    """
    Endpoint: 'warehouses.delete'
    Eliminar almacén.
    """
    a = Almacen.query.get_or_404(id)
    db.session.delete(a)
    db.session.commit()
    flash('Almacén eliminado', 'warning')
    return redirect(url_for('warehouses.list'))
