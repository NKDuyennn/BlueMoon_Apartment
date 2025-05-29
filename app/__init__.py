from flask import Flask, session
from flask_sqlalchemy import SQLAlchemy
import os
from datetime import date, timedelta
from flask_login import LoginManager
from .model import TaiKhoan, KhoanThu, DotThu, KhoanThu_Has_DotThu, NopPhi
from .extension import db
from .services.hokhau_service import HoKhauService


def create_db(app):
    db_path = "instance/apartment.db"
    if not os.path.exists(db_path):
        with app.app_context():
            db.create_all()
            print("Database created successfully")

            admin_exists = db.session.query(TaiKhoan).filter_by(vaiTro='admin').first()
            if not admin_exists:
                # Danh sách tài khoản mặc định cần tạo
                default_users = [
                    {
                        'username': 'admin',
                        'password': 'admin123',
                        'vaiTro': 'admin',
                        'hoTen': 'Quản trị viên'
                    },
                    {
                        'username': 'topho',
                        'password': 'topho123',
                        'vaiTro': 'Tổ phó',
                        'hoTen': 'Tổ phó mặc định'
                    },
                    {
                        'username': 'ketoan',
                        'password': 'ketoan123',
                        'vaiTro': 'Kế toán',
                        'hoTen': 'Kế toán mặc định'
                    }
                ]

                for user in default_users:
                    tai_khoan = TaiKhoan(
                        username=user['username'],
                        password=user['password'],
                        vaiTro=user['vaiTro'],
                        hoTen=user['hoTen']
                    )
                    tai_khoan.set_password(user['password'])
                    db.session.add(tai_khoan)
                    print(f"Default {user['vaiTro']} account created")
                
                db.session.commit()
                print("Tạo tài khoản thành công")
    else:
        print("Database already exists")


def init_jinja_filters(app):
    """Đăng ký các filter Jinja2 tùy chỉnh."""
    # Filter lấy thông tin hộ khẩu
    def get_hokhau_so_nha(maHoKhau):
        hokhau = HoKhauService.get_hokhau_by_id(maHoKhau)
        return hokhau.soNha if hokhau else '-'

    def get_chu_ho(maHoKhau):
        hokhau = HoKhauService.get_hokhau_by_id(maHoKhau)
        return hokhau.chuHo if hokhau else '-'

    def get_hokhau_dien_tich(maHoKhau):
        hokhau = HoKhauService.get_hokhau_by_id(maHoKhau)
        return hokhau.dienTich if hokhau else 0

    def get_hokhau_xe_may(maHoKhau):
        hokhau = HoKhauService.get_hokhau_by_id(maHoKhau)
        return hokhau.xeMay if hokhau else 0

    def get_hokhau_o_to(maHoKhau):
        hokhau = HoKhauService.get_hokhau_by_id(maHoKhau)
        return hokhau.oTo if hokhau else 0

    # Filter định dạng ngày tháng
    def format_date_input(value):
        if isinstance(value, date):
            return value.strftime('%Y-%m-%d')
        return value

    def format_date(value):
        if value is None:
            return '-'
        if isinstance(value, date):
            return value.strftime('%d/%m/%Y')
        return value

    # Đăng ký các filter với Jinja2
    app.jinja_env.filters['get_hokhau_so_nha'] = get_hokhau_so_nha
    app.jinja_env.filters['get_chu_ho'] = get_chu_ho
    app.jinja_env.filters['get_hokhau_dien_tich'] = get_hokhau_dien_tich
    app.jinja_env.filters['get_hokhau_xe_may'] = get_hokhau_xe_may
    app.jinja_env.filters['get_hokhau_o_to'] = get_hokhau_o_to
    app.jinja_env.filters['format_date_input'] = format_date_input
    app.jinja_env.filters['format_date'] = format_date


def create_app(config_file="config.py"):
    app = Flask(__name__)
    app.config.from_pyfile(config_file)
    db.init_app(app)

    create_db(app)

    # Đăng ký các filter Jinja2
    init_jinja_filters(app)

    # Thêm current_user vào tất cả template
    @app.context_processor
    def inject_current_user():
        current_user = {
            'id': session.get('user_id'),
            'username': session.get('username'),
            'role': session.get('vaiTro'),
            'name': session.get('hoTen')
        }
        return dict(current_user=current_user)
    
    # Import và đăng ký Blueprint
    from app.routes import auth_routes, user_routes, hokhau_routes, thuphi_routes
    app.register_blueprint(auth_routes.auth)
    app.register_blueprint(user_routes.user)
    app.register_blueprint(hokhau_routes.hk)
    app.register_blueprint(thuphi_routes.tp)

    # Khởi tạo login manager
    login_manager = LoginManager()
    login_manager.login_view = "auth.login"  # Chuyển đến trang login nếu chưa đăng nhập
    login_manager.init_app(app)  # Khởi tạo login manager với app
    app.permanent_session_lifetime = timedelta(hours=1)  # Thời gian session tồn tại
    
    @login_manager.user_loader
    def load_user(id):
        return TaiKhoan.query.get(int(id))  # Lấy user từ db theo id

    return app