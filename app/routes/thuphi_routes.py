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

@tp.route('/khoanthu/add', methods=['POST'])
@login_required
def add_khoanthu():
    if current_user.vaiTro not in ['Kế toán']:
        return jsonify({'success': False, 'message': 'Không có quyền thực hiện'}), 403
    
    data = request.form
    ten_khoanthu = data.get('tenKhoanThu')
    loai_khoanthu = data.get('loaiKhoanThu')
    so_tien = data.get('soTien')
    loai_sotien = data.get('loaiSoTien')
    ghi_chu = data.get('ghiChu', '')
    
    if not all([ten_khoanthu, loai_khoanthu, so_tien, loai_sotien]):
        return jsonify({'success': False, 'message': 'Vui lòng điền đầy đủ thông tin'}), 400
    
    try:
        so_tien = float(so_tien)
    except ValueError:
        return jsonify({'success': False, 'message': 'Số tiền không hợp lệ'}), 400
    
    new_khoanthu = KhoanThuService.create_khoanthu(
        tenKhoanThu=ten_khoanthu,
        loaiKhoanThu=loai_khoanthu,
        soTien=so_tien,
        loaiSoTien=loai_sotien,
        ghiChu=ghi_chu,
        idNguoiTao=current_user.id
    )
    
    if new_khoanthu:
        return jsonify({'success': True, 'message': 'Tạo khoản thu thành công'}), 201
    else:
        return jsonify({'success': False, 'message': 'Có lỗi xảy ra khi tạo khoản thu'}), 500

@tp.route('/khoanthu/<int:ma_khoanthu>', methods=['GET'])
@login_required
def get_khoanthu(ma_khoanthu):
    if current_user.vaiTro not in ['Kế toán']:
        return jsonify({'success': False, 'message': 'Không có quyền thực hiện'}), 403
    
    khoanthu = KhoanThuService.get_khoanthu_by_id(ma_khoanthu)
    if not khoanthu:
        return jsonify({'success': False, 'message': 'Không tìm thấy khoản thu'}), 404
    
    return jsonify({
        'maKhoanThu': khoanthu.maKhoanThu,
        'tenKhoanThu': khoanthu.tenKhoanThu,
        'loaiKhoanThu': khoanthu.loaiKhoanThu,
        'soTien': khoanthu.soTien,
        'loaiSoTien': khoanthu.loaiSoTien,
        'ghiChu': khoanthu.ghiChu,
        'idNguoiTao': khoanthu.idNguoiTao
    }), 200

@tp.route('/khoanthu/<int:ma_khoanthu>', methods=['PUT'])
@login_required
def update_khoanthu(ma_khoanthu):
    if current_user.vaiTro not in ['Kế toán']:
        return jsonify({'success': False, 'message': 'Không có quyền thực hiện'}), 403
    
    data = request.json
    ten_khoanthu = data.get('tenKhoanThu')
    loai_khoanthu = data.get('loaiKhoanThu')
    so_tien = data.get('soTien')
    loai_sotien = data.get('loaiSoTien')
    ghi_chu = data.get('ghiChu', '')
    
    if not all([ten_khoanthu, loai_khoanthu, so_tien, loai_sotien]):
        return jsonify({'success': False, 'message': 'Vui lòng điền đầy đủ thông tin'}), 400
    
    try:
        so_tien = float(so_tien)
    except ValueError:
        return jsonify({'success': False, 'message': 'Số tiền không hợp lệ'}), 400
    
    result = KhoanThuService.update_khoanthu(
        maKhoanThu=ma_khoanthu,
        tenKhoanThu=ten_khoanthu,
        loaiKhoanThu=loai_khoanthu,
        soTien=so_tien,
        loaiSoTien=loai_sotien,
        ghiChu=ghi_chu,
    )
    
    if result:
        return jsonify({'success': True, 'message': 'Cập nhật khoản thu thành công'}), 200
    else:
        return jsonify({'success': False, 'message': 'Không tìm thấy khoản thu hoặc có lỗi xảy ra'}), 404

@tp.route('/khoanthu/<int:ma_khoanthu>', methods=['DELETE'])
@login_required
def delete_khoanthu(ma_khoanthu):
    if current_user.vaiTro not in ['Kế toán']:
        return jsonify({'success': False, 'message': 'Không có quyền thực hiện'}), 403
    
    result = KhoanThuService.delete_khoanthu(ma_khoanthu)
    if result:
        return jsonify({'success': True, 'message': 'Xóa khoản thu thành công'}), 200
    else:
        return jsonify({'success': False, 'message': 'Không tìm thấy khoản thu hoặc có lỗi xảy ra'}), 404

@tp.route('/dotthu', methods=['GET'])
@login_required
def dotthu():
    dotthus = DotThuService.get_all_dotthus()
    return render_template('dotthu.html', dotthus=dotthus)

@tp.route('/dotthu/add', methods=['POST'])
@login_required
def add_dotthu():
    if current_user.vaiTro not in ['Kế toán']:
        return jsonify({'success': False, 'message': 'Không có quyền thực hiện'}), 403
    
    data = request.form
    ten_dotthu = data.get('tenDotThu')
    ngay_bat_dau = data.get('ngayBatDau')
    ngay_ket_thuc = data.get('ngayKetThuc')
    trang_thai = data.get('trangThai', 'Đang thực hiện')
    
    try:
        ngay_bat_dau = datetime.strptime(ngay_bat_dau, '%Y-%m-%d').date()
        ngay_ket_thuc = datetime.strptime(ngay_ket_thuc, '%Y-%m-%d').date()
    except ValueError:
        return jsonify({'success': False, 'message': 'Định dạng ngày không hợp lệ'}), 400
    
    if ngay_bat_dau > ngay_ket_thuc:
        return jsonify({'success': False, 'message': 'Ngày bắt đầu phải sớm hơn ngày kết thúc'}), 400
    
    if DotThuService.get_dotthu_by_name(ten_dotthu):
        return jsonify({'success': False, 'message': 'Tên đợt thu đã tồn tại'}), 400
    
    result = DotThuService.create_dotthu(
        tenDotThu=ten_dotthu,
        ngayBatDau=ngay_bat_dau,
        ngayKetThuc=ngay_ket_thuc,
        trangThai=trang_thai
    )
    
    if result:
        return jsonify({'success': True, 'message': 'Thêm đợt thu thành công'}), 201
    else:
        return jsonify({'success': False, 'message': 'Thêm đợt thu thất bại'}), 500

@tp.route('/dotthu/<int:maDotThu>', methods=['GET'])
@login_required
def dotthu_chitiet(maDotThu):
    if current_user.vaiTro not in ['Kế toán']:
        flash('Không có quyền truy cập trang', 'danger')
        return redirect(url_for('auth.home'))
    
    dotthu = DotThuService.get_dotthu_by_id(maDotThu)
    if not dotthu:
        flash('Không tìm thấy đợt thu', 'danger')
        return redirect(url_for('tp.dotthu'))
    
    khoanthus = KhoanThuHasDotThuService.get_by_dotthu(maDotThu)
    all_khoanthus = KhoanThuService.get_all_khoanthus()
    hokhaus = HoKhauService.get_all_hokhaus()
    nopphi_details = NopPhiService.get_nopphis_with_details(maDotThu)
    
    return render_template('dotthu_chitiet.html', 
                         dotthu=dotthu, 
                         khoanthus=khoanthus, 
                         all_khoanthus=all_khoanthus, 
                         hokhaus=hokhaus, 
                         nopphi_details=nopphi_details)

@tp.route('/dotthu/<int:maDotThu>', methods=['PUT'])
@login_required
def update_dotthu(maDotThu):
    if current_user.vaiTro not in ['Kế toán']:
        return jsonify({'success': False, 'message': 'Không có quyền thực hiện'}), 403
    
    data = request.json
    ten_dotthu = data.get('tenDotThu')
    ngay_bat_dau = data.get('ngayBatDau')
    ngay_ket_thuc = data.get('ngayKetThuc')
    trang_thai = data.get('trangThai')
    
    if not all([ten_dotthu, ngay_bat_dau, ngay_ket_thuc, trang_thai]):
        return jsonify({'success': False, 'message': 'Vui lòng điền đầy đủ thông tin'}), 400
    
    try:
        ngay_bat_dau = datetime.strptime(ngay_bat_dau, '%Y-%m-%d').date()
        ngay_ket_thuc = datetime.strptime(ngay_ket_thuc, '%Y-%m-%d').date()
    except ValueError:
        return jsonify({'success': False, 'message': 'Định dạng ngày không hợp lệ'}), 400
    
    if ngay_bat_dau > ngay_ket_thuc:
        return jsonify({'success': False, 'message': 'Ngày bắt đầu phải sớm hơn ngày kết thúc'}), 400
    
    existing_dotthu = DotThuService.get_dotthu_by_name(ten_dotthu)
    if existing_dotthu and existing_dotthu.maDotThu != maDotThu:
        return jsonify({'success': False, 'message': 'Tên đợt thu đã tồn tại'}), 400
    
    result = DotThuService.update_dotthu(
        maDotThu=maDotThu,
        tenDotThu=ten_dotthu,
        ngayBatDau=ngay_bat_dau,
        ngayKetThuc=ngay_ket_thuc,
        trangThai=trang_thai
    )
    
    if result:
        return jsonify({'success': True, 'message': 'Cập nhật đợt thu thành công'}), 200
    else:
        return jsonify({'success': False, 'message': 'Không tìm thấy đợt thu hoặc có lỗi xảy ra'}), 404

@tp.route('/dotthu/<int:maDotThu>/update_khoanthus', methods=['POST'])
@login_required
def update_khoanthus_in_dotthu(maDotThu):
    if current_user.vaiTro not in ['Kế toán']:
        return jsonify({'success': False, 'message': 'Không có quyền thực hiện'}), 403
    
    data = request.json
    selected_khoanthus = data.get('selectedKhoanThu', [])
    
    current_khoanthus = KhoanThuHasDotThuService.get_by_dotthu(maDotThu)
    current_khoanthu_ids = [str(kt.maKhoanThu) for kt in current_khoanthus]
    
    khoanthus_to_add = [kt_id for kt_id in selected_khoanthus if kt_id not in current_khoanthu_ids]
    khoanthus_to_remove = [kt for kt in current_khoanthus if str(kt.maKhoanThu) not in selected_khoanthus]
    
    success = True
    messages = []
    
    # Lấy danh sách hộ khẩu hiện tại trong đợt thu
    current_nopphis = NopPhiService.get_nopphis_with_details(maDotThu)
    current_hokhau_ids = [int(hk['maHoKhau']) for hk in current_nopphis]
    
    for kt_id in khoanthus_to_add:
        result = KhoanThuHasDotThuService.create_khoanthu_has_dotthu(int(kt_id), maDotThu)
        if not result:
            success = False
            messages.append(f'Thêm khoản thu {kt_id} thất bại')
        else:
            # Tạo bản ghi nộp phí cho tất cả hộ khẩu hiện tại
            for hk_id in current_hokhau_ids:
                nopphi = NopPhiService.create_nopphi_for_hokhau(
                    maHoKhau=hk_id,
                    idKhoanThuDotThu=result.idKhoanThuDotThu,
                    nguoiNop='',
                    idNguoiThu=current_user.id
                )
                if not nopphi:
                    success = False
                    messages.append(f'Tạo bản ghi nộp phí cho hộ khẩu {hk_id} và khoản thu {kt_id} thất bại')
    
    for kt in khoanthus_to_remove:
        # Xóa các bản ghi NopPhi liên quan trước
        nopphis = NopPhiService.get_nopphis_by_khoanthu_dotthu(kt.idKhoanThuDotThu)
        for nopphi in nopphis:
            if not NopPhiService.delete_nopphi(nopphi.IDNopTien):
                success = False
                messages.append(f'Xóa bản ghi nộp phí cho khoản thu {kt.maKhoanThu} thất bại')
        
        if not KhoanThuHasDotThuService.delete(kt.idKhoanThuDotThu):
            success = False
            messages.append(f'Xóa khoản thu {kt.maKhoanThu} thất bại')
    
    if success:
        return jsonify({'success': True, 'message': 'Cập nhật danh sách khoản thu thành công'}), 200
    else:
        return jsonify({'success': False, 'message': '\n'.join(messages)}), 500

@tp.route('/dotthu/<int:maDotThu>/update_hokhaus', methods=['POST'])
@login_required
def update_hokhaus_in_dotthu(maDotThu):
    if current_user.vaiTro not in ['Kế toán']:
        return jsonify({'success': False, 'message': 'Không có quyền thực hiện'}), 403
    
    data = request.json
    selected_hokhaus = data.get('selectedHoKhau', [])
    nguoi_nop_mac_dinh = data.get('nguoiNopMacDinh', '')
    
    current_nopphis = NopPhiService.get_nopphis_with_details(maDotThu)
    current_hokhau_ids = [str(hk['maHoKhau']) for hk in current_nopphis]
    
    hokhaus_to_add = [hk_id for hk_id in selected_hokhaus if hk_id not in current_hokhau_ids]
    hokhaus_to_remove = [hk_id for hk_id in current_hokhau_ids if hk_id not in selected_hokhaus]
    
    success = True
    messages = []
    
    for hk_id in hokhaus_to_add:
        nopphis = NopPhiService.create_multiple_nopphi_for_hokhau(
            maHoKhau=int(hk_id),
            maDotThu=maDotThu,
            nguoiNop=nguoi_nop_mac_dinh,
            idNguoiThu=current_user.id
        )
        if not nopphis:
            success = False
            messages.append(f'Thêm hộ khẩu {hk_id} thất bại')
    
    for hk_id in hokhaus_to_remove:
        nopphis = NopPhiService.get_nopphis_by_hokhau(int(hk_id))
        khoanthu_dotthus = KhoanThuHasDotThuService.get_by_dotthu(maDotThu)
        kt_dt_ids = [kt_dt.idKhoanThuDotThu for kt_dt in khoanthu_dotthus]
        
        for nopphi in nopphis:
            if nopphi.idKhoanThuDotThu in kt_dt_ids:
                if not NopPhiService.delete_nopphi(nopphi.IDNopTien):
                    success = False
                    messages.append(f'Xóa bản ghi nộp phí cho hộ khẩu {hk_id} thất bại')
    
    # Cập nhật nguoiNop cho các hộ khẩu hiện tại
    if nguoi_nop_mac_dinh:
        for hk_id in selected_hokhaus:
            nopphis = NopPhiService.get_nopphis_by_hokhau(int(hk_id))
            khoanthu_dotthus = KhoanThuHasDotThuService.get_by_dotthu(maDotThu)
            kt_dt_ids = [kt_dt.idKhoanThuDotThu for kt_dt in khoanthu_dotthus]
            
            for nopphi in nopphis:
                if nopphi.idKhoanThuDotThu in kt_dt_ids:
                    if not NopPhiService.update_nopphi(
                        IDNopTien=nopphi.IDNopTien,
                        nguoiNop=nguoi_nop_mac_dinh
                    ):
                        success = False
                        messages.append(f'Cập nhật người nộp cho hộ khẩu {hk_id} thất bại')
    
    if success:
        return jsonify({'success': True, 'message': 'Cập nhật danh sách hộ khẩu thành công'}), 200
    else:
        return jsonify({'success': False, 'message': '\n'.join(messages)}), 500

@tp.route('/dotthu/<int:maDotThu>/update_nopphi/<int:IDNopTien>', methods=['PUT'])
@login_required
def update_nopphi(maDotThu, IDNopTien):
    if current_user.vaiTro not in ['Kế toán']:
        return jsonify({'success': False, 'message': 'Không có quyền thực hiện'}), 403
    
    data = request.json
    so_tien_da_nop = data.get('soTienDaNop')
    nguoi_nop = data.get('nguoiNop')
    
    if so_tien_da_nop is not None:
        try:
            so_tien_da_nop = float(so_tien_da_nop)
        except (ValueError, TypeError):
            return jsonify({'success': False, 'message': 'Số tiền không hợp lệ'}), 400
    
    result = NopPhiService.update_nopphi(
        IDNopTien=IDNopTien,
        soTienDaNop=so_tien_da_nop,
        nguoiNop=nguoi_nop
    )
    
    if result:
        return jsonify({'success': True, 'message': 'Cập nhật nộp phí thành công'}), 200
    else:
        return jsonify({'success': False, 'message': 'Cập nhật nộp phí thất bại'}), 500

@tp.route('/dotthu/<int:maDotThu>', methods=['DELETE'])
@login_required
def delete_dotthu(maDotThu):
    if current_user.vaiTro not in ['Kế toán']:
        return jsonify({'success': False, 'message': 'Không có quyền thực hiện'}), 403
    
    # Xóa tất cả bản ghi nộp phí liên quan
    khoanthu_dotthus = KhoanThuHasDotThuService.get_by_dotthu(maDotThu)
    for kt_dt in khoanthu_dotthus:
        nopphis = NopPhiService.get_nopphis_by_khoanthu_dotthu(kt_dt.idKhoanThuDotThu)
        for nopphi in nopphis:
            NopPhiService.delete_nopphi(nopphi.IDNopTien)
    
    # Xóa tất cả bản ghi KhoanThu_Has_DotThu
    for kt_dt in khoanthu_dotthus:
        KhoanThuHasDotThuService.delete(kt_dt.idKhoanThuDotThu)
    
    result = DotThuService.delete_dotthu(maDotThu)
    if result:
        return jsonify({'success': True, 'message': 'Xóa đợt thu thành công'}), 200
    else:
        return jsonify({'success': False, 'message': 'Đợt thu không tồn tại hoặc có lỗi xảy ra'}), 404
    
@tp.route('/dotthu/<int:maDotThu>/remove_hokhau/<int:maHoKhau>', methods=['DELETE'])
@login_required
def remove_hokhau(maDotThu, maHoKhau):
    if current_user.vaiTro not in ['Kế toán']:
        return jsonify({'success': False, 'message': 'Không có quyền thực hiện'}), 403

    # Lấy danh sách idKhoanThuDotThu của đợt thu
    khoanthu_dotthus = KhoanThuHasDotThuService.get_by_dotthu(maDotThu)
    kt_dt_ids = [kt_dt.idKhoanThuDotThu for kt_dt in khoanthu_dotthus]

    # Xóa các bản ghi NopPhi liên quan đến hộ khẩu trong đợt thu
    nopphis = NopPhiService.get_nopphis_by_hokhau(maHoKhau)
    for nopphi in nopphis:
        if nopphi.idKhoanThuDotThu in kt_dt_ids:
            if not NopPhiService.delete_nopphi(nopphi.IDNopTien):
                return jsonify({'success': False, 'message': f'Xóa bản ghi nộp phí cho hộ khẩu {maHoKhau} thất bại'}), 500

    return jsonify({'success': True, 'message': 'Xóa hộ khẩu thành công'}), 200

@tp.route('/dotthu/<int:maDotThu>/remove_khoanthu/<int:idKhoanThuDotThu>', methods=['DELETE'])
@login_required
def remove_khoanthu(maDotThu, idKhoanThuDotThu):
    if current_user.vaiTro not in ['Kế toán']:
        return jsonify({'success': False, 'message': 'Không có quyền thực hiện'}), 403

    # Xóa các bản ghi NopPhi liên quan trước
    nopphis = NopPhiService.get_nopphis_by_khoanthu_dotthu(idKhoanThuDotThu)
    for nopphi in nopphis:
        if not NopPhiService.delete_nopphi(nopphi.IDNopTien):
            return jsonify({'success': False, 'message': f'Xóa bản ghi nộp phí thất bại'}), 500

    # Xóa bản ghi KhoanThuHasDotThu
    if not KhoanThuHasDotThuService.delete(idKhoanThuDotThu):
        return jsonify({'success': False, 'message': 'Xóa khoản thu thất bại'}), 500

    return jsonify({'success': True, 'message': 'Xóa khoản thu thành công'}), 200