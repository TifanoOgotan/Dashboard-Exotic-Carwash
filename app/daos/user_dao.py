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
    
def insert_user(data):
    try:
        user = User(
            nama=data['nama'],
            username=data['username'],
            password=data['password'],
            jabatan=data['jabatan']
        )
        db.session.add(user)
        db.session.commit()
        return {"status":True, "message":"Berhasil menyimpan user !!!"}
    except IntegrityError as e:
        db.session.rollback()
        print("Error insert_user:", e)
        return {"status": False, "message": "User sudah terdaftar !!!"}
    except Exception as e:
        db.session.rollback() 
        print("Error insert_user:", e)
        return {"status":False, "message":"Gagal menyimpan user !!!"}