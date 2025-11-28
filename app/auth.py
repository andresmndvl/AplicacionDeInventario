# app/auth.py
from flask import Blueprint, render_template, redirect, url_for, flash, request
from .forms import LoginForm
from .models import User
from . import db
from werkzeug.security import check_password_hash
from flask_login import login_user, logout_user
from datetime import datetime, timezone

bp = Blueprint('auth', __name__, template_folder='templates')

@bp.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm(request.form)
    if request.method == 'POST' and form.validate():
        nombre = form.nombre.data
        password = form.password.data
        user = User.query.filter_by(nombre=nombre).first()
        if user and check_password_hash(user.password, password):
            login_user(user)

            user.fecha_hora_ultimo_inicio = datetime.now(timezone.utc)
            db.session.commit()

            return redirect(url_for('index'))
        else:
            flash('Usuario o contraseña incorrectos', 'danger')
    return render_template('login.html', form=form)

@bp.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('auth.login'))
