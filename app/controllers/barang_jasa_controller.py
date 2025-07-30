from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from app.daos import menu_dao, user_dao

barang_jasa_bp = Blueprint('barang_jasa', __name__, url_prefix='/barang-jasa')

@barang_jasa_bp.route('/')
def barang_jasa():
    if not session.get('person'):
        flash("Anda Harus Login !!!", "unauthorized")
        return redirect(url_for('auth.login'))  # Arahkan ke endpoint login

    return render_template('barang_jasa.html')