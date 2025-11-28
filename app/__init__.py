import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager

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

    # Ensure DATABASE_URL env or default path
    basedir = os.path.abspath(os.path.dirname(__file__))
    default_db = 'sqlite:///' + os.path.join(basedir, '..', 'data', 'InventarioBD.db')
    app.config.setdefault('SQLALCHEMY_DATABASE_URI', os.environ.get('DATABASE_URL', default_db))

    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'

    # register blueprints (as before)
    from .auth import bp as auth_bp
    from .products import bp as products_bp
    from .warehouses import bp as warehouses_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(products_bp, url_prefix='/productos')
    app.register_blueprint(warehouses_bp, url_prefix='/almacenes')

    # import models to ensure they're registered
    from . import models

    @app.route('/')
    def index():
        from flask import render_template
        return render_template('home.html')

    return app
