from app.model import HoKhau, NhanKhau, LichSuHoKhau, TamTruTamVang
from app import db
from datetime import datetime
from sqlalchemy.exc import SQLAlchemyError

class HoKhauService:
    @staticmethod
    def get_hokhau_by_soNha(soNha):
        return HoKhau.query.filter_by(soNha=soNha).first()

        
class NhanKhauService:

    @staticmethod
    def get_nhankhau_by_id(maNhanKhau):
        return NhanKhau.query.get(maNhanKhau)

        
class LichSuHoKhauService:
    
    @staticmethod
    def get_lichsuhokhau_by_id(id):
        return LichSuHoKhau.query.get(id)
    
class TamTruTamVangService:
    
    @staticmethod
    def get_tamtrutamvang_by_id(id):
        return TamTruTamVang.query.get(id)
    
        
    