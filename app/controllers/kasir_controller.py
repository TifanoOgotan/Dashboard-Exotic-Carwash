from flask import Blueprint, render_template, request, redirect, url_for, session, flash, jsonify
from app.daos import menu_dao, user_dao, pelanggan_dao, transaksi_dao, pegawai_dao
from datetime import date, timedelta

kasir_bp = Blueprint('kasir', __name__, url_prefix='/kasir')

@kasir_bp.route('/')
def kasir():
    if not session.get('person'):
        flash("Anda Harus Login !!!", "unauthorized")
        return redirect(url_for('auth.login'))
    if not session.get('person').get('jabatan') in 'DEV OWNER ADMIN KASIR':
        flash("Anda Tidak Berhak !!!", "info")
        return redirect(url_for('base.home'))
    daftar = pelanggan_dao.get_all_pelanggan()
    data_transaksi_bb = transaksi_dao.get_transaksi_by_date(date.today(), date.today(), 'BB')
    pegawai_list = pegawai_dao.get_all_pegawai()
    return render_template('kasir.html',daftar=daftar, data_transaksi_bb = data_transaksi_bb, pegawai_list = pegawai_list)

@kasir_bp.route('/simpan-transaksi', methods=['POST'])
def simpan_transaksi():
    if not session.get('person'):
        flash("Anda Harus Login !!!", "unauthorized")
        return redirect(url_for('auth.login'))
    if not session.get('person').get('jabatan') in 'DEV OWNER ADMIN KASIR':
        flash("Anda Tidak Berhak !!!", "info")
        return redirect(url_for('base.home'))
    param = request.get_json()
    nopol = param.get('nopol')
    nama_pelanggan = param.get('nama_pelanggan')
    nama_kendaraan = param.get('nama_kendaraan')
    no_hp = param.get('no_hp')
    total_harga = param.get('total_harga')
    status_bayar = param.get('status_bayar')
    edit = param.get('edit')
    details = param.get('details')
    pelanggan_dao.check_pelanggan(nopol, nama_pelanggan, nama_kendaraan, no_hp, edit)
    hasil = transaksi_dao.insert_transaksi(nopol, status_bayar, total_harga, details)
    return jsonify(hasil)

@kasir_bp.route('/edit-transaksi', methods=['POST'])
def edit_transaksi():
    if not session.get('person'):
        flash("Anda Harus Login !!!", "unauthorized")
        return redirect(url_for('auth.login'))
    if not session.get('person').get('jabatan') in 'DEV OWNER ADMIN KASIR':
        flash("Anda Tidak Berhak !!!", "info")
        return redirect(url_for('base.home'))
    param = request.get_json()
    id_transaksi = param.get('id_transaksi')
    tanggal = param.get('tanggal')
    nopol = param.get('nopol')
    total_harga = param.get('total_harga')
    status_bayar = param.get('status_bayar')
    details = param.get('details')
    hasil = transaksi_dao.update_transaksi(id_transaksi, tanggal, nopol, status_bayar, total_harga, details)
    return jsonify(hasil)