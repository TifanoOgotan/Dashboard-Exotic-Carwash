from flask import Blueprint, render_template, request, redirect, url_for, session, flash, jsonify
from app.daos import menu_dao, user_dao, pelanggan_dao, transaksi_dao

kasir_bp = Blueprint('kasir', __name__, url_prefix='/kasir')

@kasir_bp.route('/')
def kasir():
    if not session.get('person'):
        flash("Anda Harus Login !!!", "unauthorized")
        return redirect(url_for('auth.login'))  # Arahkan ke endpoint login

    daftar = pelanggan_dao.get_all_pelanggan()

    return render_template('kasir.html',daftar=daftar)

@kasir_bp.route('/simpan-transaksi', methods=['POST'])
def simpan_transaksi():
    data = request.get_json()
    nopol = data.get('nopol')
    nama_pelanggan = data.get('nama_pelanggan')
    nama_kendaraan = data.get('nama_kendaraan')
    no_hp = data.get('no_hp')
    total_harga = data.get('total_harga')
    status_bayar = data.get('status_bayar')
    edit = data.get('edit')
    details = data.get('details')

    pelanggan_dao.check_pelanggan(nopol, nama_pelanggan, nama_kendaraan, no_hp, edit)

    hasil = transaksi_dao.insert_transaksi(nopol, status_bayar, total_harga, details)

    return jsonify(hasil)