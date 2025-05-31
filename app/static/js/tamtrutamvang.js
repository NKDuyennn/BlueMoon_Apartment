// DOM Elements
const addModal = document.getElementById('addTTTVModal');
const viewModal = document.getElementById('viewTTTVModal');
const editModal = document.getElementById('editTTTVModal');
const deleteModal = document.getElementById('deleteTTTVModal');
const addForm = document.getElementById('addTTTVForm');
const editForm = document.getElementById('editTTTVForm');
const deleteForm = document.getElementById('deleteTTTVForm');
const searchInput = document.getElementById('searchInput');

// Search functionality
searchInput.addEventListener('keyup', function() {
    const searchTerm = this.value.toLowerCase();
    const tableRows = document.querySelectorAll('.account-table tbody tr');

    tableRows.forEach(row => {
        const rowText = row.textContent.toLowerCase();
        if (rowText.includes(searchTerm)) {
            row.style.display = '';
        } else {
            row.style.display = 'none';
        }
    });
});

// Modal functions
function openAddModal() {
    addModal.style.display = 'block';
    addForm.reset();
}

function closeAddModal() {
    addModal.style.display = 'none';
}

function openViewModal() {
    viewModal.style.display = 'block';
}

function closeViewModal() {
    viewModal.style.display = 'none';
}

function openEditModal() {
    editModal.style.display = 'block';
}

function closeEditModal() {
    editModal.style.display = 'none';
}

function openDeleteModal() {
    deleteModal.style.display = 'block';
}

function closeDeleteModal() {
    deleteModal.style.display = 'none';
}

// Close modals when clicking outside
window.onclick = function(event) {
    if (event.target === addModal) {
        closeAddModal();
    }
    if (event.target === viewModal) {
        closeViewModal();
    }
    if (event.target === editModal) {
        closeEditModal();
    }
    if (event.target === deleteModal) {
        closeDeleteModal();
    }
};

// Load NhanKhau when a HoKhau is selected
function loadNhanKhauByHoKhau() {
    const maHoKhau = document.getElementById('maHoKhau').value;
    if (!maHoKhau) {
        document.getElementById('maNhanKhau').innerHTML = '<option value="">-- Chọn nhân khẩu --</option>';
        return;
    }
    
    fetch(`/tamtrutamvang/nhankhau-by-hokhau/${maHoKhau}`)
        .then(response => response.json())
        .then(data => {
            const nhanKhauSelect = document.getElementById('maNhanKhau');
            nhanKhauSelect.innerHTML = '<option value="">-- Chọn nhân khẩu --</option>';
            
            data.forEach(nk => {
                const option = document.createElement('option');
                option.value = nk.maNhanKhau;
                option.textContent = `${nk.maNhanKhau} - ${nk.hoTen}`;
                nhanKhauSelect.appendChild(option);
            });
        })
        .catch(error => {
            console.error('Error:', error);
            alert('Đã xảy ra lỗi khi lấy danh sách nhân khẩu');
        });
}

// Form submission handling
addForm.addEventListener('submit', function(e) {
    e.preventDefault();
    const formData = new FormData(addForm);

    fetch('/tamtrutamvang/add', {
        method: 'POST',
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            alert(data.message);
            closeAddModal();
            location.reload();
        } else {
            alert(data.message);
        }
    })
    .catch(error => {
        console.error('Error:', error);
        alert('Đã xảy ra lỗi khi thêm thông tin tạm trú/tạm vắng');
    });
});

// Update the edit form submission handler with validation
editForm.addEventListener('submit', function(e) {
    e.preventDefault();
    const tttvId = document.getElementById('edit-id').value;
    
    // Validate dates before submitting
    const ngayBatDau = document.getElementById('edit-ngayBatDau').value;
    const ngayKetThuc = document.getElementById('edit-ngayKetThuc').value;
    
    // Check if dates are in valid format
    const dateRegex = /^\d{4}-\d{2}-\d{2}$/;
    
    if (!dateRegex.test(ngayBatDau)) {
        alert('Ngày bắt đầu không đúng định dạng (YYYY-MM-DD)');
        return;
    }
    
    if (!dateRegex.test(ngayKetThuc)) {
        alert('Ngày kết thúc không đúng định dạng (YYYY-MM-DD)');
        return;
    }
    
    const formData = new FormData(editForm);

    fetch(`/tamtrutamvang/${tttvId}`, {
        method: 'PUT',
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            alert(data.message);
            closeEditModal();
            location.reload();
        } else {
            alert(data.message);
        }
    })
    .catch(error => {
        console.error('Error:', error);
        alert('Đã xảy ra lỗi khi cập nhật thông tin tạm trú/tạm vắng');
    });
});


deleteForm.addEventListener('submit', function(e) {
    e.preventDefault();
    const tttvId = document.getElementById('delete-id').value;

    fetch(`/tamtrutamvang/${tttvId}`, {
        method: 'DELETE'
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            alert(data.message);
            closeDeleteModal();
            location.reload();
        } else {
            alert(data.message);
        }
    })
    .catch(error => {
        console.error('Error:', error);
        alert('Đã xảy ra lỗi khi xóa thông tin tạm trú/tạm vắng');
    });
});

// TTTV operations
function viewTTTV(id) {
    fetch(`/tamtrutamvang/${id}`, {
        method: 'GET'
    })
    .then(response => response.json())
    .then(data => {
        document.getElementById('view-id').textContent = data.id;
        document.getElementById('view-loai').textContent = data.loai;
        document.getElementById('view-maNhanKhau').textContent = data.maNhanKhau;
        document.getElementById('view-ngayBatDau').textContent = data.ngayBatDau;
        document.getElementById('view-ngayKetThuc').textContent = data.ngayKetThuc;
        document.getElementById('view-lyDo').textContent = data.lyDo;
        document.getElementById('view-hoTen').textContent = data.hoTen;
        document.getElementById('view-qhVoiChuHo').textContent = data.qhVoiChuHo;
        document.getElementById('view-maHoKhau').textContent = data.maHoKhau;
        document.getElementById('view-ngaySinh').textContent = data.ngaySinh;
        document.getElementById('view-gioiTinh').textContent = data.gioiTinh;
        document.getElementById('view-quocTich').textContent = data.quocTich;
        document.getElementById('view-noiSinh').textContent = data.noiSinh;
        document.getElementById('view-cmnd').textContent = data.cmnd;
        
        openViewModal();
    })
    .catch(error => {
        console.error('Error:', error);
        alert('Đã xảy ra lỗi khi lấy thông tin tạm trú/tạm vắng');
    });
}

function editTTTV(id) {
    fetch(`/tamtrutamvang/${id}`, {
        method: 'GET'
    })
    .then(response => response.json())
    .then(data => {
        document.getElementById('edit-id').value = data.id;
        document.getElementById('edit-loai').value = data.loai;
        document.getElementById('edit-ngayBatDau').value = data.ngayBatDau;
        document.getElementById('edit-ngayKetThuc').value = data.ngayKetThuc;
        document.getElementById('edit-lyDo').value = data.lyDo;
        
        document.getElementById('edit-maNhanKhau').textContent = data.maNhanKhau;
        document.getElementById('edit-maNhanKhau-input').value = data.maNhanKhau;
        document.getElementById('edit-hoTen').textContent = data.hoTen;
        document.getElementById('edit-qhVoiChuHo').textContent = data.qhVoiChuHo;
        document.getElementById('edit-maHoKhau').textContent = data.maHoKhau;
        document.getElementById('edit-ngaySinh').textContent = data.ngaySinh;
        document.getElementById('edit-gioiTinh').textContent = data.gioiTinh;
        document.getElementById('edit-quocTich').textContent = data.quocTich;
        document.getElementById('edit-noiSinh').textContent = data.noiSinh;
        document.getElementById('edit-cmnd').textContent = data.cmnd;
        
        openEditModal();
    })
    .catch(error => {
        console.error('Error:', error);
        alert('Đã xảy ra lỗi khi lấy thông tin tạm trú/tạm vắng');
    });
}

function deleteTTTV(id) {
    document.getElementById('delete-id').value = id;
    openDeleteModal();
}