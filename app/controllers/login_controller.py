from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from app.daos import menu_dao, user_dao

auth_bp = Blueprint('auth', __name__, url_prefix='/auth')

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        user = user_dao.get_pegawai_by_username(username)
        if user and user.password == password:
            session['person'] = {
                "nama": user.nama_pegawai.title(),
                "username": user.username,
                "jabatan": user.jabatan,
                "no_hp": user.no_hp
            }

            session['menus'] = menu_dao.get_menu_by_akses(user.jabatan)

            flash(f"Login Berhasil \nSelamat Datang {user.nama_pegawai.title()}", "success")
            return redirect(url_for('base.home'))
        else:
            flash("Username atau Password salah!", "error")

    return render_template('login.html')


@auth_bp.route('/logout')
def logout():
    session.clear()
    flash("Anda Telah Keluar.", "info")
    return redirect(url_for('auth.login'))
