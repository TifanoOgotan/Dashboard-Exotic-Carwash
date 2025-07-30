from app.models.produk_model import Produk
from app import db
from sqlalchemy.exc import SQLAlchemyError

def get_all_produk():
    try:
        produks = Produk.query.all()
        return [p.to_dict() for p in produks]
    except Exception as e:
        print("Error get_all_produk:", e)
        return None