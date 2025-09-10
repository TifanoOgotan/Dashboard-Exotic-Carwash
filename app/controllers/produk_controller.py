from flask import Blueprint, render_template, request, redirect, url_for, session, flash, jsonify
from app.daos import menu_dao, user_dao, produk_dao

produk_bp = Blueprint('produk', __name__, url_prefix='/produk')

@produk_bp.route('/')
def produk():
    if not session.get('person'):
        flash("Anda Harus Login !!!", "unauthorized")
        return redirect(url_for('auth.login'))
    if session.get('person').get('jabatan') not in 'OWNER ADMIN':
        flash("Anda Tidak Berhak !!!", "info")
        return redirect(url_for('base.home'))
    return render_template('produk.html')

@produk_bp.route('/data', methods=['POST'])
def data_produk():
    if not session.get('person'):
        flash("Anda Harus Login !!!", "unauthorized")
        return redirect(url_for('auth.login'))
    data = produk_dao.get_all_produk()
    return jsonify({"data": data})

@produk_bp.route('/tambah-produk', methods=['POST'])
def tambah_produk():
    if not session.get('person'):
        flash("Anda Harus Login !!!", "unauthorized")
        return redirect(url_for('auth.login'))
    if session.get('person').get('jabatan') not in 'OWNER ADMIN':
        return {"status": False, "message": "Anda Tidak Berhak !!!"}
    param = request.get_json()
    nama_produk = param.get('nama_produk')
    jenis = param.get('jenis')
    harga = param.get('harga')
    stok = param.get('stok')
    hasil = produk_dao.insert_produk(nama_produk, jenis, harga, stok)
    return jsonify(hasil)

@produk_bp.route('/update-produk', methods=['POST'])
def update_produk():
    if not session.get('person'):
        flash("Anda Harus Login !!!", "unauthorized")
        return redirect(url_for('auth.login'))
    if session.get('person').get('jabatan') not in 'OWNER ADMIN':
        return {"status": False, "message": "Anda Tidak Berhak !!!"}
    param = request.get_json()
    id_produk = param.get('id_produk')
    nama_produk = param.get('nama_produk')
    jenis = param.get('jenis')
    harga = param.get('harga')
    stok = param.get('stok')
    hasil = produk_dao.update_produk(id_produk, nama_produk, jenis, harga, stok)
    return jsonify(hasil)

@produk_bp.route('/delete/<id_produk>', methods=['POST'])
def delete_produk(id_produk):
    if not session.get('person'):
        flash("Anda Harus Login !!!", "unauthorized")
        return redirect(url_for('auth.login'))
    if session.get('person').get('jabatan') not in 'OWNER ADMIN':
        return {"status": False, "message": "Anda Tidak Berhak !!!"}
    hasil = produk_dao.delete_produk(id_produk)
    return jsonify(hasil)