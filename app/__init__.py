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
    from app.controllers.produk_controller import produk_bp
    from app.controllers.transaksi_controller import transaksi_bp
    from app.controllers.pegawai_controller import pegawai_bp
    from app.controllers.akses_controller import akses_bp
    from app.controllers.pelanggan_controller import pelanggan_bp

    # register blueprint
    app.register_blueprint(base_bp)
    app.register_blueprint(auth_bp)
    app.register_blueprint(kasir_bp)
    app.register_blueprint(produk_bp)
    app.register_blueprint(transaksi_bp)
    app.register_blueprint(pegawai_bp)
    app.register_blueprint(akses_bp)
    app.register_blueprint(pelanggan_bp)

    return app

