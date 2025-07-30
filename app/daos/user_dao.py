from app.models.user_model import Pegawai
from app import db
from sqlalchemy.exc import SQLAlchemyError

def get_pegawai_by_username(username):
    try:
        return Pegawai.query.filter_by(username=username).first()
    except SQLAlchemyError as e:
        return None

def get_all_pegawai():
    return Pegawai.query.all()

def insert_pegawai(data):
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