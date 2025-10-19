from app import db
from app.models.transaksi_model import Transaksi, DetailTransaksi
from app.models.produk_model import Produk
from app.models.pelanggan_model import Pelanggan
from datetime import date
from sqlalchemy import func, and_
from sqlalchemy.exc import SQLAlchemyError, IntegrityError

def get_new_id_transaksi(tanggal):
    try:
        last_transaksi = (
            db.session.query(Transaksi)
            .filter(func.date(Transaksi.tanggal) == tanggal)
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
    
def get_transaksi_by_date(tanggal_awal, tanggal_akhir, status_bayar=None):
    try:
        query = (
            db.session.query(Transaksi, Pelanggan)
            .join(Pelanggan, Transaksi.nopol == Pelanggan.nopol)
            .filter(
                and_(
                    Transaksi.tanggal >= tanggal_awal,
                    Transaksi.tanggal <= tanggal_akhir
                )
            )
            .order_by(Transaksi.tanggal,Transaksi.id_transaksi)
        )

        # kalau status_bayar ada isinya → tambahin filter
        if status_bayar:
            query = query.filter(Transaksi.status_bayar == status_bayar)

        transaksi = query.all()

        return [
            {
                **t.to_dict(),
                "pelanggan": p.to_dict()
            }
            for t, p in transaksi
        ]
    except Exception as e:
        print("Error get_transaksi_by_date:", e)
        return []

def insert_transaksi(tanggal, nopol, status_bayar, total_harga, details_list):
    try:
        id_transaksi = get_new_id_transaksi(tanggal)
        transaksi = Transaksi(id_transaksi, tanggal, nopol, status_bayar, total_harga)
        details = []
        details_data = []
        data = {}
        for item in details_list:
            # Buat detail transaksi
            detail = DetailTransaksi(
                id_transaksi=id_transaksi,
                tanggal=tanggal,
                id_produk=item["id_produk"],
                nama_produk=item["nama_produk"],
                jenis=item["jenis"],
                harga=item["harga"],
                jumlah=item["jumlah"],
                worker=item["worker"],
                total=item["total"]
            )
            details.append(detail)

            detail_data = {
                'nama_produk':item["nama_produk"],
                'harga':item["harga"],
                'jumlah':item["jumlah"],
                'total':item['total']
            }
            details_data.append(detail_data)

            # Jika jenis BARANG → kurangi stok
            if "BARANG" in item["jenis"]:
                produk = Produk.query.filter_by(id_produk=item["id_produk"]).first()
                if not produk:
                    raise ValueError(f"Produk dengan ID {item['id_produk']} tidak ditemukan!")
                if produk.stok < item["jumlah"]:
                    raise ValueError(f"Stok produk {produk.nama_produk} tidak mencukupi! Sisa: {produk.stok}")
                produk.stok -= item["jumlah"]

        data['id_transaksi'] = id_transaksi
        data['tanggal'] = tanggal
        data['nopol'] = nopol
        data['status_bayar'] = status_bayar
        data['total_harga'] = total_harga
        data['details'] = details_data

        db.session.add(transaksi)
        db.session.add_all(details)
        db.session.commit()
        return {"status":True, "message":"Berhasil menyimpan transaksi !!!","data":data}
    except Exception as e:
        db.session.rollback() 
        print("Error insert_transaksi:", e)
        return {"status":False, "message":"Gagal menyimpan transaksi !!!"}
    
def update_transaksi(id_transaksi, tanggal, nopol, status_bayar, total_harga, details_list):
    try:
        transaksi = db.session.query(Transaksi).filter_by(id_transaksi=id_transaksi, tanggal=tanggal).first()
        transaksi.status_bayar = status_bayar
        transaksi.total_harga = total_harga
        old_details = {d.id_produk: d for d in transaksi.details}
        details_data = []
        data = {}
        for item in details_list:
            id_produk = item["id_produk"]
            jumlah_baru = item["jumlah"]

            produk = db.session.get(Produk, id_produk)

            if id_produk in old_details:
                # sudah ada detail sebelumnya
                detail = old_details[id_produk]
                if "BARANG" in item["jenis"]:
                    jumlah_lama = detail.jumlah
                    if jumlah_baru != jumlah_lama:
                        selisih = jumlah_baru - jumlah_lama
                        produk.stok -= selisih  

                        detail.jumlah = jumlah_baru
                        detail.total = jumlah_baru * detail.harga
                        detail.worker = item.get("worker")
            else:
                if "BARANG" in item["jenis"]:
                    produk.stok -= jumlah_baru
                detail = DetailTransaksi(
                    id_transaksi=id_transaksi,
                    tanggal=tanggal,
                    id_produk=item["id_produk"],
                    nama_produk=item["nama_produk"],
                    jenis=item["jenis"],
                    harga=item["harga"],
                    jumlah=jumlah_baru,
                    worker=item["worker"],
                    total=item["total"],
                )
                db.session.add(detail)

            detail_data = {
                'nama_produk':item["nama_produk"],
                'harga':item["harga"],
                'jumlah':item["jumlah"],
                'total':item['total']
            }
            details_data.append(detail_data)

        # --- Hapus detail lama yang tidak ada di details_list ---
        details_id_set = {item["id_produk"] for item in details_list}
        for id_produk, detail in old_details.items():
            if id_produk not in details_id_set:
                produk = db.session.get(Produk, id_produk)
                if "BARANG" in detail.jenis:
                    produk.stok += detail.jumlah  # kembalikan stok
                db.session.delete(detail)

        data['id_transaksi'] = id_transaksi
        data['tanggal'] = tanggal
        data['nopol'] = nopol
        data['status_bayar'] = status_bayar
        data['total_harga'] = total_harga
        data['details'] = details_data
        db.session.commit()
        return {"status":True, "message":"Berhasil menyimpan transaksi !!!","data":data}
    except Exception as e:
        db.session.rollback() 
        print("Error update_transaksi:", e)
        return {"status":False, "message":"Gagal menyimpan transaksi !!!"}
    
def get_detail_transaksi_by_worker(pegawai ,tanggal_awal, tanggal_akhir):
    try:
        query = (
            db.session.query(DetailTransaksi)
            .filter(
                and_(
                    DetailTransaksi.tanggal >= tanggal_awal,
                    DetailTransaksi.tanggal <= tanggal_akhir,
                    DetailTransaksi.worker == pegawai
                )
            )
            .order_by(DetailTransaksi.tanggal,DetailTransaksi.id_transaksi)
        )

        details = query.all()

        return [d.to_dict() for d in details]
    except Exception as e:
        print("Error get_detail_transaksi_by_worker:", e)
        return None
    
def delete_transaksi(id_transaksi,tanggal):
    try:
        transaksi = db.session.query(Transaksi).filter_by(id_transaksi=id_transaksi, tanggal=tanggal).first()
        if not transaksi:
            return {"status": False, "message": "Transaksi tidak ditemukan!"}
        for item in transaksi.details:
            if "BARANG" in item.jenis:
                produk = db.session.query(Produk).filter_by(id_produk=item.id_produk).first()
                if produk:
                    produk.stok += item.jumlah  # kembalikan stok sesuai jumlah yg terjual
                    db.session.add(produk)

        # hapus transaksi (detail ikut terhapus karena cascade)
        db.session.delete(transaksi)
        db.session.commit()
        return {"status": True, "message": "Berhasil menghapus transaksi!"}
    except Exception as e:
        db.session.rollback()
        print("Error transaksi_produk:", e)
        return {"status": False, "message": "Gagal hapus transaksi"}