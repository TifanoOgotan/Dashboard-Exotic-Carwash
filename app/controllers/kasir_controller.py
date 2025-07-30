from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from app.daos import menu_dao, user_dao

kasir_bp = Blueprint('kasir', __name__, url_prefix='/kasir')

@kasir_bp.route('/')
def kasir():
    if not session.get('person'):
        flash("Anda Harus Login !!!", "unauthorized")
        return redirect(url_for('auth.login'))  # Arahkan ke endpoint login

    

    return render_template('kasir.html')