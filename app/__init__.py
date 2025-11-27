import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager

db = SQLAlchemy()
migrate = Migrate()
login_manager = LoginManager()

def create_app():
    app = Flask(__name__, static_folder="static", template_folder="templates")
    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'dev-secret')
    basedir = os.path.abspath(os.path.dirname(__file__))
    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get(
        'DATABASE_URL', 'sqlite:///' + os.path.join(basedir, '..', 'data', 'InventarioBD.db')
    )
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'

    # blueprints
    from .auth import bp as auth_bp
    from .products import bp as products_bp
    from .warehouses import bp as warehouses_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(products_bp, url_prefix='/productos')
    app.register_blueprint(warehouses_bp, url_prefix='/almacenes')

    from . import models

    # home route
    @app.route('/')
    def index():
        return __import__('flask').render_template('home.html')

    return app
