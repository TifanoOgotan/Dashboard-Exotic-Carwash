from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from .config import Config


db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    app.config.from_object('app.config.Config')

    db.init_app(app)

    @app.errorhandler(404)
    def not_found(e):
        return render_template('404.html'), 404
    
    # register controller
    from app.controllers.base_controller import base_bp
    from app.controllers.login_controller import auth_bp
    from app.controllers.kasir_controller import kasir_bp
    from app.controllers.barang_jasa_controller import barang_jasa_bp

    # register blueprint
    app.register_blueprint(base_bp)
    app.register_blueprint(auth_bp)
    app.register_blueprint(kasir_bp)
    app.register_blueprint(barang_jasa_bp)

    return app

