from app import db
from app.models.menu_model import Menu
from sqlalchemy import func

def get_menu_by_akses(akses):
    try:
        pattern = f"% {akses} %"
        menus = Menu.query.filter(func.concat(' ',Menu.akses_menu,' ').ilike(f"%{pattern}%")).order_by(Menu.kode_menu).all()
        return [m.to_dict() for m in menus]
    except Exception as e:
        print("Error get_menu_by_kode:", e)
        return None