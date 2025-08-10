from app.models.user_model import Pegawai
from app import db
from sqlalchemy.exc import SQLAlchemyError, IntegrityError

def get_pegawai_by_username(username):
    try:
        return Pegawai.query.filter_by(username=username).first()
    except SQLAlchemyError as e:
        print("Error get_pegawai_by_username:", e)
        return None

def get_all_pegawai():
    try:
        return Pegawai.query.all()
    except Exception as e:
        print("Error get_all_pegawai:", e)
        return []
    
def insert_pegawai(data):
    try:
        pegawai = Pegawai(
            nama_pegawai=data['nama_pegawai'],
            username=data['username'],
            password=data['password'],
            jabatan=data['jabatan'],
            no_hp=data['no_hp'],
            tgl_masuk=data['tgl_masuk'],
            status=data['status']
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
        print("Error insert_pegawai:", e)
        return {"status":False, "message":"Gagal menyimpan pegawai !!!"}