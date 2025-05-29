from flask import Blueprint, request, jsonify, render_template, session, redirect, url_for, flash
from flask_login import login_required, current_user
from app.services.thuphi_service import *
from app.services.hokhau_service import *
from datetime import datetime

tp = Blueprint('tp', __name__)

@tp.route('/khoanthu', methods=['GET'])
@login_required
def khoanthu():
    if current_user.vaiTro not in ['Kế toán']:
        flash('Không có quyền truy cập trang', 'danger')
        return redirect(url_for('auth.home'))
    
    khoanthus = KhoanThuService.get_all_khoanthus()
    return render_template('khoanthu.html', khoanthus=khoanthus)

