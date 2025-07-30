from app import db

class Menu(db.Model):
    __tablename__ = 'ec_menus'

    kode_menu = db.Column(db.String(20), primary_key=True)
    nama_menu = db.Column(db.String(100), nullable=False)
    lvl_menu = db.Column(db.Integer, nullable=False)
    anak_menu = db.Column(db.String(20), nullable=True)
    link_menu = db.Column(db.String(100), nullable=True)
    akses_menu = db.Column(db.String(100), nullable=True)
    aksi_menu = db.Column(db.String(1), nullable=True)
    aktif_menu = db.Column(db.String(1), nullable=True)

    def to_dict(self):
        return {
            "kode_menu": self.kode_menu,
            "nama_menu": self.nama_menu,
            "lvl_menu": self.lvl_menu,
            "anak_menu": self.anak_menu,
            "link_menu": self.link_menu,
            "akses_menu": self.akses_menu,
            "aksi_menu": self.aksi_menu,
            "aktif_menu": self.aktif_menu
        }
