from app.models.pelanggan_model import Pelanggan
from app import db
from sqlalchemy.exc import SQLAlchemyError, IntegrityError

def get_all_pelanggan():
    try:
        pelanggans = Pelanggan.query.all()
        return [p.to_dict() for p in pelanggans]
    except Exception as e:
        print("Error get_all_pelanggan:", e)
        return []
    
def check_pelanggan(nopol, nama_pelanggan, nama_kendaraan, no_hp, edit):
    try:
        pelanggan =  db.session.get(Pelanggan, nopol)
        if pelanggan :
            if edit == 'T':
                pelanggan.nama_pelanggan = nama_pelanggan
                pelanggan.nama_kendaraan = nama_kendaraan
                pelanggan.no_hp = no_hp
                db.session.add(pelanggan)
        else :
            pelanggan = Pelanggan(nopol, nama_pelanggan, nama_kendaraan, no_hp)
            db.session.add(pelanggan)

        return None
    except Exception as e:
        db.session.rollback() 
        print("Error check_pelanggan:", e)
        return None