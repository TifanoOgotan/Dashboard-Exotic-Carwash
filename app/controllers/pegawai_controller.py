from flask import Blueprint, render_template, request, redirect, url_for, session, flash, jsonify
from app.daos import pegawai_dao, transaksi_dao

pegawai_bp = Blueprint('pegawai', __name__, url_prefix='/pegawai')

@pegawai_bp.route('/')
def pegawai():
    if not session.get('person'):
        flash("Anda Harus Login !!!", "unauthorized")
        return redirect(url_for('auth.login'))
    if not session.get('person').get('jabatan') in 'DEV OWNER ADMIN':
        flash("Anda Tidak Berhak !!!", "info")
        return redirect(url_for('base.home'))
    pegawai_list = pegawai_dao.get_all_pegawai()
    return render_template('pegawai.html', pegawai_list = pegawai_list)

@pegawai_bp.route('/data', methods=['POST'])
def data_pegawai():
    if not session.get('person'):
        flash("Anda Harus Login !!!", "unauthorized")
        return redirect(url_for('auth.login'))
    data = pegawai_dao.get_all_pegawai()
    return jsonify({"data": data})

@pegawai_bp.route('/detail', methods=['POST'])
def data_detail():
    if not session.get('person'):
        flash("Anda Harus Login !!!", "unauthorized")
        return redirect(url_for('auth.login'))
    param = request.get_json()
    pegawai = param.get('pegawai')
    tanggal_awal = param.get('tanggal_awal')
    tanggal_akhir = param.get('tanggal_akhir')
    data = transaksi_dao.get_detail_transaksi_by_worker(pegawai, tanggal_awal, tanggal_akhir)
    return jsonify({"data": data})

@pegawai_bp.route('/tambah-pegawai', methods=['POST'])
def tambah_pegawai():
    if not session.get('person'):
        flash("Anda Harus Login !!!", "unauthorized")
        return redirect(url_for('auth.login'))
    if not session.get('person').get('jabatan') in 'DEV OWNER ADMIN':
        flash("Anda Tidak Berhak !!!", "info")
        return redirect(url_for('base.home'))
    param = request.get_json()
    nama = param.get('nama').strip()
    no_hp = param.get('no_hp')
    hasil = pegawai_dao.insert_pegawai(nama, no_hp)
    return jsonify(hasil)

@pegawai_bp.route('/delete/<nama>', methods=['POST'])
def delete_produk(nama):
    if not session.get('person'):
        flash("Anda Harus Login !!!", "unauthorized")
        return redirect(url_for('auth.login'))
    if not session.get('person').get('jabatan') in 'DEV OWNER ADMIN':
        flash("Anda Tidak Berhak !!!", "info")
        return redirect(url_for('base.home'))
    hasil = pegawai_dao.delete_pegawai(nama)
    return jsonify(hasil)