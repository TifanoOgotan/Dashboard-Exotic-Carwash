from flask import Blueprint, render_template, request, redirect, url_for, session, flash, jsonify
from app.daos import transaksi_dao, pegawai_dao

transaksi_bp = Blueprint('transaksi', __name__, url_prefix='/transaksi')

@transaksi_bp.route('/')
def transaksi():
    if not session.get('person'):
        flash("Anda Harus Login !!!", "unauthorized")
        return redirect(url_for('auth.login'))
    if session.get('person').get('jabatan') not in 'OWNER ADMIN KASIR VIEW':
        flash("Anda Tidak Berhak !!!", "info")
        return redirect(url_for('base.home'))
    pegawai_list = pegawai_dao.get_all_pegawai()
    return render_template('transaksi.html', pegawai_list = pegawai_list)

@transaksi_bp.route('/data', methods=['POST'])
def data_transaksi():
    if not session.get('person'):
        flash("Anda Harus Login !!!", "unauthorized")
        return redirect(url_for('auth.login'))
    tanggal_awal = request.form.get("tanggal_awal")
    tanggal_akhir = request.form.get("tanggal_akhir")
    data = transaksi_dao.get_transaksi_by_date(tanggal_awal, tanggal_akhir)
    return jsonify({"data": data})

@transaksi_bp.route('/delete/<id>/<tanggal>', methods=['POST'])
def delete_transaksi(id, tanggal):
    if not session.get('person'):
        flash("Anda Harus Login !!!", "unauthorized")
        return redirect(url_for('auth.login'))
    if session.get('person').get('jabatan') not in 'OWNER':
        return {"status": False, "message": "Anda Tidak Berhak !!!"}
    hasil = transaksi_dao.delete_transaksi(id,tanggal)
    return jsonify(hasil)
