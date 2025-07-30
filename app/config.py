import os 

class Config:
    SECRET_KEY = 'ini_rahasiamu'  # ganti untuk production
    SQLALCHEMY_DATABASE_URI = 'postgresql://postgres:ifan@localhost:5432/postgres'
    SQLALCHEMY_TRACK_MODIFICATIONS = False