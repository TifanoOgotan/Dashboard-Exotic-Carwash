from flask import Blueprint, render_template, request, redirect, url_for, session, flash, jsonify
from app.daos import pelanggan_dao

pelanggan_bp = Blueprint('pelanggan', __name__, url_prefix='/pelanggan')

@pelanggan_bp.route('/')
def pelanggan():
    if not session.get('person'):
        flash("Anda Harus Login !!!", "unauthorized")
        return redirect(url_for('auth.login'))
    if session.get('person').get('jabatan') not in 'OWNER ADMIN KASIR':
        flash("Anda Tidak Berhak !!!", "info")
        return redirect(url_for('base.home'))
    pelanggan_list = pelanggan_dao.get_all_pelanggan()
    return render_template('pelanggan.html', pelanggan_list = pelanggan_list)

@pelanggan_bp.route('/data', methods=['POST'])
def data_pelanggan():
    if not session.get('person'):
        flash("Anda Harus Login !!!", "unauthorized")
        return redirect(url_for('auth.login'))
    data = pelanggan_dao.get_all_pelanggan()
    return jsonify({"data": data})

@pelanggan_bp.route('/tambah-pelanggan', methods=['POST'])
def tambah_pelanggan():
    if not session.get('person'):
        flash("Anda Harus Login !!!", "unauthorized")
        return redirect(url_for('auth.login'))
    if session.get('person').get('jabatan') not in 'OWNER ADMIN KASIR':
        return {"status": False, "message": "Anda Tidak Berhak !!!"}
    param = request.get_json()
    nopol = param.get('nopol')
    nama_pelanggan = param.get('nama_pelanggan')
    nama_kendaraan = param.get('nama_kendaraan')
    no_hp = param.get('no_hp')
    hasil = pelanggan_dao.insert_pelanggan(nopol, nama_pelanggan, nama_kendaraan, no_hp)
    return jsonify(hasil)

@pelanggan_bp.route('/delete/<nopol>', methods=['POST'])
def delete_produk(nopol):
    if not session.get('person'):
        flash("Anda Harus Login !!!", "unauthorized")
        return redirect(url_for('auth.login'))
    if session.get('person').get('jabatan') not in 'OWNER ADMIN':
        return {"status": False, "message": "Anda Tidak Berhak !!!"}
    hasil = pelanggan_dao.delete_pelanggan(nopol)
    return jsonify(hasil)

@pelanggan_bp.route('/update-pelanggan', methods=['POST'])
def update_pelanggan():
    if not session.get('person'):
        flash("Anda Harus Login !!!", "unauthorized")
        return redirect(url_for('auth.login'))
    if session.get('person').get('jabatan') not in 'OWNER ADMIN KASIR':
        return {"status": False, "message": "Anda Tidak Berhak !!!"}
    param = request.get_json()
    nopol = param.get('nopol')
    nama_pelanggan = param.get('nama_pelanggan')
    nama_kendaraan = param.get('nama_kendaraan')
    no_hp = param.get('no_hp')
    hasil = pelanggan_dao.update_pelanggan(nopol, nama_pelanggan, nama_kendaraan, no_hp)
    return jsonify(hasil)