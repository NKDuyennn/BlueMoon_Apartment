-- Tạo database
CREATE DATABASE IF NOT EXISTS quan_ly_chung_cu;
USE quan_ly_chung_cu;

-- Tạo bảng taikhoan
CREATE TABLE taikhoan (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    password VARCHAR(100) NOT NULL,
    vaiTro VARCHAR(50),
    hoTen VARCHAR(100)
);

-- Tạo bảng hokhau
CREATE TABLE hokhau (
    maHoKhau INT AUTO_INCREMENT PRIMARY KEY,
    chuHo INT NOT NULL,
    soNha VARCHAR(25) NOT NULL,
    ngayLap DATE,
    ngayCapNhat DATE,
    dienTich FLOAT NOT NULL,
    xeMay INT DEFAULT 0,
    oTo INT DEFAULT 0
);

-- Tạo bảng nhankhau
CREATE TABLE nhankhau (
    maNhanKhau INT AUTO_INCREMENT PRIMARY KEY,
    hoTen VARCHAR(100) NOT NULL,
    ngaySinh DATE,
    gioiTinh VARCHAR(10),
    quocTich VARCHAR(100),
    noiSinh VARCHAR(100),
    cmnd VARCHAR(25),
    qhVoiChuHo VARCHAR(50),
    trangThai VARCHAR(50),
    maHoKhau INT,
    FOREIGN KEY (maHoKhau) REFERENCES hokhau(maHoKhau) ON DELETE CASCADE
);

-- Tạo bảng khoanthu
CREATE TABLE khoanthu (
    maKhoanThu INT AUTO_INCREMENT PRIMARY KEY,
    tenKhoanThu VARCHAR(100) NOT NULL,
    loaiKhoanThu VARCHAR(50),
    soTien FLOAT,
    loaiSoTien VARCHAR(50),
    ghiChu VARCHAR(1000),
    idNguoiTao INT,
    FOREIGN KEY (idNguoiTao) REFERENCES taikhoan(id) ON DELETE SET NULL
);

-- Tạo bảng dotthu
CREATE TABLE dotthu (
    maDotThu INT AUTO_INCREMENT PRIMARY KEY,
    tenDotThu VARCHAR(100) NOT NULL,
    ngayBatDau DATE,
    ngayKetThuc DATE,
    trangThai VARCHAR(50)
);

-- Tạo bảng khoanthu_has_dotthu (bảng liên kết)
CREATE TABLE khoanthu_has_dotthu (
    idKhoanThuDotThu INT AUTO_INCREMENT PRIMARY KEY,
    maKhoanThu INT,
    maDotThu INT,
    FOREIGN KEY (maKhoanThu) REFERENCES khoanthu(maKhoanThu) ON DELETE CASCADE,
    FOREIGN KEY (maDotThu) REFERENCES dotthu(maDotThu) ON DELETE CASCADE
);

-- Tạo bảng nopphi
CREATE TABLE nopphi (
    IDNopTien INT AUTO_INCREMENT PRIMARY KEY,
    ngayThu DATE,
    soTienDaNop FLOAT NOT NULL DEFAULT 0.0,
    soTienCanNop FLOAT NOT NULL DEFAULT 0.0,
    nguoiNop VARCHAR(100),
    idNguoiThu INT,
    maHoKhau INT NOT NULL,
    idKhoanThuDotThu INT NOT NULL,
    FOREIGN KEY (idNguoiThu) REFERENCES taikhoan(id) ON DELETE SET NULL,
    FOREIGN KEY (maHoKhau) REFERENCES hokhau(maHoKhau) ON DELETE CASCADE,
    FOREIGN KEY (idKhoanThuDotThu) REFERENCES khoanthu_has_dotthu(idKhoanThuDotThu) ON DELETE CASCADE
);

-- Tạo bảng lichsuhokhau
CREATE TABLE lichsuhokhau (
    id INT AUTO_INCREMENT PRIMARY KEY,
    loaiThayDoi VARCHAR(45),
    thoiGian DATETIME,
    noiDung VARCHAR(1000),
    maHoKhau INT,
    maNhanKhau INT,
    FOREIGN KEY (maHoKhau) REFERENCES hokhau(maHoKhau) ON DELETE CASCADE,
    FOREIGN KEY (maNhanKhau) REFERENCES nhankhau(maNhanKhau) ON DELETE CASCADE
);

-- Tạo bảng tamtrutamvang
CREATE TABLE tamtrutamvang (
    id INT AUTO_INCREMENT PRIMARY KEY,
    loai VARCHAR(50),
    ngayBatDau DATE,
    ngayKetThuc DATE,
    lyDo VARCHAR(1000),
    maNhanKhau INT,
    FOREIGN KEY (maNhanKhau) REFERENCES nhankhau(maNhanKhau) ON DELETE CASCADE
);

-- Tạo các index để tối ưu performance
CREATE INDEX idx_taikhoan_username ON taikhoan(username);
CREATE INDEX idx_hokhau_chuho ON hokhau(chuHo);
CREATE INDEX idx_nhankhau_hokhau ON nhankhau(maHoKhau);
CREATE INDEX idx_khoanthu_nguoitao ON khoanthu(idNguoiTao);
CREATE INDEX idx_nopphi_hokhau ON nopphi(maHoKhau);
CREATE INDEX idx_nopphi_khoanthu_dotthu ON nopphi(idKhoanThuDotThu);
CREATE INDEX idx_lichsu_hokhau ON lichsuhokhau(maHoKhau);
CREATE INDEX idx_lichsu_nhankhau ON lichsuhokhau(maNhanKhau);
CREATE INDEX idx_tamtru_nhankhau ON tamtrutamvang(maNhanKhau);

-- Thêm dữ liệu mẫu cho bảng taikhoan (tùy chọn)
INSERT INTO taikhoan (username, password, vaiTro, hoTen) VALUES
('admin', 'pbkdf2:sha256:260000$salt$hash', 'Admin', 'Quản trị viên'),
('thu_phi', 'pbkdf2:sha256:260000$salt$hash', 'Thu phí', 'Nhân viên thu phí');

-- Thêm comment cho các bảng
ALTER TABLE taikhoan COMMENT = 'Bảng quản lý tài khoản người dùng';
ALTER TABLE hokhau COMMENT = 'Bảng quản lý thông tin hộ khẩu';
ALTER TABLE nhankhau COMMENT = 'Bảng quản lý thông tin nhân khẩu';
ALTER TABLE khoanthu COMMENT = 'Bảng quản lý các khoản thu';
ALTER TABLE dotthu COMMENT = 'Bảng quản lý các đợt thu';
ALTER TABLE khoanthu_has_dotthu COMMENT = 'Bảng liên kết giữa khoản thu và đợt thu';
ALTER TABLE nopphi COMMENT = 'Bảng quản lý việc nộp phí của các hộ khẩu';
ALTER TABLE lichsuhokhau COMMENT = 'Bảng lưu lịch sử thay đổi hộ khẩu';
ALTER TABLE tamtrutamvang COMMENT = 'Bảng quản lý tạm trú tạm vắng';