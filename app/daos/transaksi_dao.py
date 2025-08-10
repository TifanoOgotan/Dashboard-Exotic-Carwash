from app import db
from app.models.transaksi_model import Transaksi, DetailTransaksi
from app.models.produk_model import Produk
from datetime import date
from sqlalchemy import func
from sqlalchemy.exc import SQLAlchemyError, IntegrityError

def get_new_id_transaksi_today():
    try:
        last_transaksi = (
            db.session.query(Transaksi)
            .filter(func.date(Transaksi.tanggal) == date.today())
            .order_by(Transaksi.id_transaksi.desc())
            .first()
        )

        if last_transaksi :
            next_num = int(last_transaksi.id_transaksi.split("-")[1]) + 1
            trx = f"TRX-{next_num:04d}"
        else :
            trx = "TRX-0001"
        return trx
    except Exception as e:
        print("Error get_last_id_transaksi_today:", e)
        return None

def insert_transaksi(nopol, status_bayar, total_harga, details_list):
    try:
        id_transaksi = get_new_id_transaksi_today()
        transaksi = Transaksi(id_transaksi, date.today(), nopol, status_bayar, total_harga)
        details = []
        for item in details_list:
            # Buat detail transaksi
            detail = DetailTransaksi(
                id_transaksi=id_transaksi,
                tanggal=date.today(),
                id_produk=item["id_produk"],
                nama_produk=item["nama_produk"],
                jenis=item["jenis"],
                harga=item["harga"],
                jumlah=item["jumlah"],
                worker=item["worker"],
                total=item["total"]
            )
            details.append(detail)

            # Jika jenis BARANG → kurangi stok
            if item["jenis"].upper() == "BARANG":
                produk = Produk.query.filter_by(id_produk=item["id_produk"]).first()
                if not produk:
                    raise ValueError(f"Produk dengan ID {item['id_produk']} tidak ditemukan!")
                
                if produk.stok < item["jumlah"]:
                    raise ValueError(f"Stok produk {produk.nama_produk} tidak mencukupi! Sisa: {produk.stok}")

                produk.stok -= item["jumlah"]

        db.session.add(transaksi)
        db.session.add_all(details)
        db.session.commit()
        return {"status":True, "message":"Berhasil menyimpan transaksi !!!"}
    except Exception as e:
        db.session.rollback() 
        print("Error insert_transaksi:", e)
        return {"status":False, "message":"Gagal menyimpan transaksi !!!"}