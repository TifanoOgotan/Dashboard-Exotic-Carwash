from app import db

class Produk(db.Model):
    __tablename__ = 'ec_produk'

    id_produk = db.Column(db.String(100), primary_key=True)
    nama_produk = db.Column(db.String(100), nullable=False)
    jenis = db.Column(db.String(20), nullable=False)
    harga = db.Column(db.Integer, nullable=False)
    stok = db.Column(db.Integer, nullable=False)

    def __init__(self, id_produk, nama_produk, jenis, harga, stok):
        self.id_produk = id_produk
        self.nama_produk = nama_produk
        self.jenis = jenis
        self.harga = harga
        self.stok = stok

    def to_dict(self):
        return {
            'id_produk': self.id_produk,
            'nama_produk': self.nama_produk,
            'jenis': self.jenis,
            'harga': self.harga,
            'stok': self.stok
        }