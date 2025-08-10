from app.models.produk_model import Produk
from app import db
from sqlalchemy.exc import SQLAlchemyError, IntegrityError

def get_all_produk():
    try:
        produks = Produk.query.all()
        return [p.to_dict() for p in produks]
    except Exception as e:
        print("Error get_all_produk:", e)
        return None
    
def insert_produk(nama_produk, jenis, harga, stok):
    try:
        id_produk = generate_id_product(jenis, nama_produk)
        produk = Produk(id_produk, nama_produk, jenis, harga, stok)
        db.session.add(produk)
        db.session.commit()
        return {"status":True, "message":"Berhasil menyimpan produk !!!"}
    except IntegrityError as e:
        db.session.rollback()
        print("Error insert_produk:", e)
        return {"status": False, "message": "Produk sudah terdaftar !!!"}
    except Exception as e:
        db.session.rollback() 
        print("Error insert_produk:", e)
        return {"status":False, "message":"Gagal menyimpan produk !!!"}
    
def update_produk(id_produk, nama_produk, jenis, harga, stok):
    try:
        produk = db.session.get(Produk, id_produk)
        if not produk:
            return {"status": False, "message": "Produk tidak ditemukan!"}
        produk.nama_produk = nama_produk
        produk.jenis = jenis
        produk.harga = harga
        produk.stok = stok
        db.session.commit()
        return {"status": True, "message": "Berhasil mengupdate produk!"}
    except Exception as e:
        db.session.rollback()
        print("Error update_produk:", e)
        return {"status": False, "message": "Gagal mengupdate produk!"}

def delete_produk(id_produk):
    try:
        produk = db.session.get(Produk, id_produk)
        if not produk:
            return {"status": False, "message": "Produk tidak ditemukan!"}
        db.session.delete(produk)
        db.session.commit()
        return {"status": True, "message": "Berhasil menghapus produk!"}
    except Exception as e:
        db.session.rollback()
        print("Error update_produk:", e)
        return {"status": False, "message": "Gagal hapus produk"}

def generate_id_product(jenis, nama_produk):
    depan = jenis[0].upper()
    kata_list = nama_produk.strip().upper().split()
    belakang = ''.join([kata[:3] for kata in kata_list])
    return depan+'-'+belakang