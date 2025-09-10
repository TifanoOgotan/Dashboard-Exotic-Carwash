from flask import Blueprint, render_template, request, redirect, url_for, session, flash, jsonify
from app.daos import user_dao

akses_bp = Blueprint('akses', __name__, url_prefix='/akses')

@akses_bp.route('/')
def akses():
    if not session.get('person'):
        flash("Anda Harus Login !!!", "unauthorized")
        return redirect(url_for('auth.login'))
    if session.get('person').get('jabatan') not in 'OWNER':
        flash("Anda Tidak Berhak !!!", "info")
        return redirect(url_for('base.home'))
    return render_template('akses.html')

@akses_bp.route('/data', methods=['POST'])
def data_user():
    if not session.get('person'):
        flash("Anda Harus Login !!!", "unauthorized")
        return redirect(url_for('auth.login'))
    data = user_dao.get_user_by_akses("OWNER")
    return jsonify({"data": data})

@akses_bp.route('/tambah-akses', methods=['POST'])
def tambah_akses():
    if not session.get('person'):
        flash("Anda Harus Login !!!", "unauthorized")
        return redirect(url_for('auth.login'))
    if session.get('person').get('jabatan') not in 'OWNER':
        return {"status": False, "message": "Anda Tidak Berhak !!!"}
    param = request.get_json()
    username = param.get('username').strip()
    password = param.get('password').strip()
    nama = param.get('nama').strip()
    jabatan = param.get('jabatan').strip()
    hasil = user_dao.insert_user(username, password, nama, jabatan)
    return jsonify(hasil)

@akses_bp.route('/update-akses', methods=['POST'])
def update_akses():
    if not session.get('person'):
        flash("Anda Harus Login !!!", "unauthorized")
        return redirect(url_for('auth.login'))
    if session.get('person').get('jabatan') not in 'OWNER':
        return {"status": False, "message": "Anda Tidak Berhak !!!"}
    param = request.get_json()
    username = param.get('username')
    password = param.get('password').strip()
    nama = param.get('nama').strip()
    jabatan = param.get('jabatan').strip()
    hasil = user_dao.update_user(username, password, nama, jabatan)
    return jsonify(hasil)

@akses_bp.route('/delete/<nama>', methods=['POST'])
def delete_produk(nama):
    if not session.get('person'):
        flash("Anda Harus Login !!!", "unauthorized")
        return redirect(url_for('auth.login'))
    if session.get('person').get('jabatan') not in 'OWNER':
        return {"status": False, "message": "Anda Tidak Berhak !!!"}
    hasil = user_dao.delete_user(nama)
    return jsonify(hasil)