from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
from app.extension import db
from flask_login import UserMixin

class TaiKhoan(db.Model, UserMixin):
    __tablename__ = 'taikhoan'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)
    vaiTro = db.Column(db.String(50))
    hoTen = db.Column(db.String(100))
    
    # Relationships
    nopphis = db.relationship('NopPhi', backref='taikhoan', lazy=True)
    
    def __init__(self, username, password, vaiTro, hoTen):
        self.username = username
        self.password = password
        self.vaiTro = vaiTro
        self.hoTen = hoTen
    
    def set_password(self, password):
        self.password = generate_password_hash(password)
        
    def check_password(self, password):
        return check_password_hash(self.password, password)
    
    def __repr__(self):
        return f'<TaiKhoan {self.username}>'


class KhoanThu(db.Model):
    __tablename__ = 'khoanthu'
    
    maKhoanThu = db.Column(db.Integer, primary_key=True)
    tenKhoanThu = db.Column(db.String(100), nullable=False)
    loaiKhoanThu = db.Column(db.String(50))     # "Phí dịch vụ", "Phí quản lý", "Phí xe máy", "Phí ô tô", "Khác", "Đóng góp"
    soTien = db.Column(db.Float)
    loaiSoTien = db.Column(db.String(50))  # "VNĐ"
    ghiChu = db.Column(db.String(1000))     # "/m2"
    idNguoiTao = db.Column(db.Integer, db.ForeignKey('taikhoan.id'))
    
    # Relationships
    nguoiTao = db.relationship("TaiKhoan", backref="cacKhoanThu")
    khoanthu_has_dotthus = db.relationship('KhoanThu_Has_DotThu', backref='khoanthu', lazy=True)
    
    def __init__(self, tenKhoanThu, loaiKhoanThu, soTien, loaiSoTien, ghiChu, idNguoiTao):
        self.tenKhoanThu = tenKhoanThu
        self.loaiKhoanThu = loaiKhoanThu
        self.soTien = soTien
        self.loaiSoTien = loaiSoTien
        self.ghiChu = ghiChu
        self.idNguoiTao = idNguoiTao
    
    def __repr__(self):
        return f'<KhoanThu {self.tenKhoanThu}>'

class DotThu(db.Model):
    __tablename__ = 'dotthu'
    
    maDotThu = db.Column(db.Integer, primary_key=True)
    tenDotThu = db.Column(db.String(100), nullable=False)
    ngayBatDau = db.Column(db.Date)
    ngayKetThuc = db.Column(db.Date)
    trangThai = db.Column(db.String(50))
    
    # Relationships
    khoanthu_has_dotthus = db.relationship('KhoanThu_Has_DotThu', backref='dotthu', lazy=True)
    
    def __init__(self, tenDotThu, ngayBatDau, ngayKetThuc, trangThai="Đang thực hiện"):
        self.tenDotThu = tenDotThu
        self.ngayBatDau = ngayBatDau
        self.ngayKetThuc = ngayKetThuc
        self.trangThai = trangThai
    
    def __repr__(self):
        return f'<DotThu {self.tenDotThu}>'


class KhoanThu_Has_DotThu(db.Model):
    __tablename__ = 'khoanthu_has_dotthu'
    
    idKhoanThuDotThu = db.Column(db.Integer, primary_key=True)
    maKhoanThu = db.Column(db.Integer, db.ForeignKey('khoanthu.maKhoanThu'))
    maDotThu = db.Column(db.Integer, db.ForeignKey('dotthu.maDotThu'))
    
    # Relationships
    nopphis = db.relationship('NopPhi', backref='khoanthu_has_dotthu', lazy=True)
    
    def __init__(self, maKhoanThu, maDotThu):
        self.maKhoanThu = maKhoanThu
        self.maDotThu = maDotThu
    
    def __repr__(self):
        return f'<KhoanThu_Has_DotThu {self.idKhoanThuDotThu}>'


class NopPhi(db.Model):
    __tablename__ = 'nopphi'
    
    IDNopTien = db.Column(db.Integer, primary_key=True)
    ngayThu = db.Column(db.Date, nullable=True)
    soTienDaNop = db.Column(db.Float, nullable=False, default=0.0)
    soTienCanNop = db.Column(db.Float, nullable=False, default=0.0)
    nguoiNop = db.Column(db.String(100), nullable=True)
    idNguoiThu = db.Column(db.Integer, db.ForeignKey('taikhoan.id'), nullable=True)
    maHoKhau = db.Column(db.Integer, db.ForeignKey('hokhau.maHoKhau'), nullable=False)
    idKhoanThuDotThu = db.Column(db.Integer, db.ForeignKey('khoanthu_has_dotthu.idKhoanThuDotThu'), nullable=False)
    
    # Relationships (tùy chọn, để dễ truy vấn)

    def __init__(self, soTienDaNop, soTienCanNop, nguoiNop, idKhoanThuDotThu, maHoKhau, idNguoiThu, ngayThu=None):
        self.soTienDaNop = soTienDaNop
        self.soTienCanNop = soTienCanNop
        self.nguoiNop = nguoiNop
        self.idKhoanThuDotThu = idKhoanThuDotThu
        self.maHoKhau = maHoKhau
        self.idNguoiThu = idNguoiThu
        self.ngayThu = ngayThu if ngayThu else datetime.now().date()
    
    def __repr__(self):
        return f'<NopPhi {self.IDNopTien}>'
    

class HoKhau(db.Model):
    __tablename__ = 'hokhau'
    
    maHoKhau = db.Column(db.Integer, primary_key=True)
    chuHo = db.Column(db.Integer, nullable=False)
    soNha = db.Column(db.String(25), nullable=False)
    ngayLap = db.Column(db.Date)
    ngayCapNhat = db.Column(db.Date)
    dienTich = db.Column(db.Float, nullable=False)
    xeMay = db.Column(db.Integer, default=0)
    oTo = db.Column(db.Integer, default=0)

    # Relationships
    lichsuhokhau = db.relationship('LichSuHoKhau', backref='hokhau', lazy=True)
    nhankhau = db.relationship('NhanKhau', backref='hokhau', lazy=True)
    
    def __init__(self, chuHo, soNha, ngayLap, ngayCapNhat, dienTich, xeMay=0, oTo=0):
        self.chuHo = chuHo
        self.soNha = soNha
        self.ngayLap = ngayLap
        self.ngayCapNhat = ngayCapNhat
        self.dienTich = dienTich
        self.xeMay = xeMay
        self.oTo = oTo

    def __repr__(self):
        return f'<HoKhau {self.maHoKhau}>'


class NhanKhau(db.Model):
    __tablename__ = 'nhankhau'
    
    maNhanKhau = db.Column(db.Integer, primary_key=True)
    hoTen = db.Column(db.String(100), nullable=False)
    ngaySinh = db.Column(db.Date)
    gioiTinh = db.Column(db.String(10))
    quocTich = db.Column(db.String(100))
    noiSinh = db.Column(db.String(100))
    cmnd = db.Column(db.String(25))
    qhVoiChuHo = db.Column(db.String(50))
    trangThai = db.Column(db.String(50))        # 'Thường trú', 'Tạm trú', 'Tạm vắng'
    maHoKhau = db.Column(db.Integer, db.ForeignKey('hokhau.maHoKhau'))
    
    # Relationships
    lichsuhokhau = db.relationship('LichSuHoKhau', backref='nhankhau', lazy=True)
    tamtrutamvang = db.relationship('TamTruTamVang', backref='nhankhau', lazy=True)
    
    def __init__(self, hoTen, ngaySinh, gioiTinh, maHoKhau):
        self.hoTen = hoTen
        self.ngaySinh = ngaySinh
        self.gioiTinh = gioiTinh
        self.maHoKhau = maHoKhau
    
    def __repr__(self):
        return f'<NhanKhau {self.hoTen}>'


class LichSuHoKhau(db.Model):
    __tablename__ = 'lichsuhokhau'
    
    id = db.Column(db.Integer, primary_key=True)
    loaiThayDoi = db.Column(db.String(45))          # Thêm, sửa, xóa
    thoiGian = db.Column(db.DateTime)
    noiDung = db.Column(db.String(1000))         
    maHoKhau = db.Column(db.Integer, db.ForeignKey('hokhau.maHoKhau'))
    maNhanKhau = db.Column(db.Integer, db.ForeignKey('nhankhau.maNhanKhau'))
    
    def __init__(self, loaiThayDoi, maHoKhau, maNhanKhau, thoiGian, noiDung):
        self.loaiThayDoi = loaiThayDoi
        self.maHoKhau = maHoKhau
        self.maNhanKhau = maNhanKhau
        self.noiDung = noiDung
        self.thoiGian = thoiGian if thoiGian else datetime.now()
    
    def __repr__(self):
        return f'<LichSuHoKhau {self.id}>'


class TamTruTamVang(db.Model):
    __tablename__ = 'tamtrutamvang'
    
    id = db.Column(db.Integer, primary_key=True)
    loai = db.Column(db.String(50))  # "Tạm trú" or "Tạm vắng"
    ngayBatDau = db.Column(db.Date)
    ngayKetThuc = db.Column(db.Date)
    lyDo = db.Column(db.String(1000))
    maNhanKhau = db.Column(db.Integer, db.ForeignKey('nhankhau.maNhanKhau'))
    
    def __init__(self, loai, maNhanKhau, ngayBatDau, ngayKetThuc, lyDo):
        self.loai = loai
        self.maNhanKhau = maNhanKhau
        self.ngayBatDau = ngayBatDau if ngayBatDau else datetime.now().date()
        self.ngayKetThuc = ngayKetThuc
        self.lyDo = lyDo
    
    def __repr__(self):
        return f'<TamTruTamVang {self.id}>'