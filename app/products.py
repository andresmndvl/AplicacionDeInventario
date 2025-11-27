from flask import Blueprint, render_template, request, redirect, url_for, flash
from .models import Producto, Almacen
from . import db
from .forms import ProductForm
from flask_login import current_user, login_required
from .decorators import role_required
from datetime import datetime

bp = Blueprint('products', __name__, template_folder='templates/products')

@bp.route('/')
@login_required
def list():
    # filtros básicos desde query params (nombre, cantidad_min, cantidad_max, precio_min, precio_max, almacen)
    q = Producto.query.join(Almacen, isouter=True)
    nombre = request.args.get('nombre')
    if nombre:
        q = q.filter(Producto.nombre.ilike(f'%{nombre}%'))
    # rangos de cantidad
    try:
        cmin = request.args.get('cantidad_min')
        if cmin is not None and cmin != '':
            q = q.filter(Producto.cantidad >= int(cmin))
        cmax = request.args.get('cantidad_max')
        if cmax is not None and cmax != '':
            q = q.filter(Producto.cantidad <= int(cmax))
    except ValueError:
        pass
    # rangos de precio
    try:
        pmin = request.args.get('precio_min')
        if pmin is not None and pmin != '':
            q = q.filter(Producto.precio >= float(pmin))
        pmax = request.args.get('precio_max')
        if pmax is not None and pmax != '':
            q = q.filter(Producto.precio <= float(pmax))
    except ValueError:
        pass

    almacen_id = request.args.get('almacen_id')
    if almacen_id:
        q = q.filter(Producto.almacen_id == int(almacen_id))

    productos = q.all()
    almacenes = Almacen.query.all()
    return render_template('list.html', productos=productos, almacenes=almacenes)

@bp.route('/create', methods=['GET', 'POST'])
@login_required
@role_required('ADMIN', 'PRODUCTOS')
def create():
    form = ProductForm(request.form)
    form.almacen_id.choices = [(a.id, a.nombre) for a in Almacen.query.all()]
    if request.method == 'POST' and form.validate():
        p = Producto(
            nombre=form.nombre.data,
            descripcion=form.descripcion.data,
            cantidad=form.cantidad.data,
            precio=form.precio.data,
            almacen_id=form.almacen_id.data,
            fecha_hora_creacion=datetime.utcnow(),
            ultimo_usuario_en_modificar=current_user.nombre
        )
        db.session.add(p)
        db.session.commit()
        flash('Producto creado', 'success')
        return redirect(url_for('products.list'))
    return render_template('form.html', form=form, action='Crear')

@bp.route('/edit/<int:id>', methods=['GET', 'POST'])
@login_required
@role_required('ADMIN', 'PRODUCTOS')
def edit(id):
    p = Producto.query.get_or_404(id)
    form = ProductForm(request.form, obj=p)
    form.almacen_id.choices = [(a.id, a.nombre) for a in Almacen.query.all()]
    if request.method == 'POST' and form.validate():
        form.populate_obj(p)
        p.fecha_hora_ultima_modificacion = datetime.utcnow()
        p.ultimo_usuario_en_modificar = current_user.nombre
        db.session.commit()
        flash('Producto actualizado', 'success')
        return redirect(url_for('products.list'))
    return render_template('form.html', form=form, action='Editar')

@bp.route('/delete/<int:id>', methods=['POST'])
@login_required
@role_required('ADMIN', 'PRODUCTOS')
def delete(id):
    p = Producto.query.get_or_404(id)
    db.session.delete(p)
    db.session.commit()
    flash('Producto eliminado', 'warning')
    return redirect(url_for('products.list'))
