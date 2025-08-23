from app import db

class Pegawai(db.Model):
    __tablename__ = 'ec_pegawai'

    nama = db.Column(db.String(100), primary_key=True)
    no_hp = db.Column(db.String(20), nullable=False)

    def __init__(self, nama, no_hp):
        self.nama = nama
        self.no_hp = no_hp

    def to_dict(self):
        return {
            'nama': self.nama,
            'no_hp': self.no_hp,
        }