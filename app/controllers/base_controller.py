import os
from flask import Blueprint, render_template, request, redirect, url_for, session, flash, send_from_directory, current_app
from app.daos import menu_dao, user_dao, transaksi_dao
from datetime import date

base_bp = Blueprint('base', __name__, url_prefix='/')

@base_bp.route('/')
@base_bp.route('/home')
def home():
    if not session.get('person'):
        flash("Anda Harus Login !!!", "unauthorized")
        return redirect(url_for('auth.login'))

    transaksi = transaksi_dao.get_transaksi_by_date(date.today(), date.today())
    total_transaksi = len(transaksi)
    pendapatan = 0
    total_bb = 0

    if transaksi:
        for trx in transaksi:
            if trx['status_bayar'] == 'BB':
                total_bb += 1
            else:
                pendapatan += trx['total_harga']

    data = {
        "total_transaksi": total_transaksi,
        "pendapatan": f"{pendapatan:,}".replace(",", "."),
        "total_bb": total_bb
    }

    return render_template('dashboard.html', data=data)


# Endpoint manifest.json
@base_bp.route('/manifest.json')
def manifest():
    return send_from_directory(
        os.path.join(current_app.root_path, 'static'),
        'manifest.json',
        mimetype='application/manifest+json'
    )

# Endpoint service-worker.js
@base_bp.route('/service-worker.js')
def service_worker():
    return send_from_directory(
        os.path.join(current_app.root_path, 'static'),
        'service-worker.js',
        mimetype='application/javascript'
    )
