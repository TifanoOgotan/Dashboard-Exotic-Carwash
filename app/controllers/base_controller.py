from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from app.daos import menu_dao, user_dao

base_bp = Blueprint('base', __name__, url_prefix='/')

@base_bp.route('/')
@base_bp.route('/home')
def home():
    if not session.get('person'):
        flash("Anda Harus Login !!!", "unauthorized")
        return redirect(url_for('auth.login'))  # Arahkan ke endpoint login

    return render_template('dashboard.html')