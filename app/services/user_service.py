from app.model import TaiKhoan
from app import db
from sqlalchemy.exc import SQLAlchemyError

class UserService:
    @staticmethod
    def authenticate_user(username, password):
        """
        Xác thực người dùng bằng tên đăng nhập và mật khẩu.
        Trả về đối tượng người dùng nếu xác thực thành công, ngược lại trả về None.
        """
        user = TaiKhoan.query.filter_by(username=username).first()
        if user and user.check_password(password):
            return user
        return None

    @staticmethod
    def create_user(username, password, vaiTro, hoTen):
        """
        Tạo người dùng mới.
        Trả về đối tượng người dùng đã tạo hoặc None nếu người dùng đã tồn tại.
        """
        try:
            if TaiKhoan.query.filter_by(username=username).first():
                return None 
            
            new_user = TaiKhoan(
                username=username,
                password=password,
                vaiTro=vaiTro,
                hoTen=hoTen
            )
            new_user.set_password(password)
            db.session.add(new_user)
            db.session.commit()
            return new_user
        except SQLAlchemyError:
            db.session.rollback()
            return None

    @staticmethod
    def get_user_by_username(username):
        """
        Lấy thông tin người dùng bằng tên đăng nhập.
        """
        return TaiKhoan.query.filter_by(username=username).first()

    @staticmethod
    def get_user_by_id(user_id):
        """
        Lấy thông tin người dùng bằng ID.
        """
        return TaiKhoan.query.get(user_id)
    
    @staticmethod
    def get_all_users():
        """
        Lấy danh sách tất cả người dùng.
        """
        return TaiKhoan.query.all()
    
    @staticmethod
    def update_user(user_id, hoTen, vaiTro, password=None):
        """
        Cập nhật thông tin người dùng.
        Trả về True nếu cập nhật thành công, ngược lại trả về False.
        """
        try:
            user = TaiKhoan.query.get(user_id)
            if not user:
                return False
            
            user.hoTen = hoTen
            user.vaiTro = vaiTro
            
            if password:
                user.set_password(password)
            
            db.session.commit()
            return True
        except SQLAlchemyError:
            db.session.rollback()
            return False

    @staticmethod
    def delete_user(user_id):
        """
        Xóa người dùng.
        Trả về True nếu xóa thành công, ngược lại trả về False.
        """
        try:
            user = TaiKhoan.query.get(user_id)
            if not user:
                return False
            
            db.session.delete(user)
            db.session.commit()
            return True
        except SQLAlchemyError:
            db.session.rollback()
            return False