from app import db

class Pegawai(db.Model):
    __tablename__ = 'ec_pegawai'
    
    id_pegawai = db.Column(db.Integer, primary_key=True)
    nama_pegawai = db.Column(db.String(100), nullable=False)
    username = db.Column(db.String(100), nullable=False, unique=True)
    password = db.Column(db.String(100), nullable=False)
    jabatan = db.Column(db.String(50), nullable=False)
    no_hp = db.Column(db.String(15), nullable=True)
    tgl_masuk = db.Column(db.Date, nullable=True)
    status = db.Column(db.String(20), nullable=False)

    def __init__(self, nama_pegawai, username, password, jabatan, no_hp, tgl_masuk, status):
        self.nama_pegawai = nama_pegawai
        self.username = username
        self.password = password
        self.jabatan = jabatan
        self.no_hp = no_hp
        self.tgl_masuk = tgl_masuk
        self.status = status

    def to_dict(self):
        return {
            'id_pegawai': self.id_pegawai,
            'nama_pegawai': self.nama_pegawai,
            'username': self.username,
            'jabatan': self.jabatan,
            'no_hp': self.no_hp,
            'tgl_masuk': self.tgl_masuk.isoformat() if self.tgl_masuk else None,
            'status': self.status
        }