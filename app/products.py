# app/products.py
from flask import Blueprint, render_template, request, redirect, url_for, flash
from .models import Producto, Almacen
from . import db
from .forms import ProductForm
from flask_login import current_user, login_required
from .decorators import role_required
from datetime import datetime, timezone

bp = Blueprint('products', __name__, template_folder='templates/products')

@bp.route('/')
@login_required
def list():
    """
    Endpoint: 'products.list'
    Lista productos con filtros y pasa 'almacenes' para el select de filtro.
    """
    q = Producto.query.outerjoin(Almacen)
    nombre = request.args.get('nombre')
    if nombre:
        q = q.filter(Producto.nombre.ilike(f'%{nombre}%'))
    # rango cantidad
    try:
        cmin = request.args.get('cantidad_min')
        if cmin not in (None, ''):
            q = q.filter(Producto.cantidad >= int(cmin))
        cmax = request.args.get('cantidad_max')
        if cmax not in (None, ''):
            q = q.filter(Producto.cantidad <= int(cmax))
    except ValueError:
        pass
    # rango precio
    try:
        pmin = request.args.get('precio_min')
        if pmin not in (None, ''):
            q = q.filter(Producto.precio >= float(pmin))
        pmax = request.args.get('precio_max')
        if pmax not in (None, ''):
            q = q.filter(Producto.precio <= float(pmax))
    except ValueError:
        pass

    almacen_id = request.args.get('almacen_id')
    if almacen_id not in (None, ''):
        try:
            q = q.filter(Producto.almacen_id == int(almacen_id))
        except ValueError:
            pass

    productos = q.all()
    almacenes = Almacen.query.all()
    return render_template('products/list.html', productos=productos, almacenes=almacenes)

@bp.route('/create', methods=['GET', 'POST'])
@login_required
@role_required('ADMIN', 'PRODUCTOS')
def create():
    """
    Endpoint: 'products.create'
    Crear producto; marca fecha_hora_creacion y ultimo_usuario_en_modificar.
    """
    form = ProductForm(request.form)
    form.almacen_id.choices = [(a.id, a.nombre) for a in Almacen.query.all()]
    if request.method == 'POST' and form.validate():
        p = Producto(
            nombre=form.nombre.data,
            descripcion=form.descripcion.data,
            cantidad=form.cantidad.data,
            precio=form.precio.data,
            almacen_id=form.almacen_id.data,
            fecha_hora_creacion=datetime.now(timezone.utc),  # añadido
            ultimo_usuario_en_modificar=current_user.nombre  # añadido
        )
        db.session.add(p)
        db.session.commit()
        flash('Producto creado', 'success')
        return redirect(url_for('products.list'))
    return render_template('products/form.html', form=form, action='Crear')

@bp.route('/edit/<int:id>', methods=['GET', 'POST'])
@login_required
@role_required('ADMIN', 'PRODUCTOS')
def edit(id):
    """
    Endpoint: 'products.edit'
    Editar producto; actualiza fecha_hora_ultima_modificacion y ultimo_usuario_en_modificar.
    """
    p = Producto.query.get_or_404(id)
    form = ProductForm(request.form, obj=p)
    form.almacen_id.choices = [(a.id, a.nombre) for a in Almacen.query.all()]
    if request.method == 'POST' and form.validate():
        form.populate_obj(p)
        p.fecha_hora_ultima_modificacion = datetime.now(timezone.utc)  # añadido
        p.ultimo_usuario_en_modificar = current_user.nombre  # añadido
        db.session.commit()
        flash('Producto actualizado', 'success')
        return redirect(url_for('products.list'))
    return render_template('products/form.html', form=form, action='Editar', producto=p)

@bp.route('/delete/<int:id>', methods=['POST'])
@login_required
@role_required('ADMIN', 'PRODUCTOS')
def delete(id):
    """
    Endpoint: 'products.delete'
    Eliminar producto.
    """
    p = Producto.query.get_or_404(id)
    db.session.delete(p)
    db.session.commit()
    flash('Producto eliminado', 'warning')
    return redirect(url_for('products.list'))
