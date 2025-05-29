from app.model import *
from app import db
from datetime import datetime
from sqlalchemy.exc import SQLAlchemyError
from datetime import date
from sqlalchemy.sql import extract
class KhoanThuService:
    
    @staticmethod
    def get_khoanthu_by_id(maKhoanThu):
        return KhoanThu.query.get(maKhoanThu)

class DotThuService:
    
    @staticmethod
    def get_dotthu_by_name(tenDotThu):
        return DotThu.query.filter_by(tenDotThu=tenDotThu).first()



class KhoanThuHasDotThuService:
    
    @staticmethod
    def get_by_id(idKhoanThuDotThu):
        return KhoanThu_Has_DotThu.query.get(idKhoanThuDotThu)

class NopPhiService:
    
    @staticmethod
    def get_nopphi_by_id(IDNopTien):
        return NopPhi.query.get(IDNopTien)
