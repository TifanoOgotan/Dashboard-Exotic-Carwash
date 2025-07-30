from app import db

class Pegawai(db.Model):
    __tablename__ = 'ec_pegawai'  # sesuai nama tabel di PostgreSQL (huruf kecil semua lebih aman)

    id_pegawai = db.Column(db.Integer, primary_key=True)
    nama_pegawai = db.Column(db.String(100))
    username = db.Column(db.String(100))
    password = db.Column(db.String(100))
    jabatan = db.Column(db.String(50))
    no_hp = db.Column(db.String(15))
    tgl_masuk = db.Column(db.Date)
    status = db.Column(db.String(20)) 