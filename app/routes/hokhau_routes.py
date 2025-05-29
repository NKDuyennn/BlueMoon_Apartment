from flask import Blueprint, request, jsonify, render_template, session, redirect, url_for, flash
from flask_login import login_user, login_required, logout_user, current_user
from app.services.hokhau_service import *
from datetime import datetime

hk = Blueprint('hk', __name__)

@hk.route('/hokhau', methods=['GET'])
@login_required
def hokhau():
    hokhaus = HoKhauService.get_all_hokhaus()
    nhankhaus = NhanKhauService.get_all_nhankhau()
    return render_template('hokhau.html', hokhaus=hokhaus, nhankhaus=nhankhaus)
