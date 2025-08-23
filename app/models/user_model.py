from app import db

class User(db.Model):
    __tablename__ = 'ec_akses'
    
    nama = db.Column(db.String(100), nullable=False)
    username = db.Column(db.String(100), nullable=False, primary_key=True)
    password = db.Column(db.String(100), nullable=False)
    jabatan = db.Column(db.String(50), nullable=False)

    def __init__(self, username, password, nama, jabatan):
        self.nama = nama
        self.username = username
        self.password = password
        self.jabatan = jabatan

    def to_dict(self):
        return {
            'nama': self.nama,
            'username': self.username,
            'password': self.password,
            'jabatan': self.jabatan
        }
    