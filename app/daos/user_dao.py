from app.models.user_model import User
from app import db
from sqlalchemy.exc import SQLAlchemyError, IntegrityError

def get_user_by_username(username):
    try:
        return User.query.filter_by(username=username).first()
    except SQLAlchemyError as e:
        print("Error get_user_by_username:", e)
        return None

def get_all_user():
    try:
        return User.query.all()
    except Exception as e:
        print("Error get_all_user:", e)
        return []
    

def get_user_by_akses(akses):
    try:
        users = User.query.filter(User.jabatan != akses).all()
        return [u.to_dict() for u in users]
    except Exception as e:
        print("Error get_user_by_akses:", e)
        return []

def insert_user(username, password, nama, jabatan):
    try:
        user = User(
            username=username,
            password=password,
            nama=nama,
            jabatan=jabatan
        )
        db.session.add(user)
        db.session.commit()
        return {"status":True, "message":"Berhasil menyimpan akses !!!"}
    except IntegrityError as e:
        db.session.rollback()
        print("Error insert_user:", e)
        return {"status": False, "message": "Akses sudah terdaftar !!!"}
    except Exception as e:
        db.session.rollback() 
        print("Error insert_user:", e)
        return {"status":False, "message":"Gagal menyimpan akses !!!"}
    
def update_user(username, password, nama, jabatan):
    try:
        user = db.session.get(User, username)
        if not user:
            return {"status": False, "message": "Akses tidak ditemukan!"}
        user.password = password
        user.nama = nama
        user.jabatan = jabatan
        db.session.commit()
        return {"status": True, "message": "Berhasil mengupdate akses!"}
    except Exception as e:
        db.session.rollback()
        print("Error update_produk:", e)
        return {"status": False, "message": "Gagal mengupdate akses!"}

def delete_user(username):
    try:
        user = db.session.get(User, username)
        if not user:
            return {"status": False, "message": "Akses tidak ditemukan!"}
        db.session.delete(user)
        db.session.commit()
        return {"status": True, "message": "Berhasil menghapus akses!"}
    except Exception as e:
        db.session.rollback()
        print("Error delete_user:", e)
        return {"status": False, "message": "Gagal hapus akses"}