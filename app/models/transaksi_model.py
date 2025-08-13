from app import db
from datetime import date
from sqlalchemy import Column, String, Integer, Date, ForeignKeyConstraint
from sqlalchemy.orm import relationship

class Transaksi(db.Model):
    __tablename__ = 'ec_transaksi'

    id_transaksi = db.Column(db.String(8), primary_key=True)
    tanggal = db.Column(db.Date, primary_key=True)
    nopol = db.Column(db.String(20), db.ForeignKey("ec_pelanggan.nopol"))
    status_bayar = db.Column(db.String(2), nullable=False)
    total_harga = db.Column(db.Integer, nullable=False)
    details = relationship("DetailTransaksi", back_populates="transaksi",cascade="all, delete-orphan")
    pelanggan = relationship("Pelanggan", backref="transaksi")

    def __init__(self, id_transaksi, tanggal, nopol, status_bayar, total_harga):
        self.id_transaksi = id_transaksi
        self.tanggal = tanggal
        self.nopol = nopol
        self.status_bayar = status_bayar
        self.total_harga = total_harga

    def to_dict(self, include_details=True):
        data = {
            "id_transaksi": self.id_transaksi,
            "tanggal": self.tanggal.strftime("%d-%b-%Y"),
            "nopol": self.nopol,
            "status_bayar": self.status_bayar,
            "total_harga": self.total_harga
        }

        if include_details:
            data["details"] = [
                detail.to_dict() if hasattr(detail, "to_dict") else {
                    "id": detail.id,
                    "id_produk": detail.id_produk,
                    "nama_produk": detail.nama_produk,
                    "jenis": detail.jenis,
                    "harga": detail.harga,
                    "jumlah": detail.jumlah,
                    "worker": detail.worker,
                    "total": detail.total
                }
                for detail in self.details
            ]

        return data

class DetailTransaksi(db.Model):
    __tablename__ = 'ec_detail_transaksi'

    id = Column(Integer, primary_key=True, autoincrement=True)
    id_transaksi = Column(String(8), nullable=False)
    tanggal = Column(Date, nullable=False)
    id_produk = Column(String(20), nullable=False)
    nama_produk = Column(String(100), nullable=False)
    jenis = Column(String(20), nullable=False)
    harga = Column(Integer, nullable=False)
    jumlah = Column(Integer, nullable=False)
    worker = Column(String(50))
    total = Column(Integer, nullable=False)

    __table_args__ = (
        ForeignKeyConstraint(
            ['id_transaksi', 'tanggal'],
            ['ec_transaksi.id_transaksi', 'ec_transaksi.tanggal']
        ),
    )

    transaksi = relationship("Transaksi", back_populates="details")
    
    def __init__(self, id_transaksi, tanggal, id_produk, nama_produk, jenis, harga, jumlah, worker, total):
        self.id_transaksi = id_transaksi
        self.tanggal = tanggal
        self.id_produk = id_produk
        self.nama_produk = nama_produk
        self.jenis = jenis
        self.harga = harga
        self.jumlah = jumlah
        self.worker = worker
        self.total = total

    def to_dict(self):
        return {
            "id": self.id,
            "id_transaksi": self.id_transaksi,
            "tanggal": self.tanggal.strftime("%d-%b-%Y"),
            "id_produk": self.id_produk,
            "nama_produk": self.nama_produk,
            "jenis": self.jenis,
            "harga": float(self.harga),
            "jumlah": self.jumlah,
            "worker": self.worker,
            "total": float(self.total)
        }