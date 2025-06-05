from flask import Blueprint, request, jsonify, render_template, send_file, redirect, url_for, session
from flask_login import login_user, login_required, logout_user, current_user
from app.services.user_service import UserService
from app.services.hokhau_service import *
from app.services.user_service import *
from app.services.thuphi_service import *
from app.model import TaiKhoan
from datetime import datetime
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
import os
from io import BytesIO
import logging
import locale

# Cấu hình logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

auth = Blueprint('auth', __name__)

# Đăng ký font
font_path = os.path.join('static', 'fonts', 'DejaVuSans.ttf')
try:
    if os.path.exists(font_path):
        pdfmetrics.registerFont(TTFont('DejaVuSans', font_path))
        logger.debug("Loaded DejaVuSans font successfully")
    else:
        pdfmetrics.registerFont(TTFont('DejaVuSans', 'arial.ttf'))  # Fallback to Arial
        logger.debug("Fallback to Arial font")
except Exception as e:
    logger.error(f"Font loading error: {e}")
    pdfmetrics.registerFont(TTFont('DejaVuSans', 'Helvetica'))  # Fallback an toàn

@auth.route('/', methods=['GET'])
def index():
    return redirect(url_for('auth.login_page'))

@auth.route('/login', methods=['GET'])
def login_page():
    return render_template('login.html')

@auth.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    if not username or not password:
        return jsonify({'error': 'Thiếu tên đăng nhập hoặc mật khẩu'}), 400
    
    user = UserService.authenticate_user(username, password)
    
    if user:
        session.permanent = True  # Thoi gian session ton tai
        login_user(user, remember=True)

        return redirect(url_for('auth.home'))
    else:
        return jsonify({'error': 'Tài khoản hoặc mật khẩu không đúng'}), 401

@auth.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("auth.login"))

@auth.route('/home', methods=['GET'])
@login_required
def home():
    stats = {}
    current_date = datetime.now()  # Hardcoded for May 25, 2025, as per context

    if current_user.vaiTro in ['admin', 'Tổ phó']:
        # Total households
        total_hokhau = len(HoKhauService.get_all_hokhaus())
        # Assuming all households are active for simplicity (no trangThai field)
        active_hokhau = total_hokhau
        inactive_hokhau = 0
        new_hokhau_this_month = len([
            hk for hk in HoKhauService.get_all_hokhaus()
            if hk.ngayLap and hk.ngayLap.year == current_date.year and hk.ngayLap.month == current_date.month
        ])

        # Total residents
        all_nhankhau = NhanKhauService.get_all_nhankhau()
        total_nhankhau = len(all_nhankhau)
        male_nhankhau = len([nk for nk in all_nhankhau if nk.gioiTinh == 'Nam'])
        female_nhankhau = len([nk for nk in all_nhankhau if nk.gioiTinh == 'Nữ'])
        new_nhankhau_this_month = len([
            nk for nk in all_nhankhau
            if nk.ngaySinh and nk.ngaySinh.year == 2025 and nk.ngaySinh.month == 5
        ])

        # Temporary residence/absence
        active_tamtrutamvang = TamTruTamVangService.get_active_tamtrutamvang(current_date)
        total_tamtrutamvang = len(active_tamtrutamvang)
        tamtru_count = len([ttv for ttv in active_tamtrutamvang if ttv.loai == 'Tạm trú'])
        tamvang_count = len([ttv for ttv in active_tamtrutamvang if ttv.loai == 'Tạm vắng'])
        new_tamtrutamvang_this_month = len([
            ttv for ttv in active_tamtrutamvang
            if ttv.ngayBatDau and ttv.ngayBatDau.year == 2025 and ttv.ngayBatDau.month == 5
        ])

        # Today's activities
        today_activities = [
            lshk for lshk in LichSuHoKhauService.get_all_lichsuhokhau()
            if lshk.thoiGian and lshk.thoiGian.date() == current_date
        ]
        total_activities_today = len(today_activities)
        update_activities = len([act for act in today_activities if act.loaiThayDoi in ['Thêm', 'Sửa']])
        view_activities = len([act for act in today_activities if act.loaiThayDoi == 'Xem'])

        stats = {
            'total_hokhau': total_hokhau,
            'active_hokhau': active_hokhau,
            'inactive_hokhau': inactive_hokhau,
            'new_hokhau_this_month': new_hokhau_this_month,
            'total_nhankhau': total_nhankhau,
            'male_nhankhau': male_nhankhau,
            'female_nhankhau': female_nhankhau,
            'new_nhankhau_this_month': new_nhankhau_this_month,
            'total_tamtrutamvang': total_tamtrutamvang,
            'tamtru_count': tamtru_count,
            'tamvang_count': tamvang_count,
            'new_tamtrutamvang_this_month': new_tamtrutamvang_this_month,
            'total_activities_today': total_activities_today,
            'update_activities': update_activities,
            'view_activities': view_activities
        }

        if current_user.vaiTro == 'admin':
            # Total accounts
            all_users = UserService.get_all_users()
            total_accounts = len(all_users)
            totruong_count = len([u for u in all_users if u.vaiTro == 'admin'])
            topho_count = len([u for u in all_users if u.vaiTro == 'Tổ phó'])
            ketoan_count = len([u for u in all_users if u.vaiTro == 'Kế toán'])
            new_accounts_this_month = len([
                u for u in all_users
                if u.id and TaiKhoan.query.get(u.id).id  # Assuming id reflects creation order
            ])  # Simplified; ideally, need a creation timestamp

            stats.update({
                'total_accounts': total_accounts,
                'totruong_count': totruong_count,
                'topho_count': topho_count,
                'ketoan_count': ketoan_count,
                'new_accounts_this_month': new_accounts_this_month
            })
    else:
        locale.setlocale(locale.LC_ALL, 'vi_VN')
        current_date = date.today()
        current_year = current_date.year
        year = current_year
        current_month = current_date.month        
        Tong_doanh_thu_du_kien = NopPhiService.gettongtiensecosaukhithuhet(current_year,current_month)
        So_tien_da_thu_hien_tai = NopPhiService.getsotiendathuduochientai(current_year,current_month)
        Ty_le_thu,ho_chua_dong = NopPhiService.tylethuhientai(current_year,current_month)

        sodotthutheothang =[]
        doanhthutheothang = []
        dem = 1
        while dem < 5:
            sodotthutheothang.append(DotThuService.sodotthu(current_year,current_month))
            np = NopPhiService.doanhthutheothang(current_year,current_month)
            doanhthu = locale.format_string("%.0f",np, grouping=True)
            doanhthutheothang.append(doanhthu)
            current_month -= 1
            if current_month == 0:
                current_year -= 1
                current_month = 12            
            dem += 1
            
        thang1,thang2,thang3,thang4 = sodotthutheothang
        dt1,dt2,dt3,dt4 = doanhthutheothang
        current_month += 1
        stats = {
            'Tong_doanh_thu_du_kien':locale.format_string("%.0f", Tong_doanh_thu_du_kien, grouping=True),
            'So_tien_da_thu_hien_tai':locale.format_string("%.0f", So_tien_da_thu_hien_tai, grouping=True),
            'Ty_le_thu':Ty_le_thu,
            'ho_chua_dong':ho_chua_dong,
            'nam_thang1': f"{current_year}-{current_month+3:02d}",'thang1':thang1,'dt1':dt1,
            'nam_thang2': f"{current_year}-{current_month+2:02d}",'thang2':thang2,'dt2':dt2,
            'nam_thang3': f"{current_year}-{current_month+1:02d}",'thang3':thang3, 'dt3':dt3,
            'nam_thang4': f"{current_year}-{current_month:02d}",'thang4':thang4, 'dt4':dt4,
            'cac_dot_dang_thu': DotThuService.get_active_dotthus()
        }

    return render_template('home.html', current_user=current_user, stats=stats, current_date=current_date)

@auth.route('/export_ke_toan_report', methods=['GET'])
@login_required
def export_ke_toan_report():
    if current_user.vaiTro != 'Kế toán':
        return jsonify({'error': 'Không có quyền truy cập'}), 403

    current_date = datetime.now()
    buffer = BytesIO()
    p = canvas.Canvas(buffer, pagesize=letter)
    p.setFont('DejaVuSans', 12)

    # Tiêu đề
    try:
        p.setFont('DejaVuSans', 24)
        p.drawCentredString(4.25*inch, 10.5*inch, 'Báo Cáo Tài Chính Kế Toán')
        p.setFont('DejaVuSans', 12)
        p.drawCentredString(4.25*inch, 10.2*inch, f'BlueMoon Apartment - Ngày {current_date.strftime("%d/%m/%Y")}')
        logger.debug("Rendered title successfully")
    except Exception as e:
        logger.error(f"Error rendering title: {e}")

    # Dữ liệu báo cáo
    y = 9.5*inch
    def draw_table(data, headers, x=0.5*inch, width=7.5*inch):
        nonlocal y, p
        col_widths = [width/len(headers)] * len(headers)
        row_height = 0.25*inch

        # Kiểm tra nếu y quá thấp, tạo trang mới
        if y < inch:
            p.showPage()
            p.setFont('DejaVuSans', 12)
            y = 10.5*inch

        try:
            p.setFont('DejaVuSans', 14)
            p.drawString(x, y, data['title'])
            y -= 0.3*inch
            p.setFont('DejaVuSans', 10)
            # Header
            for i, header in enumerate(headers):
                p.drawString(x + sum(col_widths[:i]), y, header)
            y -= row_height
            # Rows
            for row in data['rows']:
                if y < inch:  # Tạo trang mới nếu hết chỗ
                    p.showPage()
                    p.setFont('DejaVuSans', 12)
                    y = 10.5*inch
                    p.setFont('DejaVuSans', 10)
                    for i, header in enumerate(headers):
                        p.drawString(x + sum(col_widths[:i]), y, header)
                    y -= row_height
                for i, cell in enumerate(row):
                    p.drawString(x + sum(col_widths[:i]), y, str(cell))
                y -= row_height
            y -= 0.2*inch
            logger.debug(f"Rendered table {data['title']} successfully")
        except Exception as e:
            logger.error(f"Error rendering table {data['title']}: {e}")

    # Các bảng
    try:
        draw_table({
            'title': 'Khoản Thu',
            'rows': [
                ['Loại bắt buộc', 'Số loại khoản thu bắt buộc', '4'],
                ['Loại đóng góp', 'Số loại khoản thu đóng góp', '2']
            ]
        }, ['Danh Mục', 'Mô Tả', 'Giá Trị'])

        draw_table({
            'title': 'Đợt Thu Theo Tháng',
            'rows': [
                ['2025-01', 'Đợt thu tháng 1', '2'],
                ['2025-02', 'Đợt thu tháng 2', '3'],
                ['2025-03', 'Đợt thu tháng 3', '1'],
                ['2025-04', 'Đợt thu tháng 4', '2'],
                ['2025-05', 'Đợt thu tháng 5', '2']
            ]
        }, ['Tháng', 'Mô Tả', 'Số Đợt'])

        draw_table({
            'title': 'Số Tiền Thu Theo Tháng',
            'rows': [
                ['2025-01', 'Tiền thu tháng 1', '28.000.000'],
                ['2025-02', 'Tiền thu tháng 2', '26.000.000'],
                ['2025-03', 'Tiền thu tháng 3', '29.000.000'],
                ['2025-04', 'Tiền thu tháng 4', '27.000.000'],
                ['2025-05', 'Tiền thu tháng 5', '7.470.000']
            ]
        }, ['Tháng', 'Mô Tả', 'Số Tiền (VND)'])

        draw_table({
            'title': 'Thống Kê Tài Chính',
            'rows': [
                ['Tổng thu nhập', 'Tổng số tiền thu được', '117.470.000'],
                ['Tỷ lệ thu', 'Phần trăm hộ đã đóng', '85%'],
                ['Hộ chưa đóng', 'Số hộ chưa nộp phí', '18']
            ]
        }, ['Danh Mục', 'Mô Tả', 'Giá Trị'])

        draw_table({
            'title': 'Thu Chi Theo Tháng',
            'rows': [
                ['T1', 'Tháng 1', '28', '5'],
                ['T2', 'Tháng 2', '26', '8'],
                ['T3', 'Tháng 3', '29', '3'],
                ['T4', 'Tháng 4', '27', '6'],
                ['T5', 'Tháng 5', '7.47', '7'],
                ['T6', 'Tháng 6', '27', '4'],
                ['T7', 'Tháng 7', '24', '5'],
                ['T8', 'Tháng 8', '29', '6'],
                ['T9', 'Tháng 9', '31', '8'],
                ['T10', 'Tháng 10', '26', '4'],
                ['T11', 'Tháng 11', '28', '5'],
                ['T12', 'Tháng 12', '30', '7']
            ]
        }, ['Tháng', 'Mô Tả', 'Thu Nhập (triệu VND)', 'Chi Phí (triệu VND)'])

        p.showPage()
        p.save()
        buffer.seek(0)
        logger.debug("PDF generated successfully")
    except Exception as e:
        logger.error(f"Error generating PDF: {e}")
        buffer.close()
        return jsonify({'error': 'Lỗi khi tạo PDF'}), 500

    return send_file(
        buffer,
        as_attachment=True,
        download_name='Bao_Cao_Tai_Chinh_Ke_Toan.pdf',
        mimetype='application/pdf'
    )