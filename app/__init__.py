import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager

# extensiones
db = SQLAlchemy()
migrate = Migrate()
login_manager = LoginManager()

def create_app(config_class=None):
    app = Flask(__name__, static_folder="static", template_folder="templates")

    if config_class is None:
        cfg = os.environ.get("FLASK_CONFIG", "config.DevelopmentConfig")
        app.config.from_object(cfg)
    else:
        app.config.from_object(config_class)

    basedir = os.path.abspath(os.path.dirname(__file__))
    default_db = 'sqlite:///' + os.path.join(basedir, '..', 'data', 'InventarioBD.db')
    app.config.setdefault('SQLALCHEMY_DATABASE_URI', os.environ.get('DATABASE_URL', default_db))

    # inicializar extensiones
    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'


    from datetime import datetime, timezone, timedelta
    try:
        from zoneinfo import ZoneInfo
        HERMOSILLO_TZ = ZoneInfo("America/Hermosillo")
    except Exception:
        HERMOSILLO_TZ = timezone(timedelta(hours=-7))

    def format_local_dt(value, fmt="%d/%m/%Y %H:%M:%S %Z"):
        """
        Convierte un datetime (timezone-aware o naive asumido UTC) a America/Hermosillo.
        Retorna string formateado. Si value es None -> retorna cadena vacía.
        """
        if value is None:
            return ""
        if not hasattr(value, "tzinfo") or value.tzinfo is None:
            value = value.replace(tzinfo=timezone.utc)
        try:
            local = value.astimezone(HERMOSILLO_TZ)
            return local.strftime(fmt)
        except Exception:
            local = value.astimezone(HERMOSILLO_TZ)
            return local.strftime(fmt)

    app.jinja_env.filters['local_dt'] = format_local_dt

    # Blueprints
    from .auth import bp as auth_bp
    from .products import bp as products_bp
    from .warehouses import bp as warehouses_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(products_bp, url_prefix='/productos')
    app.register_blueprint(warehouses_bp, url_prefix='/almacenes')

    # importar modelos (para que sqlalchemy los reconozca)
    from . import models

    @app.route('/')
    def index():
        from flask import render_template
        return render_template('home.html')

    return app
