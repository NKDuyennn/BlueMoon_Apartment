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

@hk.route('/hokhau/add', methods=['POST'])
@login_required
def add_new_hokhau():
    if current_user.vaiTro != 'admin':
        return jsonify({'success': False, 'message': 'Không có quyền thực hiện'}), 403
    
    data = request.form
    soNha = data.get('soNha')
    ngayLap = data.get('ngayLap')
    ngayCapNhat = data.get('ngayCapNhat')
    dienTich = data.get('dienTich')
    xeMay = data.get('xeMay', 0)
    oTo = data.get('oTo', 0)
    chuHo_val = data.get('chuHo')
    chuHo = int(chuHo_val) if chuHo_val else 0
    
    # Debug information
    print(f"Form data received: soNha={soNha}, ngayLap={ngayLap}, ngayCapNhat={ngayCapNhat}, dienTich={dienTich}, xeMay={xeMay}, oTo={oTo}, chuHo={chuHo}")

    ngayCapNhat = datetime.strptime(ngayCapNhat, '%Y-%m-%d').date() if ngayCapNhat else datetime.now().date()
    ngayLap = datetime.strptime(ngayLap, '%Y-%m-%d').date() if ngayLap else datetime.now().date()
    
    # Validate required fields
    if not all([soNha, ngayLap, ngayCapNhat, dienTich]):
        return jsonify({'success': False, 'message': 'Vui lòng điền đầy đủ thông tin (số nhà, ngày lập, ngày cập nhật, diện tích)'}), 400 
    
    try:
        dienTich = float(dienTich)
        xeMay = int(xeMay) if xeMay else 0
        oTo = int(oTo) if oTo else 0
    except ValueError:
        return jsonify({'success': False, 'message': 'Diện tích, số xe máy, số ô tô phải là số hợp lệ'}), 400

    # Create new household
    new_hokhau = HoKhauService.create_hokhau(chuHo, soNha, ngayLap, ngayCapNhat, dienTich, xeMay, oTo)
    
    if new_hokhau:
        return jsonify({'success': True, 'message': 'Tạo hộ khẩu thành công'}), 201
    else:
        return jsonify({'success': False, 'message': 'Hộ khẩu đã tồn tại'}), 400



@hk.route('/hokhau/<int:maHoKhau>/update', methods=['PUT'])
@login_required
def update_hokhau(maHoKhau):
    if current_user.vaiTro != 'admin':
        return jsonify({'success': False, 'message': 'Không có quyền thực hiện'}), 403

    data = request.form

    chuHo_val = data.get('chuHo')
    chuHo = int(chuHo_val) if chuHo_val and chuHo_val.isdigit() else 0

    soNha = data.get('soNha')
    ngayLap_str = data.get('ngayLap')
    ngayCapNhat_str = data.get('ngayCapNhat')
    dienTich = data.get('dienTich')
    xeMay = data.get('xeMay', 0)
    oTo = data.get('oTo', 0)

    # Parse dates
    try:
        ngayLap = datetime.strptime(ngayLap_str, '%Y-%m-%d').date()
        ngayCapNhat = datetime.strptime(ngayCapNhat_str, '%Y-%m-%d').date()
    except Exception:
        return jsonify({'success': False, 'message': 'Ngày không hợp lệ'}), 400

    # Validate required fields
    if not all([soNha, ngayLap, ngayCapNhat, dienTich]):
        return jsonify({'success': False, 'message': 'Vui lòng điền đầy đủ thông tin (số nhà, ngày lập, ngày cập nhật, diện tích)'}), 400

    try:
        dienTich = float(dienTich)
        xeMay = int(xeMay) if xeMay else 0
        oTo = int(oTo) if oTo else 0
    except ValueError:
        return jsonify({'success': False, 'message': 'Diện tích, số xe máy, số ô tô phải là số hợp lệ'}), 400

    # Get current household
    current_hokhau = HoKhau.query.get(maHoKhau)
    if not current_hokhau:
        return jsonify({'success': False, 'message': 'Không tìm thấy hộ khẩu'}), 404
    
    old_chuho = current_hokhau.chuHo
    
    # Handle household head change
    if chuHo == 0 and old_chuho > 0:
        # Update old household head's relationship
        old_chuho_nhankhau = NhanKhau.query.get(old_chuho)
        if old_chuho_nhankhau:
            old_chuho_nhankhau.qhVoiChuHo = "Khác"
            db.session.add(old_chuho_nhankhau)
            
            # Record this change in lichsuhokhau
            noiDung = f"Hộ khẩu ({maHoKhau}) CẬP NHẬT vai trò của Nhân khẩu (ID: {old_chuho}, Họ tên: {old_chuho_nhankhau.hoTen}) từ 'Chủ hộ' -> 'Khác', Hộ khẩu không có chủ hộ"
            
            lich_su = LichSuHoKhauService.create_lichsuhokhau(
                loaiThayDoi="Sửa",
                maHoKhau=int(maHoKhau),
                maNhanKhau=old_chuho,
                thoiGian=datetime.now(),
                noiDung=noiDung
            )
            
            if not lich_su:
                print("Không thể tạo lịch sử hộ khẩu cho việc xóa chủ hộ")
    
    # If changing household head
    if chuHo > 0 and chuHo != old_chuho:
        # Update old household head's relationship
        old_chuho_nhankhau = NhanKhau.query.get(old_chuho)
        if old_chuho_nhankhau:
            old_chuho_nhankhau.qhVoiChuHo = "Khác"
            db.session.add(old_chuho_nhankhau)
            noiDung = f"Hộ khẩu ({maHoKhau}) CẬP NHẬT vai trò của Nhân khẩu (ID: {old_chuho}, Họ tên: {old_chuho_nhankhau.hoTen}) từ 'Chủ hộ' -> 'Khác'"
            lich_su = LichSuHoKhauService.create_lichsuhokhau(
                loaiThayDoi="Sửa",
                maHoKhau=int(maHoKhau),
                maNhanKhau=old_chuho,
                thoiGian=datetime.now(),
                noiDung=noiDung
            )
            if not lich_su:
                print("Không thể tạo lịch sử hộ khẩu cho chủ hộ cũ")
        
        new_chuho_nhankhau = NhanKhau.query.get(chuHo)
        if new_chuho_nhankhau:
            new_chuho_nhankhau.qhVoiChuHo = "Chủ hộ"
            db.session.add(new_chuho_nhankhau)
            noiDung = f"Hộ khẩu ({maHoKhau}) CẬP NHẬT vai trò của Nhân khẩu (ID: {chuHo}, Họ tên: {new_chuho_nhankhau.hoTen}) thành 'Chủ hộ'"
            lich_su = LichSuHoKhauService.create_lichsuhokhau(
                loaiThayDoi="Sửa",
                maHoKhau=int(maHoKhau),
                maNhanKhau=chuHo,
                thoiGian=datetime.now(),
                noiDung=noiDung
            )
            if not lich_su:
                print("Không thể tạo lịch sử hộ khẩu cho chủ hộ mới")

    success = HoKhauService.update_HoKhau(maHoKhau, chuHo, soNha, ngayLap, ngayCapNhat, dienTich, xeMay, oTo)
    if success:
        return jsonify({'success': True, 'message': 'Cập nhật hộ khẩu thành công'}), 200
    else:
        return jsonify({'success': False, 'message': 'Cập nhật thất bại hoặc không tìm thấy hộ khẩu'}), 400



@hk.route('/hokhau/<int:maHoKhau>/delete', methods=['DELETE'])
@login_required
def delete_hokhau(maHoKhau):
    if current_user.vaiTro != 'admin':
        return jsonify({'success': False, 'message': 'Không có quyền thực hiện'}), 403
    
    result = HoKhauService.delete_hokhau(maHoKhau)

    if result:
         return jsonify({'success': True, 'message': 'Xóa hộ khẩu thành công'}), 200
    else:
        return jsonify({'success': False, 'message': 'Không tìm thấy hộ khẩu hoặc có lỗi xảy ra'}), 400
    

@hk.route('/hokhau/<int:maHoKhau>', methods=['GET'])
@login_required
def hokhau_chitiet(maHoKhau):
    hokhau = HoKhauService.get_hokhau_by_id(maHoKhau)
    nhankhaus = NhanKhauService.get_nhankhau_by_hoKhau(maHoKhau)
    if not hokhau:
        flash('Không tìm thấy hộ khẩu', 'danger')
        return redirect(url_for('hk.hokhau'))
    
    chu_ho = None
    if hokhau and hokhau.chuHo != 0:
        for nk in nhankhaus:
            if nk.maNhanKhau == hokhau.chuHo:
                chu_ho = nk.hoTen
                break

    return render_template('hokhau_chitiet.html', hokhau=hokhau, nhankhaus=nhankhaus, chu_ho=chu_ho)



@hk.route('/nhankhau/add', methods=['POST'])
@login_required
def create_nhankhau():
    if current_user.vaiTro != 'admin':
        return jsonify({'success': False, 'message': 'Không có quyền thực hiện'}), 403
    
    # Lấy dữ liệu từ request JSON
    data = request.json
    
    # Trích xuất các trường bắt buộc
    hoTen = data.get('hoTen')
    ngaySinh = data.get('ngaySinh')
    gioiTinh = data.get('gioiTinh')
    maHoKhau = data.get('maHoKhau')
    
    # Trích xuất các trường không bắt buộc
    quocTich = data.get('quocTich', 'Việt Nam')
    noiSinh = data.get('noiSinh')
    cmnd = data.get('cmnd')
    qhVoiChuHo = data.get('qhVoiChuHo')
    trangThai = data.get('trangThai', 'Thường trú')
    
    # Kiểm tra các trường bắt buộc
    if not all([hoTen, ngaySinh, gioiTinh, maHoKhau]):
        return jsonify({
            'success': False, 
            'message': 'Vui lòng điền đầy đủ các thông tin bắt buộc (họ tên, ngày sinh, giới tính)'
        }), 400
    
    # Chuyển đổi ngày sinh từ chuỗi sang đối tượng date
    try:
        ngaySinh = datetime.strptime(ngaySinh, '%Y-%m-%d').date()
    except ValueError:
        return jsonify({
            'success': False, 
            'message': 'Định dạng ngày sinh không hợp lệ. Sử dụng định dạng YYYY-MM-DD'
        }), 400
    
    # Kiểm tra xem hộ khẩu có tồn tại không
    ho_khau = HoKhauService.get_hokhau_by_id(int(maHoKhau))
    if not ho_khau:
        return jsonify({
            'success': False, 
            'message': 'Không tìm thấy hộ khẩu với mã đã cung cấp'
        }), 404
    
    # Tạo nhân khẩu mới
    try:
        new_nhankhau = NhanKhauService.create_nhankhau(
            hoTen=hoTen,
            ngaySinh=ngaySinh,
            gioiTinh=gioiTinh,
            maHoKhau=int(maHoKhau),
            quocTich=quocTich,
            noiSinh=noiSinh,
            cmnd=cmnd,
            qhVoiChuHo=qhVoiChuHo,
            trangThai=trangThai
        )
        
        # Thêm lịch sử nhân khẩu mới
        noiDung = f"Hộ khẩu ({maHoKhau}) THÊM Nhân khẩu (ID: {new_nhankhau.maNhanKhau}, Họ tên: {hoTen}, Giới tính: {gioiTinh}, Ngày sinh: {ngaySinh.strftime('%Y-%m-%d')}, CMND: {cmnd or 'Chưa có'})"

        lich_su = LichSuHoKhauService.create_lichsuhokhau(
            loaiThayDoi="Thêm",
            maHoKhau=int(maHoKhau),
            maNhanKhau=new_nhankhau.maNhanKhau,
            thoiGian=datetime.now(),
            noiDung=noiDung
        )
        
        if not lich_su:
            print("Không thể tạo lịch sử hộ khẩu")

        # Kiểm tra xem có phải là chủ hộ không và cập nhật hộ khẩu nếu cần
        if qhVoiChuHo == 'Chủ hộ':
            HoKhauService.update_HoKhau(
                maHoKhau=int(maHoKhau),
                chuHo=new_nhankhau.maNhanKhau,
                soNha=ho_khau.soNha,
                ngayLap=ho_khau.ngayLap,
                ngayCapNhat=datetime.now().date(),
                dienTich=ho_khau.dienTich,
                xeMay=ho_khau.xeMay,
                oTo=ho_khau.oTo
            )
        

        return jsonify({
            'success': True, 
            'message': 'Tạo nhân khẩu mới thành công',
            'maNhanKhau': new_nhankhau.maNhanKhau
        }), 201
        
    except Exception as e:
        print(f"Lỗi khi tạo nhân khẩu: {str(e)}")
        return jsonify({
            'success': False, 
            'message': f'Lỗi khi tạo nhân khẩu: {str(e)}'
        }), 500
    


# Route to get NhanKhau details
@hk.route('/nhankhau/<int:maNhanKhau>', methods=['GET'])
@login_required
def get_nhankhau(maNhanKhau):
    try:
        nhankhau = NhanKhauService.get_nhankhau_by_id(maNhanKhau)
        if not nhankhau:
            return jsonify({
                'success': False,
                'message': 'Không tìm thấy nhân khẩu'
            }), 404
        
        return jsonify({
            'success': True,
            'maNhanKhau': nhankhau.maNhanKhau,
            'hoTen': nhankhau.hoTen,
            'ngaySinh': nhankhau.ngaySinh.strftime('%Y-%m-%d'),
            'gioiTinh': nhankhau.gioiTinh,
            'cmnd': nhankhau.cmnd or '',
            'queQuan': nhankhau.noiSinh or '',
            'maHoKhau': nhankhau.maHoKhau,
            'quanHeChuHo': nhankhau.qhVoiChuHo or '',
            'quocTich': nhankhau.quocTich or 'Việt Nam',
            'trangThai': nhankhau.trangThai or 'Thường trú'
        }), 200
    
    except Exception as e:
        print(f"Lỗi khi lấy thông tin nhân khẩu: {str(e)}")
        return jsonify({
            'success': False,
            'message': f'Lỗi khi lấy thông tin nhân khẩu: {str(e)}'
        }), 500
    


# Route to update NhanKhau
@hk.route('/nhankhau/<int:maNhanKhau>', methods=['PUT'])
@login_required
def update_nhankhau(maNhanKhau):
    if current_user.vaiTro != 'admin':
        return jsonify({'success': False, 'message': 'Không có quyền thực hiện'}), 403
    
    # Lấy dữ liệu từ request JSON
    data = request.json
    print(data)
    # Trích xuất các trường
    hoTen = data.get('hoTen')
    ngaySinh = data.get('ngaySinh')
    gioiTinh = data.get('gioiTinh')
    maHoKhau = data.get('maHoKhau')
    cmnd = data.get('cmnd')
    queQuan = data.get('queQuan')
    quanHeChuHo = data.get('quanHeChuHo')
    
    # Kiểm tra các trường bắt buộc
    if not all([hoTen, ngaySinh, gioiTinh, maHoKhau]):
        return jsonify({
            'success': False,
            'message': 'Vui lòng điền đầy đủ các thông tin bắt buộc (họ tên, ngày sinh, giới tính)'
        }), 400
    
    # Chuyển đổi ngày sinh
    try:
        ngaySinh = datetime.strptime(ngaySinh, '%Y-%m-%d').date()
    except ValueError:
        return jsonify({
            'success': False,
            'message': 'Định dạng ngày sinh không hợp lệ. Sử dụng định dạng YYYY-MM-DD'
        }), 400
    
    # Kiểm tra hộ khẩu
    ho_khau = HoKhauService.get_hokhau_by_id(int(maHoKhau))
    if not ho_khau:
        return jsonify({
            'success': False,
            'message': 'Không tìm thấy hộ khẩu với mã đã cung cấp'
        }), 404
    
    # Kiểm tra nhân khẩu
    nhankhau = NhanKhauService.get_nhankhau_by_id(maNhanKhau)
    if not nhankhau:
        return jsonify({
            'success': False,
            'message': 'Không tìm thấy nhân khẩu'
        }), 404
    
    try:
        # Theo dõi các thay đổi để lưu vào lịch sử
        changes = []
        
        # Kiểm tra từng trường để xem có thay đổi không
        if nhankhau.hoTen != hoTen:
            changes.append(f"Họ tên: {nhankhau.hoTen} -> {hoTen}")
            
        if nhankhau.ngaySinh != ngaySinh:
            changes.append(f"Ngày sinh: {nhankhau.ngaySinh.strftime('%Y-%m-%d')} -> {ngaySinh.strftime('%Y-%m-%d')}")
            
        if nhankhau.gioiTinh != gioiTinh:
            changes.append(f"Giới tính: {nhankhau.gioiTinh} -> {gioiTinh}")
            
        if nhankhau.maHoKhau != int(maHoKhau):
            changes.append(f"Mã hộ khẩu: {nhankhau.maHoKhau} -> {maHoKhau}")
            
        if (nhankhau.cmnd or '') != (cmnd or ''):
            changes.append(f"CMND: {nhankhau.cmnd or 'Chưa có'} -> {cmnd or 'Chưa có'}")
            
        if (nhankhau.noiSinh or '') != (queQuan or ''):
            changes.append(f"Quê quán: {nhankhau.noiSinh or 'Chưa có'} -> {queQuan or 'Chưa có'}")
            
        if (nhankhau.qhVoiChuHo or '') != (quanHeChuHo or ''):
            changes.append(f"Quan hệ với chủ hộ: {nhankhau.qhVoiChuHo or 'Chưa có'} -> {quanHeChuHo or 'Chưa có'}")
        
        
        # Kiểm tra nếu mã hộ khẩu thay đổi và nhân khẩu là chủ hộ của hộ khẩu cũ
        old_maHoKhau = nhankhau.maHoKhau

        if nhankhau.maHoKhau != int(maHoKhau):
            old_ho_khau = HoKhauService.get_hokhau_by_id(nhankhau.maHoKhau)
            if old_ho_khau and old_ho_khau.chuHo == maNhanKhau:
                # Cập nhật chủ hộ của hộ khẩu cũ thành None
                HoKhauService.update_HoKhau(
                    maHoKhau=nhankhau.maHoKhau,
                    chuHo=0,
                    soNha=old_ho_khau.soNha,
                    ngayLap=old_ho_khau.ngayLap,
                    ngayCapNhat=datetime.now().date(),
                    dienTich=old_ho_khau.dienTich,
                    xeMay=old_ho_khau.xeMay,
                    oTo=old_ho_khau.oTo
                )
            # Kiểm tra nếu nhân khẩu chuyển đến hộ khẩu mới với vai trò là chủ hộ
            if quanHeChuHo == 'Chủ hộ':
                # Kiểm tra xem hộ khẩu mới đã có chủ hộ chưa
                if ho_khau.chuHo != 0 and ho_khau.chuHo != maNhanKhau:
                    # Lấy thông tin chủ hộ hiện tại của hộ khẩu mới
                    current_chuho = NhanKhauService.get_nhankhau_by_id(ho_khau.chuHo)
                    if current_chuho:
                        # Cập nhật quan hệ của chủ hộ hiện tại thành "Khác"
                        current_chuho.qhVoiChuHo = "Khác"
                        db.session.add(current_chuho)
                        
                        # Lưu lịch sử về việc thay đổi vai trò của chủ hộ hiện tại
                        noiDung_old_chuho = f"Hộ khẩu ({maHoKhau}) CẬP NHẬT vai trò của Nhân khẩu (ID: {ho_khau.chuHo}, Họ tên: {current_chuho.hoTen}) từ 'Chủ hộ' -> 'Khác'"
                        LichSuHoKhauService.create_lichsuhokhau(
                            loaiThayDoi="Sửa (Chuyển)",
                            maHoKhau=int(maHoKhau),
                            maNhanKhau=ho_khau.chuHo,
                            thoiGian=datetime.now(),
                            noiDung=noiDung_old_chuho
                        )
        else:
            if quanHeChuHo == 'Chủ hộ':
                # Kiểm tra xem hộ khẩu hiện tại đã có chủ hộ chưa
                if ho_khau.chuHo != 0 and ho_khau.chuHo != maNhanKhau:
                    # Lấy thông tin chủ hộ hiện tại của hộ khẩu hiện tại
                    current_chuho = NhanKhauService.get_nhankhau_by_id(ho_khau.chuHo)
                    if current_chuho:
                        # Cập nhật quan hệ của chủ hộ hiện tại thành "Khác"
                        current_chuho.qhVoiChuHo = "Khác"
                        db.session.add(current_chuho)
                        
                        # Lưu lịch sử về việc thay đổi vai trò của chủ hộ hiện tại
                        noiDung_old_chuho = f"Hộ khẩu ({maHoKhau}) CẬP NHẬT vai trò của Nhân khẩu (ID: {ho_khau.chuHo}, Họ tên: {current_chuho.hoTen}) từ 'Chủ hộ' -> 'Khác'"
                        LichSuHoKhauService.create_lichsuhokhau(
                            loaiThayDoi="Sửa",
                            maHoKhau=int(maHoKhau),
                            maNhanKhau=ho_khau.chuHo,
                            thoiGian=datetime.now(),
                            noiDung=noiDung_old_chuho
                        )
                HoKhauService.update_HoKhau(
                    maHoKhau=int(maHoKhau),
                    chuHo=maNhanKhau,
                    soNha=ho_khau.soNha,
                    ngayLap=ho_khau.ngayLap,
                    ngayCapNhat=datetime.now().date(),
                    dienTich=ho_khau.dienTich,
                    xeMay=ho_khau.xeMay,
                    oTo=ho_khau.oTo
                )
            
        # Cập nhật nhân khẩu
        NhanKhauService.update_nhankhau(
            maNhanKhau=maNhanKhau,
            hoTen=hoTen,
            ngaySinh=ngaySinh,
            gioiTinh=gioiTinh,
            maHoKhau=int(maHoKhau),
            cmnd=cmnd,
            noiSinh=queQuan,
            qhVoiChuHo=quanHeChuHo
        )
        
        # Cập nhật chủ hộ nếu cần
        if quanHeChuHo == 'Chủ hộ':
            HoKhauService.update_HoKhau(
                maHoKhau=int(maHoKhau),
                chuHo=maNhanKhau,
                soNha=ho_khau.soNha,
                ngayLap=ho_khau.ngayLap,
                ngayCapNhat=datetime.now().date(),
                dienTich=ho_khau.dienTich,
                xeMay=ho_khau.xeMay,
                oTo=ho_khau.oTo
            )
        
        # Nếu có sự thay đổi, thêm vào lịch sử hộ khẩu
        if changes:
            # Tạo nội dung ghi log
            noiDung = f"Hộ khẩu ({old_maHoKhau}) SỬA Nhân khẩu ({maNhanKhau}): " + "; ".join(changes)
            
            # Lưu vào lịch sử hộ khẩu
            LichSuHoKhauService.create_lichsuhokhau(
                loaiThayDoi="Sửa",
                maHoKhau=int(old_maHoKhau),
                maNhanKhau=maNhanKhau,
                thoiGian=datetime.now(),
                noiDung=noiDung
            )
            
            # Nếu hộ khẩu thay đổi, lưu thêm bản ghi cho cả hộ khẩu cũ và hộ khẩu mới
            if old_maHoKhau != int(maHoKhau):
                # Bản ghi cho hộ khẩu cũ (đánh dấu XÓA)
                noiDung_old = f"Hộ khẩu ({old_maHoKhau}) XÓA Nhân khẩu ({maNhanKhau}): Chuyển sang hộ khẩu mới ({maHoKhau})"
                LichSuHoKhauService.create_lichsuhokhau(
                    loaiThayDoi="Xóa (Chuyển)",
                    maHoKhau=old_maHoKhau,
                    maNhanKhau=maNhanKhau,
                    thoiGian=datetime.now(),
                    noiDung=noiDung_old
                )
                    # Bản ghi cho hộ khẩu mới (đánh dấu THÊM)
                noiDung_new = f"Hộ khẩu ({maHoKhau}) THÊM Nhân khẩu (ID: {maNhanKhau}, Họ tên: {hoTen}, Giới tính: {gioiTinh}, Ngày sinh: {ngaySinh.strftime('%Y-%m-%d')}, CMND: {cmnd or 'Chưa có'})"
                LichSuHoKhauService.create_lichsuhokhau(
                    loaiThayDoi="Thêm (Chuyển)",
                    maHoKhau=int(maHoKhau),
                    maNhanKhau=maNhanKhau,
                    thoiGian=datetime.now(),
                    noiDung=noiDung_new
                )

        return jsonify({
            'success': True,
            'message': 'Cập nhật nhân khẩu thành công'
        }), 200
    
    except Exception as e:
        print(f"Lỗi khi cập nhật nhân khẩu: {str(e)}")
        return jsonify({
            'success': False,
            'message': f'Lỗi khi cập nhật nhân khẩu: {str(e)}'
        }), 500




# Route to delete NhanKhau
@hk.route('/nhankhau/<int:maNhanKhau>', methods=['DELETE'])
@login_required
def delete_nhankhau(maNhanKhau):
    if current_user.vaiTro != 'admin':
        return jsonify({'success': False, 'message': 'Không có quyền thực hiện'}), 403
    
    # Kiểm tra nhân khẩu
    nhankhau = NhanKhauService.get_nhankhau_by_id(maNhanKhau)
    if not nhankhau:
        return jsonify({
            'success': False,
            'message': 'Không tìm thấy nhân khẩu'
        }), 404
    
    try:
        # Lưu thông tin trước khi xóa để ghi vào lịch sử
        maHoKhau = nhankhau.maHoKhau
        hoTen = nhankhau.hoTen
        gioiTinh = nhankhau.gioiTinh
        ngaySinh = nhankhau.ngaySinh
        cmnd = nhankhau.cmnd
        
        # Tạo nội dung ghi log
        noiDung = f"Hộ khẩu ({maHoKhau}) XÓA Nhân khẩu ({maNhanKhau}): Họ tên: {hoTen}, Giới tính: {gioiTinh}, Ngày sinh: {ngaySinh.strftime('%Y-%m-%d')}, CMND: {cmnd or 'Chưa có'}"
        
        # Lưu vào lịch sử hộ khẩu
        LichSuHoKhauService.create_lichsuhokhau(
            loaiThayDoi="Xóa",
            maHoKhau=maHoKhau,
            maNhanKhau=0,  # Đặt là 0 vì nhân khẩu sẽ bị xóa
            thoiGian=datetime.now(),
            noiDung=noiDung
        )
        
        # Xóa nhân khẩu
        NhanKhauService.delete_nhankhau(maNhanKhau)
        
        # Nếu là chủ hộ, cập nhật hộ khẩu
        ho_khau = HoKhauService.get_hokhau_by_id(nhankhau.maHoKhau)
        if ho_khau and ho_khau.chuHo == maNhanKhau:
            HoKhauService.update_HoKhau(
                maHoKhau=nhankhau.maHoKhau,
                chuHo=0,
                soNha=ho_khau.soNha,
                ngayLap=ho_khau.ngayLap,
                ngayCapNhat=datetime.now().date(),
                dienTich=ho_khau.dienTich,
                xeMay=ho_khau.xeMay,
                oTo=ho_khau.oTo
            )
        
        return jsonify({
            'success': True,
            'message': 'Xóa nhân khẩu thành công'
        }), 200
    
    except Exception as e:
        print(f"Lỗi khi xóa nhân khẩu: {str(e)}")
        return jsonify({
            'success': False,
            'message': f'Lỗi khi xóa nhân khẩu: {str(e)}'
        }), 500
    


@hk.route('/lichsuhokhau', methods=['GET'])
@login_required
def lichsuhokhau():
    lichsuhokhaus = LichSuHoKhauService.get_all_lichsuhokhau()
    return render_template('lichsuhokhau.html', lichsuhokhau=lichsuhokhaus)



@hk.route('/lichsuhokhau/<int:id>', methods=['GET'])
@login_required
def get_lichsuhokhau(id):
    try:
        lichsuhokhau = LichSuHoKhauService.get_lichsuhokhau_by_id(id)
        if not lichsuhokhau:
            return jsonify({
                'success': False,
                'message': 'Không tìm thấy lịch sử hộ khẩu'
            }), 404
        
        return jsonify({
            'success': True,
            'id': lichsuhokhau.id,
            'loaiThayDoi': lichsuhokhau.loaiThayDoi,
            'maHoKhau': lichsuhokhau.maHoKhau,
            'maNhanKhau': lichsuhokhau.maNhanKhau,
            'noiDung': lichsuhokhau.noiDung or '',
            'thoiGian': lichsuhokhau.thoiGian.strftime('%Y-%m-%d %H:%M:%S') if lichsuhokhau.thoiGian else None
        }), 200
    
    except Exception as e:
        print(f"Lỗi khi lấy thông tin lịch sử hộ khẩu: {str(e)}")
        return jsonify({
            'success': False,
            'message': f'Lỗi khi lấy thông tin lịch sử hộ khẩu: {str(e)}'
        }), 500
    


@hk.route('/tamtrutamvang', methods=['GET'])
@login_required
def tamtrutamvang():
    tamtrutamvangs = TamTruTamVangService.get_all_tamtrutamvang_with_nhankhau()
    hokhaus = HoKhauService.get_all_hokhaus()
    nhankhaus = NhanKhauService.get_all_nhankhau()
    return render_template('tamtrutamvang.html', tamtrutamvangs=tamtrutamvangs, nhankhaus=nhankhaus, hokhaus=hokhaus)

@hk.route('/tamtrutamvang/nhankhau-by-hokhau/<int:maHoKhau>', methods=['GET'])
@login_required
def get_nhankhau_by_hokhau(maHoKhau):
    nhankhau_list = NhanKhauService.get_nhankhau_by_hoKhau(maHoKhau)
    result = []
    for nk in nhankhau_list:
        result.append({
            'maNhanKhau': nk.maNhanKhau,
            'hoTen': nk.hoTen
        })
    return jsonify(result)



@hk.route('/tamtrutamvang/add', methods=['POST'])
@login_required
def add_new_tamtrutamvang():
    if current_user.vaiTro != 'admin':
        return jsonify({'success': False, 'message': 'Không có quyền thực hiện'}), 403
    
    try:
        maNhanKhau = request.form.get('maNhanKhau')
        loai = request.form.get('loai')
        ngayBatDau = datetime.strptime(request.form.get('ngayBatDau'), '%Y-%m-%d').date()
        ngayKetThuc = datetime.strptime(request.form.get('ngayKetThuc'), '%Y-%m-%d').date()
        lyDo = request.form.get('lyDo')
        
        if not all([maNhanKhau, loai, ngayBatDau, ngayKetThuc, lyDo]):
            return jsonify({
                'success': False,
                'message': 'Vui lòng điền đầy đủ thông tin'
            }), 400
        
        # Kiểm tra nhân khẩu
        nhankhau = NhanKhauService.get_nhankhau_by_id(int(maNhanKhau))
        if not nhankhau:
            return jsonify({
                'success': False,
                'message': 'Không tìm thấy nhân khẩu'
            }), 404
        
        # Thêm bản ghi tạm trú/tạm vắng
        result = TamTruTamVangService.create_tamtrutamvang(loai, maNhanKhau, ngayBatDau, ngayKetThuc, lyDo)
        
        if result:
            # Cập nhật trạng thái nhân khẩu
            old_trangThai = nhankhau.trangThai
            NhanKhauService.update_nhankhau(
                maNhanKhau=int(maNhanKhau),
                hoTen=nhankhau.hoTen,
                ngaySinh=nhankhau.ngaySinh,
                gioiTinh=nhankhau.gioiTinh,
                maHoKhau=nhankhau.maHoKhau,
                cmnd=nhankhau.cmnd,
                noiSinh=nhankhau.noiSinh,
                qhVoiChuHo=nhankhau.qhVoiChuHo,
                trangThai=loai
            )
            
            # Thêm bản ghi lịch sử hộ khẩu
            noiDung = f"Hộ khẩu ({nhankhau.maHoKhau}) CẬP NHẬT trạng thái Nhân khẩu (ID: {maNhanKhau}, Họ tên: {nhankhau.hoTen}) từ '{old_trangThai}' -> '{loai}' do {loai} từ {ngayBatDau} đến {ngayKetThuc}, lý do: {lyDo}"
            lich_su = LichSuHoKhauService.create_lichsuhokhau(
                loaiThayDoi="Sửa",
                maHoKhau=nhankhau.maHoKhau,
                maNhanKhau=int(maNhanKhau),
                thoiGian=datetime.now(),
                noiDung=noiDung
            )
            
            if not lich_su:
                print("Không thể tạo lịch sử hộ khẩu cho cập nhật trạng thái")
            
            return jsonify({
                'success': True,
                'message': 'Thêm thông tin tạm trú/tạm vắng thành công'
            }), 200
        else:
            return jsonify({
                'success': False,
                'message': 'Không thể thêm thông tin tạm trú/tạm vắng'
            }), 400
    except Exception as e:
        print(f"Đã xảy ra lỗi: {str(e)}")
        return jsonify({
            'success': False,
            'message': f'Đã xảy ra lỗi: {str(e)}'
        }), 500
    


@hk.route('/tamtrutamvang/<int:id>', methods=['GET'])
@login_required
def get_tamtrutamvang(id):
    try:
        tttv = TamTruTamVangService.get_tamtrutamvang_by_id(id)
        if not tttv:
            return jsonify({
                'success': False,
                'message': 'Không tìm thấy thông tin tạm trú/tạm vắng'
            })
        
        # Format dates for display
        ngayBatDau = tttv.ngayBatDau.strftime('%Y-%m-%d') if tttv.ngayBatDau else None
        ngayKetThuc = tttv.ngayKetThuc.strftime('%Y-%m-%d') if tttv.ngayKetThuc else None
        
        # Get NhanKhau info
        nhankhau = NhanKhauService.get_nhankhau_by_id(tttv.maNhanKhau)
        if not nhankhau:
            return jsonify({
                'success': False,
                'message': 'Không tìm thấy thông tin nhân khẩu'
            })
        
        ngaySinh = nhankhau.ngaySinh.strftime('%d/%m/%Y') if nhankhau.ngaySinh else None
        
        result = {
            'id': tttv.id,
            'loai': tttv.loai,
            'maNhanKhau': tttv.maNhanKhau,
            'ngayBatDau': ngayBatDau,
            'ngayKetThuc': ngayKetThuc,
            'lyDo': tttv.lyDo,
            'hoTen': nhankhau.hoTen,
            'qhVoiChuHo': nhankhau.qhVoiChuHo,
            'maHoKhau': nhankhau.maHoKhau,
            'ngaySinh': ngaySinh,
            'gioiTinh': nhankhau.gioiTinh,
            'quocTich': nhankhau.quocTich,
            'noiSinh': nhankhau.noiSinh,
            'cmnd': nhankhau.cmnd
        }
        
        return jsonify(result)
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Đã xảy ra lỗi: {str(e)}'
        })



@hk.route('/tamtrutamvang/<int:id>', methods=['PUT'])  # Make sure the route has the ID parameter
@login_required
def update_tamtrutamvang(id):
    if current_user.vaiTro != 'admin':
        return jsonify({'success': False, 'message': 'Không có quyền thực hiện'}), 403
    
    try:
        loai = request.form.get('loai')
        ngayBatDau_str = request.form.get('ngayBatDau')
        ngayKetThuc_str = request.form.get('ngayKetThuc')
        lyDo = request.form.get('lyDo')
        
        if not all([loai, ngayBatDau_str, ngayKetThuc_str, lyDo]):
            return jsonify({
                'success': False,
                'message': 'Vui lòng điền đầy đủ thông tin'
            }), 400
        
        try:
            ngayBatDau = datetime.strptime(ngayBatDau_str, '%Y-%m-%d').date()
            ngayKetThuc = datetime.strptime(ngayKetThuc_str, '%Y-%m-%d').date()
        except ValueError:
            return jsonify({
                'success': False,
                'message': 'Ngày không đúng định dạng (YYYY-MM-DD)'
            }), 400
        
        # Lấy thông tin tạm trú/tạm vắng hiện tại
        tttv = TamTruTamVangService.get_tamtrutamvang_by_id(id)
        if not tttv:
            return jsonify({
                'success': False,
                'message': 'Không tìm thấy thông tin tạm trú/tạm vắng'
            }), 404
        
        # Lấy thông tin nhân khẩu
        nhankhau = NhanKhauService.get_nhankhau_by_id(tttv.maNhanKhau)
        if not nhankhau:
            return jsonify({
                'success': False,
                'message': 'Không tìm thấy nhân khẩu'
            }), 404
        
        # Cập nhật bản ghi tạm trú/tạm vắng
        result = TamTruTamVangService.update_tamtrutamvang(id, loai, ngayBatDau, ngayKetThuc, lyDo)
        
        if result:
            # Cập nhật trạng thái nhân khẩu
            old_trangThai = nhankhau.trangThai
            NhanKhauService.update_nhankhau(
                maNhanKhau=tttv.maNhanKhau,
                hoTen=nhankhau.hoTen,
                ngaySinh=nhankhau.ngaySinh,
                gioiTinh=nhankhau.gioiTinh,
                maHoKhau=nhankhau.maHoKhau,
                cmnd=nhankhau.cmnd,
                noiSinh=nhankhau.noiSinh,
                qhVoiChuHo=nhankhau.qhVoiChuHo,
                trangThai=loai
            )
            
            # Thêm bản ghi lịch sử hộ khẩu
            noiDung = f"Hộ khẩu ({nhankhau.maHoKhau}) CẬP NHẬT trạng thái Nhân khẩu (ID: {tttv.maNhanKhau}, Họ tên: {nhankhau.hoTen}) từ '{old_trangThai}' -> '{loai}' do {loai} từ {ngayBatDau} đến {ngayKetThuc}, lý do: {lyDo}"
            lich_su = LichSuHoKhauService.create_lichsuhokhau(
                loaiThayDoi="Sửa",
                maHoKhau=nhankhau.maHoKhau,
                maNhanKhau=tttv.maNhanKhau,
                thoiGian=datetime.now(),
                noiDung=noiDung
            )
            
            if not lich_su:
                print("Không thể tạo lịch sử hộ khẩu cho cập nhật trạng thái")
            
            return jsonify({
                'success': True,
                'message': 'Cập nhật thông tin tạm trú/tạm vắng thành công'
            }), 200
        else:
            return jsonify({
                'success': False,
                'message': 'Không thể cập nhật thông tin tạm trú/tạm vắng'
            }), 400
    except Exception as e:
        print(f"Đã xảy ra lỗi: {str(e)}")
        return jsonify({
            'success': False,
            'message': f'Đã xảy ra lỗi: {str(e)}'
        }), 500



@hk.route('/tamtrutamvang/<int:id>', methods=['DELETE'])
@login_required
def delete_tamtrutamvang(id):
    if current_user.vaiTro != 'admin':
        return jsonify({'success': False, 'message': 'Không có quyền thực hiện'}), 403
    
    try:
        tttv = TamTruTamVangService.get_tamtrutamvang_by_id(id)
        if not tttv:
            return jsonify({
                'success': False,
                'message': 'Không tìm thấy thông tin tạm trú/tạm vắng'
            }), 404
        
        nhankhau = NhanKhauService.get_nhankhau_by_id(tttv.maNhanKhau)
        if not nhankhau:
            return jsonify({
                'success': False,
                'message': 'Không tìm thấy nhân khẩu'
            }), 404
        
        result = TamTruTamVangService.delete_tamtrutamvang(id)
        
        if result:
            # Cập nhật trạng thái nhân khẩu về Thường trú
            old_trangThai = nhankhau.trangThai
            NhanKhauService.update_nhankhau(
                maNhanKhau=tttv.maNhanKhau,
                hoTen=nhankhau.hoTen,
                ngaySinh=nhankhau.ngaySinh,
                gioiTinh=nhankhau.gioiTinh,
                maHoKhau=nhankhau.maHoKhau,
                cmnd=nhankhau.cmnd,
                noiSinh=nhankhau.noiSinh,
                qhVoiChuHo=nhankhau.qhVoiChuHo,
                trangThai='Thường trú'
            )
            
            # Thêm bản ghi lịch sử hộ khẩu
            noiDung = f"Hộ khẩu ({nhankhau.maHoKhau}) CẬP NHẬT trạng thái Nhân khẩu (ID: {tttv.maNhanKhau}, Họ tên: {nhankhau.hoTen}) từ '{old_trangThai}' -> 'Thường trú' do xóa thông tin {tttv.loai}"
            lich_su = LichSuHoKhauService.create_lichsuhokhau(
                loaiThayDoi="Sửa",
                maHoKhau=nhankhau.maHoKhau,
                maNhanKhau=tttv.maNhanKhau,
                thoiGian=datetime.now(),
                noiDung=noiDung
            )
            
            if not lich_su:
                print("Không thể tạo lịch sử hộ khẩu cho cập nhật trạng thái")
            
            return jsonify({
                'success': True,
                'message': 'Xóa thông tin tạm trú/tạm vắng thành công'
            }), 200
        else:
            return jsonify({
                'success': False,
                'message': 'Không thể xóa thông tin tạm trú/tạm vắng'
            }), 400
    except Exception as e:
        print(f"Đã xảy ra lỗi: {str(e)}")
        return jsonify({
            'success': False,
            'message': f'Đã xảy ra lỗi: {str(e)}'
        }), 500