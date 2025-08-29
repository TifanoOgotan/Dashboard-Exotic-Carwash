from flask import Blueprint, render_template, request, redirect, url_for, session, flash, jsonify
from app.daos import transaksi_dao

transaksi_bp = Blueprint('transaksi', __name__, url_prefix='/transaksi')

@transaksi_bp.route('/')
def transaksi():
    if not session.get('person'):
        flash("Anda Harus Login !!!", "unauthorized")
        return redirect(url_for('auth.login'))
    if not session.get('person').get('jabatan') in 'OWNER ADMIN KASIR VIEW':
        flash("Anda Tidak Berhak !!!", "info")
        return redirect(url_for('base.home'))
    return render_template('transaksi.html')

@transaksi_bp.route('/data', methods=['POST'])
def data_transaksi():
    if not session.get('person'):
        flash("Anda Harus Login !!!", "unauthorized")
        return redirect(url_for('auth.login'))
    if not session.get('person').get('jabatan') in 'OWNER ADMIN KASIR VIEW':
        flash("Anda Tidak Berhak !!!", "info")
        return redirect(url_for('base.home'))
    tanggal_awal = request.form.get("tanggal_awal")
    tanggal_akhir = request.form.get("tanggal_akhir")
    data = transaksi_dao.get_transaksi_by_date(tanggal_awal, tanggal_akhir)
    return jsonify({"data": data})