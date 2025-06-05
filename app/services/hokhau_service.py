from app.model import HoKhau, NhanKhau, LichSuHoKhau, TamTruTamVang
from app import db
from datetime import datetime
from sqlalchemy.exc import SQLAlchemyError

class HoKhauService:
    @staticmethod
    def create_hokhau(chuHo, soNha, ngayLap, ngayCapNhat, dienTich, xeMay=0, oTo=0):
        try:
            if HoKhau.query.filter_by(soNha=soNha).first():
                return None
            
            new_hokhau = HoKhau(
                chuHo=chuHo,
                soNha=soNha,
                ngayLap=ngayLap,
                ngayCapNhat=ngayCapNhat,
                dienTich=dienTich,
                xeMay=xeMay,
                oTo=oTo
            )
            db.session.add(new_hokhau)
            db.session.commit()
            return new_hokhau
        
        except SQLAlchemyError as e:
            print(f"SQLAlchemyError at commit: {str(e)}")
            db.session.rollback()
            return None

    @staticmethod
    def get_hokhau_by_soNha(soNha):
        return HoKhau.query.filter_by(soNha=soNha).first()

    @staticmethod
    def get_hokhau_by_id(id):
        return HoKhau.query.get(id)
    
    @staticmethod
    def get_all_hokhaus():
        return HoKhau.query.all()
    
    @staticmethod
    def update_HoKhau(maHoKhau, chuHo, soNha, ngayLap, ngayCapNhat, dienTich, xeMay=0, oTo=0):
        try:
            hokhau = HoKhau.query.get(maHoKhau)
            if not hokhau:
                return False
            
            hokhau.chuHo = chuHo
            hokhau.soNha = soNha
            hokhau.ngayLap = ngayLap
            hokhau.ngayCapNhat = ngayCapNhat
            hokhau.dienTich = dienTich
            hokhau.xeMay = xeMay
            hokhau.oTo = oTo

            db.session.commit()
            return True
        except SQLAlchemyError:
            db.session.rollback()
            return False

    @staticmethod
    def delete_hokhau(maHoKhau):
        try:
            hokhau = HoKhau.query.get(maHoKhau)
            if not hokhau:
                return False
            
            db.session.delete(hokhau)
            db.session.commit()
            return True
        except SQLAlchemyError:
            db.session.rollback()
            return False
      
class NhanKhauService:
    @staticmethod
    def create_nhankhau(hoTen, ngaySinh, gioiTinh, maHoKhau=None, quocTich=None, noiSinh=None, cmnd=None, qhVoiChuHo=None, trangThai=None):
        try:
            new_nhankhau = NhanKhau(
                hoTen=hoTen,
                ngaySinh=ngaySinh,
                gioiTinh=gioiTinh,
                maHoKhau=maHoKhau
            )
            
            # Các trường bổ sung
            new_nhankhau.quocTich = quocTich
            new_nhankhau.noiSinh = noiSinh
            new_nhankhau.cmnd = cmnd
            new_nhankhau.qhVoiChuHo = qhVoiChuHo
            new_nhankhau.trangThai = trangThai

            db.session.add(new_nhankhau)
            db.session.commit()
            return new_nhankhau
        except SQLAlchemyError as e:
            print(f"SQLAlchemyError at create_nhankhau: {str(e)}")
            db.session.rollback()
            return None

    @staticmethod
    def get_nhankhau_by_id(maNhanKhau):
        return NhanKhau.query.get(maNhanKhau)

    @staticmethod
    def get_all_nhankhau():
        return NhanKhau.query.all()

    @staticmethod
    def get_nhankhau_by_hoKhau(maHoKhau):
        return NhanKhau.query.filter_by(maHoKhau=maHoKhau).all()

    @staticmethod
    def update_nhankhau(maNhanKhau, hoTen=None, ngaySinh=None, gioiTinh=None, maHoKhau=None, quocTich=None, noiSinh=None, cmnd=None, qhVoiChuHo=None, trangThai=None):
        try:
            nhankhau = NhanKhau.query.get(maNhanKhau)
            if not nhankhau:
                return False

            nhankhau.hoTen = hoTen or nhankhau.hoTen
            nhankhau.ngaySinh = ngaySinh or nhankhau.ngaySinh
            nhankhau.gioiTinh = gioiTinh or nhankhau.gioiTinh
            nhankhau.maHoKhau = maHoKhau if maHoKhau is not None else nhankhau.maHoKhau
            nhankhau.quocTich = quocTich or nhankhau.quocTich
            nhankhau.noiSinh = noiSinh or nhankhau.noiSinh
            nhankhau.cmnd = cmnd or nhankhau.cmnd
            nhankhau.qhVoiChuHo = qhVoiChuHo or nhankhau.qhVoiChuHo
            nhankhau.trangThai = trangThai or nhankhau.trangThai

            db.session.commit()
            return True
        except SQLAlchemyError as e:
            print(f"SQLAlchemyError at update_nhankhau: {str(e)}")
            db.session.rollback()
            return False

    @staticmethod
    def delete_nhankhau(maNhanKhau):
        try:
            nhankhau = NhanKhau.query.get(maNhanKhau)
            if not nhankhau:
                return False

            db.session.delete(nhankhau)
            db.session.commit()
            return True
        except SQLAlchemyError as e:
            print(f"SQLAlchemyError at delete_nhankhau: {str(e)}")
            db.session.rollback()
            return False

class LichSuHoKhauService:
    @staticmethod
    def create_lichsuhokhau(loaiThayDoi, maHoKhau, maNhanKhau, thoiGian, noiDung):
        try:
            # Nếu loại thay đổi là xóa thì mã nhân khẩu để bằng 0
            if loaiThayDoi.lower() == "xóa":
                maNhanKhau = 0
                
            new_lichsuhokhau = LichSuHoKhau(
                loaiThayDoi=loaiThayDoi,
                maHoKhau=maHoKhau,
                maNhanKhau=maNhanKhau,
                thoiGian=thoiGian,
                noiDung=noiDung
            )
            
            db.session.add(new_lichsuhokhau)
            db.session.commit()
            return new_lichsuhokhau
        except SQLAlchemyError as e:
            print(f"SQLAlchemyError at create_lichsuhokhau: {str(e)}")
            db.session.rollback()
            return None
    
    @staticmethod
    def get_lichsuhokhau_by_id(id):
        return LichSuHoKhau.query.get(id)
    
    @staticmethod
    def get_all_lichsuhokhau():
        return LichSuHoKhau.query.all()
    
    @staticmethod
    def get_lichsuhokhau_by_hokhau(maHoKhau):
        return LichSuHoKhau.query.filter_by(maHoKhau=maHoKhau).all()
    
    @staticmethod
    def get_lichsuhokhau_by_nhankhau(maNhanKhau):
        return LichSuHoKhau.query.filter_by(maNhanKhau=maNhanKhau).all()
    
    @staticmethod
    def get_lichsuhokhau_by_type(loaiThayDoi):
        return LichSuHoKhau.query.filter_by(loaiThayDoi=loaiThayDoi).all()
    
class TamTruTamVangService:
    @staticmethod
    def create_tamtrutamvang(loai, maNhanKhau, ngayBatDau=None, ngayKetThuc=None, lyDo=None):
        try:
            new_tamtrutamvang = TamTruTamVang(
                loai=loai,
                maNhanKhau=maNhanKhau,
                ngayBatDau=ngayBatDau,
                ngayKetThuc=ngayKetThuc,
                lyDo=lyDo
            )
            
            db.session.add(new_tamtrutamvang)
            db.session.commit()
            return new_tamtrutamvang
        except SQLAlchemyError as e:
            print(f"SQLAlchemyError at create_tamtrutamvang: {str(e)}")
            db.session.rollback()
            return None
    
    @staticmethod
    def get_tamtrutamvang_by_id(id):
        return TamTruTamVang.query.get(id)
    
    @staticmethod
    def get_all_tamtrutamvang():
        return TamTruTamVang.query.all()
    
    @staticmethod
    def get_tamtrutamvang_by_nhankhau(maNhanKhau):
        return TamTruTamVang.query.filter_by(maNhanKhau=maNhanKhau).all()
    
    @staticmethod
    def get_tamtrutamvang_by_type(loai):
        return TamTruTamVang.query.filter_by(loai=loai).all()
    
    @staticmethod
    def get_active_tamtrutamvang(current_date=None):
        if current_date is None:
            current_date = datetime.now().date()
        return TamTruTamVang.query.filter(
            TamTruTamVang.ngayBatDau <= current_date,
            TamTruTamVang.ngayKetThuc >= current_date
        ).all()
    @staticmethod
    def get_all_tamtrutamvang_with_nhankhau():
        return db.session.query(
            TamTruTamVang.id,
            TamTruTamVang.loai,
            TamTruTamVang.maNhanKhau,
            TamTruTamVang.ngayBatDau,
            TamTruTamVang.ngayKetThuc,
            TamTruTamVang.lyDo,
            NhanKhau.hoTen,
            NhanKhau.qhVoiChuHo,
            NhanKhau.maHoKhau,
            NhanKhau.ngaySinh,
            NhanKhau.gioiTinh,
            NhanKhau.quocTich,
            NhanKhau.noiSinh,
            NhanKhau.cmnd
        ).join(NhanKhau, TamTruTamVang.maNhanKhau == NhanKhau.maNhanKhau).all()
    
    @staticmethod
    def update_tamtrutamvang(id, loai, ngayBatDau, ngayKetThuc, lyDo):
        try:
            tamtrutamvang = TamTruTamVang.query.get(id)
            if not tamtrutamvang:
                return False
            
            tamtrutamvang.loai = loai or tamtrutamvang.loai
            tamtrutamvang.ngayBatDau = ngayBatDau or tamtrutamvang.ngayBatDau
            tamtrutamvang.ngayKetThuc = ngayKetThuc or tamtrutamvang.ngayKetThuc
            tamtrutamvang.lyDo = lyDo or tamtrutamvang.lyDo
            
            db.session.commit()
            return True
        except SQLAlchemyError as e:
            print(f"SQLAlchemyError at update_tamtrutamvang: {str(e)}")
            db.session.rollback()
            return False
    
    @staticmethod
    def delete_tamtrutamvang(id):
        try:
            tamtrutamvang = TamTruTamVang.query.get(id)
            if not tamtrutamvang:
                return False
            
            db.session.delete(tamtrutamvang)
            db.session.commit()
            return True
        except SQLAlchemyError as e:
            print(f"SQLAlchemyError at delete_tamtrutamvang: {str(e)}")
            db.session.rollback()
            return False
    
        
