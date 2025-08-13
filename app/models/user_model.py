from app import db

class User(db.Model):
    __tablename__ = 'ec_akses'
    
    id = db.Column(db.Integer, primary_key=True)
    nama = db.Column(db.String(100), nullable=False)
    username = db.Column(db.String(100), nullable=False, unique=True)
    password = db.Column(db.String(100), nullable=False)
    jabatan = db.Column(db.String(50), nullable=False)

    def __init__(self, nama, username, password, jabatan):
        self.nama = nama
        self.username = username
        self.password = password
        self.jabatan = jabatan

    def to_dict(self):
        return {
            'id': self.id,
            'nama': self.nama,
            'username': self.username,
            'jabatan': self.jabatan
        }