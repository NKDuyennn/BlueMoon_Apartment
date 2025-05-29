from flask import Blueprint, request, jsonify, render_template, session, redirect, url_for, flash
from flask_login import login_user, login_required, logout_user, current_user
from app.services.user_service import *
from app.model import TaiKhoan

user = Blueprint('user', __name__)

@user.route('/taikhoan', methods=['GET'])
@login_required
def taikhoan():
    if current_user.vaiTro != 'admin':
        flash('Không có quyền truy cập trang', 'danger')
        return redirect(url_for('auth.home'))
    
    accounts = UserService.get_all_users()
    return render_template('taikhoan.html', accounts=accounts)

@user.route('/taikhoan/add', methods=['POST'])
@login_required
def add_new_account():
    if current_user.vaiTro != 'admin':
        return jsonify({'success': False, 'message': 'Không có quyền thực hiện'}), 403
    
    data = request.form
    username = data.get('username')
    password = data.get('password')
    hoTen  = data.get('hoTen')
    vaiTro = data.get('vaiTro')

    if not all([username, password, hoTen, vaiTro]):
        return jsonify({'success': False, 'message': 'Vui lòng điền đầy đủ thông tin'}), 400
    
    # Tạo tài khoản mới
    new_user = UserService.create_user(username, password, vaiTro, hoTen)

    if new_user:
        return jsonify({'success': True, 'message': 'Tạo tài khoản thành công'}), 201
    else:
        return jsonify({'success': False, 'message': 'Tên người dùng đã tồn tại'}), 400
    
@user.route('/taikhoan/<int:id>', methods=['GET'])
@login_required
def get_account(id):
    if current_user.vaiTro != 'admin':
        return jsonify({'success': False, 'message': 'Không có quyền thực hiện'}), 403
    
    account = UserService.get_user_by_id(id)
    if not account:
        return jsonify({'success': False, 'message': 'Không tìm thấy tài khoản'}), 404
    
    return jsonify({
        'id': account.id,
        'username': account.username,
        'hoTen': account.hoTen,
        'vaiTro': account.vaiTro
    }), 200

@user.route('/taikhoan/<int:id>', methods=['PUT'])
@login_required
def update_account(id):
    if current_user.vaiTro != 'admin':
        return jsonify({'success': False, 'message': 'Không có quyền thực hiện'}), 403
    
    data = request.json
    hoTen = data.get('hoTen')
    vaiTro = data.get('vaiTro')
    password = data.get('password')  # Optional for update
    
    # Validate dữ liệu
    if not all([hoTen, vaiTro]):
        return jsonify({'success': False, 'message': 'Vui lòng điền đầy đủ thông tin'}), 400
    
    # Cập nhật tài khoản
    result = UserService.update_user(id, hoTen, vaiTro, password)
    if result:
        return jsonify({'success': True, 'message': 'Cập nhật tài khoản thành công'}), 200
    else:
        return jsonify({'success': False, 'message': 'Không tìm thấy tài khoản'}), 404
    
@user.route('/taikhoan/<int:id>', methods=['DELETE'])
@login_required
def delete_account(id):
    if current_user.vaiTro != 'admin':
        return jsonify({'success': False, 'message': 'Không có quyền thực hiện'}), 403
    
    # Ngăn chặn xóa tài khoản đang đăng nhập
    if id == current_user.id:
        return jsonify({'success': False, 'message': 'Không thể xóa tài khoản của chính mình'}), 400
    
    # Xóa tài khoản
    result = UserService.delete_user(id)
    if result:
        return jsonify({'success': True, 'message': 'Xóa tài khoản thành công'}), 200
    else:
        return jsonify({'success': False, 'message': 'Không tìm thấy tài khoản'}), 404