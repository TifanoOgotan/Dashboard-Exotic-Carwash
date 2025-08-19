from app import db
from app.models.transaksi_model import Transaksi, DetailTransaksi
from app.models.produk_model import Produk
from app.models.pelanggan_model import Pelanggan
from datetime import date
from sqlalchemy import func, and_
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
        return None

def insert_transaksi(nopol, status_bayar, total_harga, details_list):
    try:
        id_transaksi = get_new_id_transaksi_today()
        transaksi = Transaksi(id_transaksi, date.today(), nopol, status_bayar, total_harga)
        details = []
        details_data = []
        data = {}
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

            detail_data = {
                'nama_produk':item["nama_produk"],
                'harga':item["harga"],
                'jumlah':item["jumlah"],
                'total':item['total']
            }
            details_data.append(detail_data)

            # Jika jenis BARANG → kurangi stok
            if item["jenis"].upper() == "BARANG":
                produk = Produk.query.filter_by(id_produk=item["id_produk"]).first()
                if not produk:
                    raise ValueError(f"Produk dengan ID {item['id_produk']} tidak ditemukan!")
                if produk.stok < item["jumlah"]:
                    raise ValueError(f"Stok produk {produk.nama_produk} tidak mencukupi! Sisa: {produk.stok}")
                produk.stok -= item["jumlah"]

        data['id_transaksi'] = id_transaksi
        data['tanggal'] = date.today().strftime('%d-%b-%Y')
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

            print('COBA', id_produk, id_produk in old_details)

            if id_produk in old_details:
                # sudah ada detail sebelumnya
                detail = old_details[id_produk]
                print(detail)
                jumlah_lama = detail.jumlah
                if jumlah_baru != jumlah_lama:
                    selisih = jumlah_baru - jumlah_lama
                    produk.stok -= selisih  

                    detail.jumlah = jumlah_baru
                    detail.total = jumlah_baru * detail.harga
                    detail.worker = item.get("worker")
            else:
                if item["jenis"].upper() == "BARANG":
                    produk.stok -= jumlah_baru
                detail = DetailTransaksi(
                    id_transaksi=id_transaksi,
                    tanggal=date.today(),
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

        data['id_transaksi'] = id_transaksi
        data['tanggal'] = date.today().strftime('%d-%b-%Y')
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