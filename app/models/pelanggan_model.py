from app import db

class Pelanggan(db.Model):
    __tablename__ = 'ec_pelanggan'

    nopol = db.Column(db.String(20), primary_key=True)
    nama_pelanggan = db.Column(db.String(100), nullable=False)
    nama_kendaraan = db.Column(db.String(100), nullable=False)
    no_hp = db.Column(db.String(20), nullable=True)

    def __init__(self, nopol, nama_pelanggan, nama_kendaraan, no_hp=None):
        self.nopol = nopol
        self.nama_pelanggan = nama_pelanggan
        self.nama_kendaraan = nama_kendaraan
        self.no_hp = no_hp

    def to_dict(self):
        return {
            'nopol': self.nopol,
            'nama_pelanggan': self.nama_pelanggan,
            'nama_kendaraan': self.nama_kendaraan,
            'no_hp': self.no_hp
        }