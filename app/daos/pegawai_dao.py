from app.models.pegawai_model import Pegawai
from app import db
from sqlalchemy.exc import SQLAlchemyError, IntegrityError

def get_pegawai_by_nama(nama):
    try:
        return Pegawai.query.filter_by(nama=nama).first()
    except SQLAlchemyError as e:
        print("Error get_pegawai_by_nama:", e)
        return None

def get_all_pegawai():
    try:
        pegawais = Pegawai.query.all()
        return [p.to_dict() for p in pegawais]
    except Exception as e:
        print("Error get_all_pegawai:", e)
        return None
    
def insert_pegawai(nama,no_hp):
    try:
        pegawai = Pegawai(
            nama=nama,
            no_hp=no_hp
        )
        db.session.add(pegawai)
        db.session.commit()
        return {"status":True, "message":"Berhasil menyimpan pegawai !!!"}
    except IntegrityError as e:
        db.session.rollback()
        print("Error insert_pegawai:", e)
        return {"status": False, "message": "Pegawai sudah terdaftar !!!"}
    except Exception as e:
        db.session.rollback() 
        print("Error insert_user:", e)
        return {"status":False, "message":"Gagal menyimpan pegawai !!!"}
    
def delete_pegawai(nama):
    try:
        print(len(nama))
        pegawai = db.session.get(Pegawai, nama)
        if not pegawai:
            return {"status": False, "message": "Pegawai tidak ditemukan!"}
        db.session.delete(pegawai)
        db.session.commit()
        return {"status": True, "message": "Berhasil menghapus pegawai!"}
    except Exception as e:
        db.session.rollback()
        print("Error delete_produk:", e)
        return {"status": False, "message": "Gagal hapus pegawai"}