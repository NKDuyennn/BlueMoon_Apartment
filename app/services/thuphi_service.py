from app.model import *
from app import db
from datetime import datetime
from sqlalchemy.exc import SQLAlchemyError
from datetime import date
from sqlalchemy.sql import extract
class KhoanThuService:
    @staticmethod
    def create_khoanthu(tenKhoanThu, loaiKhoanThu, soTien, loaiSoTien, ghiChu, idNguoiTao):
        try:
            new_khoanthu = KhoanThu(
                tenKhoanThu=tenKhoanThu,
                loaiKhoanThu=loaiKhoanThu,
                soTien=soTien,
                loaiSoTien=loaiSoTien,
                ghiChu=ghiChu,
                idNguoiTao=idNguoiTao
            )
            db.session.add(new_khoanthu)
            db.session.commit()
            return new_khoanthu
        except SQLAlchemyError as e:
            print(f"SQLAlchemyError at create_khoanthu: {str(e)}")
            db.session.rollback()
            return None

    @staticmethod
    def get_khoanthu_by_id(maKhoanThu):
        return KhoanThu.query.get(maKhoanThu)

    @staticmethod
    def get_all_khoanthus():
        return KhoanThu.query.all()
    
    @staticmethod
    def get_khoanthus_by_loai(loaiKhoanThu):
        return KhoanThu.query.filter_by(loaiKhoanThu=loaiKhoanThu).all()
    
    @staticmethod
    def get_khoanthus_by_nguoitao(idNguoiTao):
        return KhoanThu.query.filter_by(idNguoiTao=idNguoiTao).all()

    @staticmethod
    def update_khoanthu(maKhoanThu, tenKhoanThu=None, loaiKhoanThu=None, soTien=None, loaiSoTien=None, ghiChu=None):
        try:
            khoanthu = KhoanThu.query.get(maKhoanThu)
            if not khoanthu:
                return False
            
            khoanthu.tenKhoanThu = tenKhoanThu or khoanthu.tenKhoanThu
            khoanthu.loaiKhoanThu = loaiKhoanThu or khoanthu.loaiKhoanThu
            khoanthu.soTien = soTien if soTien is not None else khoanthu.soTien
            khoanthu.loaiSoTien = loaiSoTien or khoanthu.loaiSoTien
            khoanthu.ghiChu = ghiChu or khoanthu.ghiChu
            
            db.session.commit()
            return True
        except SQLAlchemyError as e:
            print(f"SQLAlchemyError at update_khoanthu: {str(e)}")
            db.session.rollback()
            return False

    @staticmethod
    def delete_khoanthu(maKhoanThu):
        try:
            khoanthu = KhoanThu.query.get(maKhoanThu)
            if not khoanthu:
                return False
            
            db.session.delete(khoanthu)
            db.session.commit()
            return True
        except SQLAlchemyError as e:
            print(f"SQLAlchemyError at delete_khoanthu: {str(e)}")
            db.session.rollback()
            return False

class DotThuService:
    @staticmethod
    def create_dotthu(tenDotThu, ngayBatDau, ngayKetThuc, trangThai="Đang thực hiện"):
        try:
            if DotThu.query.filter_by(tenDotThu=tenDotThu).first():
                return None
                
            new_dotthu = DotThu(
                tenDotThu=tenDotThu,
                ngayBatDau=ngayBatDau,
                ngayKetThuc=ngayKetThuc,
                trangThai=trangThai
            )
            db.session.add(new_dotthu)
            db.session.commit()
            return new_dotthu
            
        except SQLAlchemyError as e:
            print(f"SQLAlchemyError at commit: {str(e)}")
            db.session.rollback()
            return None
    
    @staticmethod
    def get_dotthu_by_name(tenDotThu):
        return DotThu.query.filter_by(tenDotThu=tenDotThu).first()
    
    @staticmethod
    def get_dotthu_by_id(maDotThu):
        return DotThu.query.get(maDotThu)
        
    @staticmethod
    def get_all_dotthus():
        return DotThu.query.all()
        
    @staticmethod
    def update_dotthu(maDotThu, tenDotThu, ngayBatDau, ngayKetThuc, trangThai):
        try:
            dotthu = DotThu.query.get(maDotThu)
            if not dotthu:
                return False
                
            dotthu.tenDotThu = tenDotThu
            dotthu.ngayBatDau = ngayBatDau
            dotthu.ngayKetThuc = ngayKetThuc
            dotthu.trangThai = trangThai
            
            db.session.commit()
            return True
        except SQLAlchemyError:
            db.session.rollback()
            return False
    
    @staticmethod
    def delete_dotthu(maDotThu):
        try:
            dotthu = DotThu.query.get(maDotThu)
            if not dotthu:
                return False
                
            db.session.delete(dotthu)
            db.session.commit()
            return True
        except SQLAlchemyError:
            db.session.rollback()
            return False
    
    @staticmethod
    def get_active_dotthus():
        return DotThu.query.filter_by(trangThai="Đang thực hiện").all()
    
    @staticmethod
    def get_dotthus_by_status(trangThai):
        return DotThu.query.filter_by(trangThai=trangThai).all()
    
    @staticmethod
    def update_status(maDotThu, trangThai):
        try:
            dotthu = DotThu.query.get(maDotThu)
            if not dotthu:
                return False
                
            dotthu.trangThai = trangThai
            
            db.session.commit()
            return True
        except SQLAlchemyError:
            db.session.rollback()
            return False
    @staticmethod
    def sodotthu(current_year,current_month):
        dotthu = db.session.query(DotThu).filter(
                (extract('year', DotThu.ngayBatDau) == current_year),
                (extract('month', DotThu.ngayBatDau) == current_month)
            ).count()
        return dotthu



class KhoanThuHasDotThuService:
    @staticmethod
    def create_khoanthu_has_dotthu(maKhoanThu, maDotThu):
        try:
            khoanthu = KhoanThu.query.get(maKhoanThu)
            dotthu = DotThu.query.get(maDotThu)
            if not khoanthu or not dotthu:
                return None
            
            existing = KhoanThu_Has_DotThu.query.filter_by(
                maKhoanThu=maKhoanThu, 
                maDotThu=maDotThu
            ).first()
            if existing:
                return existing
            
            new_khoanthu_has_dotthu = KhoanThu_Has_DotThu(
                maKhoanThu=maKhoanThu,
                maDotThu=maDotThu
            )
            db.session.add(new_khoanthu_has_dotthu)
            db.session.commit()
            return new_khoanthu_has_dotthu
        except SQLAlchemyError as e:
            print(f"SQLAlchemyError at create_khoanthu_has_dotthu: {str(e)}")
            db.session.rollback()
            return None

    @staticmethod
    def get_by_id(idKhoanThuDotThu):
        return KhoanThu_Has_DotThu.query.get(idKhoanThuDotThu)

    @staticmethod
    def get_all():
        return KhoanThu_Has_DotThu.query.all()
    
    @staticmethod
    def get_by_khoanthu(maKhoanThu):
        return KhoanThu_Has_DotThu.query.filter_by(maKhoanThu=maKhoanThu).all()
    
    @staticmethod
    def get_by_dotthu(maDotThu):
        return KhoanThu_Has_DotThu.query.filter_by(maDotThu=maDotThu).all()
    
    @staticmethod
    def get_khoanthu_dotthu_details():
        return db.session.query(
            KhoanThu_Has_DotThu.idKhoanThuDotThu,
            KhoanThu.maKhoanThu,
            KhoanThu.tenKhoanThu,
            KhoanThu.loaiKhoanThu,
            KhoanThu.soTien,
            KhoanThu.loaiSoTien,
            DotThu.maDotThu,
            DotThu.tenDotThu,
            DotThu.ngayBatDau,
            DotThu.ngayKetThuc,
            DotThu.trangThai
        ).join(
            KhoanThu, KhoanThu_Has_DotThu.maKhoanThu == KhoanThu.maKhoanThu
        ).join(
            DotThu, KhoanThu_Has_DotThu.maDotThu == DotThu.maDotThu
        ).all()

    @staticmethod
    def delete(idKhoanThuDotThu):
        try:
            khoanthu_has_dotthu = KhoanThu_Has_DotThu.query.get(idKhoanThuDotThu)
            if not khoanthu_has_dotthu:
                return False
            
            db.session.delete(khoanthu_has_dotthu)
            db.session.commit()
            return True
        except SQLAlchemyError as e:
            print(f"SQLAlchemyError at delete KhoanThu_Has_DotThu: {str(e)}")
            db.session.rollback()
            return False

class NopPhiService:
    @staticmethod
    def calculate_so_tien_can_nop(khoanthu, hokhau):
        """Tính số tiền cần nộp dựa trên loại khoản thu và thông tin hộ khẩu"""
        dien_tich = hokhau.dienTich or 0
        xe_may = hokhau.xeMay or 0
        o_to = hokhau.oTo or 0
        
        if khoanthu.loaiKhoanThu in ["Phí dịch vụ", "Phí quản lý"]:
            return khoanthu.soTien * max(dien_tich, 0)
        elif khoanthu.loaiKhoanThu == "Phí xe máy":
            return khoanthu.soTien * max(xe_may, 0)
        elif khoanthu.loaiKhoanThu == "Phí ô tô":
            return khoanthu.soTien * max(o_to, 0)
        elif khoanthu.loaiKhoanThu == "Đóng góp":
            return 0
        else:  # "Khác"
            return 0

    @staticmethod
    def create_nopphi_for_hokhau(maHoKhau, idKhoanThuDotThu, nguoiNop, idNguoiThu):
        try:
            khoanthu_has_dotthu = KhoanThu_Has_DotThu.query.get(idKhoanThuDotThu)
            if not khoanthu_has_dotthu:
                return None
            
            hokhau = HoKhau.query.get(maHoKhau)
            if not hokhau:
                return None
            
            khoanthu = KhoanThu.query.get(khoanthu_has_dotthu.maKhoanThu)
            so_tien_can_nop = NopPhiService.calculate_so_tien_can_nop(khoanthu, hokhau)
            
            existing_nopphi = NopPhi.query.filter_by(
                idKhoanThuDotThu=idKhoanThuDotThu,
                maHoKhau=maHoKhau
            ).first()
            if existing_nopphi:
                return existing_nopphi
            
            new_nopphi = NopPhi(
                soTienCanNop=so_tien_can_nop,
                soTienDaNop=0,
                nguoiNop=nguoiNop,
                idKhoanThuDotThu=idKhoanThuDotThu,
                maHoKhau=maHoKhau,
                idNguoiThu=idNguoiThu,
                ngayThu=None
            )
            db.session.add(new_nopphi)
            db.session.commit()
            return new_nopphi
        except SQLAlchemyError as e:
            print(f"SQLAlchemyError at create_nopphi_for_hokhau: {str(e)}")
            db.session.rollback()
            return None

    @staticmethod
    def create_multiple_nopphi_for_hokhau(maHoKhau, maDotThu, nguoiNop, idNguoiThu):
        """Tạo bản ghi nộp phí cho một hộ khẩu với tất cả khoản thu trong đợt thu"""
        try:
            khoanthu_dotthus = KhoanThuHasDotThuService.get_by_dotthu(maDotThu)
            if not khoanthu_dotthus:
                return []
            
            hokhau = HoKhau.query.get(maHoKhau)
            if not hokhau:
                return []
            
            created_nopphis = []
            for kt_dt in khoanthu_dotthus:
                nopphi = NopPhiService.create_nopphi_for_hokhau(
                    maHoKhau=maHoKhau,
                    idKhoanThuDotThu=kt_dt.idKhoanThuDotThu,
                    nguoiNop=nguoiNop,
                    idNguoiThu=idNguoiThu
                )
                if nopphi:
                    created_nopphis.append(nopphi)
            
            return created_nopphis
        except SQLAlchemyError as e:
            print(f"SQLAlchemyError at create_multiple_nopphi_for_hokhau: {str(e)}")
            db.session.rollback()
            return []

    @staticmethod
    def create_nopphi(soTienDaNop, nguoiNop, idKhoanThuDotThu, maHoKhau, idNguoiThu, ngayThu=None):
        try:
            khoanthu_has_dotthu = KhoanThu_Has_DotThu.query.get(idKhoanThuDotThu)
            if not khoanthu_has_dotthu:
                return None
            
            hokhau = HoKhau.query.get(maHoKhau)
            if not hokhau:
                return None
            
            khoanthu = KhoanThu.query.get(khoanthu_has_dotthu.maKhoanThu)
            so_tien_can_nop = NopPhiService.calculate_so_tien_can_nop(khoanthu, hokhau)
            
            new_nopphi = NopPhi(
                soTienDaNop=soTienDaNop,
                soTienCanNop=so_tien_can_nop,
                nguoiNop=nguoiNop,
                idKhoanThuDotThu=idKhoanThuDotThu,
                maHoKhau=maHoKhau,
                idNguoiThu=idNguoiThu,
                ngayThu=ngayThu if ngayThu else datetime.now().date()
            )
            db.session.add(new_nopphi)
            db.session.commit()
            return new_nopphi
        except SQLAlchemyError as e:
            print(f"SQLAlchemyError at create_nopphi: {str(e)}")
            db.session.rollback()
            return None

    @staticmethod
    def get_nopphi_by_id(IDNopTien):
        return NopPhi.query.get(IDNopTien)

    @staticmethod
    def get_all_nopphis():
        return NopPhi.query.all()
    
    @staticmethod
    def get_nopphis_by_hokhau(maHoKhau):
        return NopPhi.query.filter_by(maHoKhau=maHoKhau).all()
    
    @staticmethod
    def get_nopphis_by_khoanthu_dotthu(idKhoanThuDotThu):
        return NopPhi.query.filter_by(idKhoanThuDotThu=idKhoanThuDotThu).all()
    
    @staticmethod
    def get_nopphis_by_nguoithu(idNguoiThu):
        return NopPhi.query.filter_by(idNguoiThu=idNguoiThu).all()
    
    @staticmethod
    def get_nopphis_by_date_range(start_date, end_date):
        return NopPhi.query.filter(
            NopPhi.ngayThu >= start_date,
            NopPhi.ngayThu <= end_date
        ).all()
    
    @staticmethod
    def get_nopphis_with_details(maDotThu):
        results = db.session.query(
            NopPhi.IDNopTien,
            NopPhi.ngayThu,
            NopPhi.soTienDaNop,
            NopPhi.soTienCanNop,
            NopPhi.nguoiNop,
            NopPhi.idNguoiThu,
            NopPhi.maHoKhau,
            KhoanThu.maKhoanThu,  # Thay đổi từ tenKhoanThu thành maKhoanThu để khớp với giao diện
            KhoanThu.loaiKhoanThu,
            DotThu.tenDotThu
        ).join(
            KhoanThu_Has_DotThu, NopPhi.idKhoanThuDotThu == KhoanThu_Has_DotThu.idKhoanThuDotThu
        ).join(
            KhoanThu, KhoanThu_Has_DotThu.maKhoanThu == KhoanThu.maKhoanThu
        ).join(
            DotThu, KhoanThu_Has_DotThu.maDotThu == DotThu.maDotThu
        ).filter(
            KhoanThu_Has_DotThu.maDotThu == maDotThu
        ).all()
        
        # Tổ chức dữ liệu theo hộ khẩu
        hokhau_data = {}
        for row in results:
            maHoKhau = row.maHoKhau
            if maHoKhau not in hokhau_data:
                hokhau_data[maHoKhau] = {
                    'maHoKhau': maHoKhau,
                    'khoanThus': {}
                }
            hokhau_data[maHoKhau]['khoanThus'][str(row.maKhoanThu)] = {  # Sử dụng maKhoanThu làm key
                'IDNopTien': row.IDNopTien,
                'soTienDaNop': row.soTienDaNop,
                'soTienCanNop': row.soTienCanNop,
                'ngayThu': row.ngayThu,
                'nguoiNop': row.nguoiNop
            }
        
        return list(hokhau_data.values())

    @staticmethod
    def update_nopphi(IDNopTien, soTienDaNop=None, nguoiNop=None):
        try:
            nopphi = NopPhi.query.get(IDNopTien)
            if not nopphi:
                return False
            
            if soTienDaNop is not None:
                nopphi.soTienDaNop = soTienDaNop
                if soTienDaNop > 0 and not nopphi.ngayThu:
                    nopphi.ngayThu = datetime.now().date()
            if nguoiNop is not None:
                nopphi.nguoiNop = nguoiNop
            
            db.session.commit()
            return True
        except SQLAlchemyError as e:
            print(f"SQLAlchemyError at update_nopphi: {str(e)}")
            db.session.rollback()
            return False

    @staticmethod
    def delete_nopphi(IDNopTien):
        try:
            nopphi = NopPhi.query.get(IDNopTien)
            if not nopphi:
                return False
            
            db.session.delete(nopphi)
            db.session.commit()
            return True
        except SQLAlchemyError as e:
            print(f"SQLAlchemyError at delete_nopphi: {str(e)}")
            db.session.rollback()
            return False
    
    @staticmethod
    def get_total_by_khoanthu(maKhoanThu):
        total = db.session.query(db.func.sum(NopPhi.soTienDaNop)).join(
            KhoanThu_Has_DotThu, NopPhi.idKhoanThuDotThu == KhoanThu_Has_DotThu.idKhoanThuDotThu
        ).filter(
            KhoanThu_Has_DotThu.maKhoanThu == maKhoanThu
        ).scalar()
        return total or 0
    
    @staticmethod
    def get_total_by_dotthu(maDotThu):
        total = db.session.query(db.func.sum(NopPhi.soTienDaNop)).join(
            KhoanThu_Has_DotThu, NopPhi.idKhoanThuDotThu == KhoanThu_Has_DotThu.idKhoanThuDotThu
        ).filter(
            KhoanThu_Has_DotThu.maDotThu == maDotThu
        ).scalar()
        return total or 0
    @staticmethod
    def gettongtiensecosaukhithuhet(year,month):
        total = db.session.query(db.func.sum(NopPhi.soTienCanNop)).filter(
            (extract('year', NopPhi.ngayThu) == year),
            (extract('month', NopPhi.ngayThu) == month)                 
        ).scalar()
        return round(total or 0,0)
    @staticmethod
    def getsotiendathuduochientai(year,month):
        total = db.session.query(db.func.sum(NopPhi.soTienDaNop)).filter(
            (extract('year', NopPhi.ngayThu) == year),
            (extract('month', NopPhi.ngayThu) == month)                 
        ).scalar()
        return round(total or 0,0)
    @staticmethod
    def tylethuhientai(year,month):
        danop = db.session.query(NopPhi).filter(
            (NopPhi.soTienCanNop - NopPhi.soTienDaNop == 0),
            (extract('year', NopPhi.ngayThu) == year),
            (extract('month', NopPhi.ngayThu) == month)                
        ).count()
        phainop = db.session.query(NopPhi).filter(
            (extract('year', NopPhi.ngayThu) == year),
            (extract('month', NopPhi.ngayThu) == month)                
        ).count()
        hochuadong = phainop-danop
        return round(danop*100/phainop or 0.00, 2),hochuadong

    @staticmethod
    def doanhthutheothang(year,month):
        sotien = db.session.query(db.func.sum(NopPhi.soTienDaNop)).filter(
                (extract('year', NopPhi.ngayThu) == year),
                (extract('month', NopPhi.ngayThu) == month)            
        ).scalar()
        return sotien if sotien is not None else 0