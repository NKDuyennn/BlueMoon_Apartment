// Constants for modal elements
const createNhanKhauModal = document.getElementById('createNhanKhauModal');
const viewNhanKhauModal = document.getElementById('viewNhanKhauModal');
const editNhanKhauModal = document.getElementById('editNhanKhauModal');
const deleteNhanKhauModal = document.getElementById('deleteNhanKhauModal');

// Helper function to format date for display
function formatDate(dateString) {
    if (!dateString) return '';
    const date = new Date(dateString);
    return date.toLocaleDateString('vi-VN');
}

// Helper function to format date for input fields
function formatDateForInput(dateString) {
    if (!dateString) return '';
    const date = new Date(dateString);
    return date.toISOString().split('T')[0];
}

// =================== CREATE NHANKHAU FUNCTIONS ===================
function openCreateNhanKhauModal() {
    createNhanKhauModal.style.display = 'block';
}

function closeCreateNhanKhauModal() {
    createNhanKhauModal.style.display = 'none';
}

// Handle form submission for creating a new NhanKhau
document.getElementById('createNhanKhauForm').addEventListener('submit', function(e) {
    e.preventDefault();
    
    // Create FormData object from the form
    const formData = new FormData(this);
    
    // Convert FormData to JSON
    const data = {};
    formData.forEach((value, key) => {
        data[key] = value;
    });
    
    // Send data to the server
    fetch('/nhankhau/add', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(data)
    })
    .then(response => {
        if (!response.ok) {
            throw new Error('Lỗi khi tạo nhân khẩu mới');
        }
        return response.json();
    })
    .then(data => {
        // Show success message
        alert('Đã tạo nhân khẩu mới thành công!');
        
        // Close the modal
        closeCreateNhanKhauModal();
        
        // Reload the page to show the new NhanKhau
        window.location.reload();
    })
    .catch(error => {
        alert('Lỗi: ' + error.message);
    });
});

// =================== VIEW NHANKHAU FUNCTIONS ===================
function openViewModal(maNhanKhau) {
    viewNhanKhauModal.style.display = 'block';
    
    // Fetch nhân khẩu details
    fetch(`/nhankhau/${maNhanKhau}`, {
        method: 'GET'
    })
    .then(response => response.json())
    .then(data => {
        document.getElementById('viewMaNhanKhau').textContent = data.maNhanKhau;
        document.getElementById('viewHoTen').textContent = data.hoTen;
        document.getElementById('viewNgaySinh').textContent = formatDate(data.ngaySinh);
        document.getElementById('viewGioiTinh').textContent = data.gioiTinh;
        document.getElementById('viewCMND').textContent = data.cmnd;
        document.getElementById('viewQueQuan').textContent = data.queQuan;
        document.getElementById('viewMaHoKhau').textContent = data.maHoKhau;
        document.getElementById('viewQuanHeChuHo').textContent = data.quanHeChuHo;
    })
    .catch(error => {
        console.error('Error:', error);
        alert('Đã xảy ra lỗi khi lấy thông tin nhân khẩu');
    });
}

function closeViewModal() {
    viewNhanKhauModal.style.display = 'none';
}

// =================== EDIT NHANKHAU FUNCTIONS ===================
function openNhanKhauEditModal(maNhanKhau) {
    editNhanKhauModal.style.display = 'block';
    
    // Fetch nhân khẩu details
    fetch(`/nhankhau/${maNhanKhau}`, {
        method: 'GET'
    })
    .then(response => response.json())
    .then(data => {
        document.getElementById('editMaNhanKhau').value = data.maNhanKhau;
        document.getElementById('editHoTen').value = data.hoTen;
        document.getElementById('editNgaySinh').value = formatDateForInput(data.ngaySinh);
        document.getElementById('editGioiTinh').value = data.gioiTinh;
        document.getElementById('editCMND').value = data.cmnd;
        document.getElementById('editQueQuan').value = data.queQuan;
        document.getElementById('editMaHoKhau0').value = data.maHoKhau;
        console.log('Mã hộ khẩu (GET):', data.maHoKhau);
        document.getElementById('editQuanHeChuHo').value = data.quanHeChuHo;
        
    })
    .catch(error => {
        console.error('Error:', error);
        alert('Đã xảy ra lỗi khi lấy thông tin nhân khẩu');
    });
}

function closeNhanKhauEditModal() {
    editNhanKhauModal.style.display = 'none';
}

// Handle form submission for updating NhanKhau
document.getElementById('editNhanKhauForm').addEventListener('submit', function(e) {
    e.preventDefault();
    updateNhanKhau();
});

// Updated function to properly handle form submission
function updateNhanKhau() {
    const maNhanKhau = document.getElementById('editMaNhanKhau').value;

    const formData = {
        hoTen: document.getElementById('editHoTen').value,
        ngaySinh: document.getElementById('editNgaySinh').value,
        gioiTinh: document.getElementById('editGioiTinh').value,
        cmnd: document.getElementById('editCMND').value,
        queQuan: document.getElementById('editQueQuan').value,
        maHoKhau: document.getElementById('editMaHoKhau0').value,
        quanHeChuHo: document.getElementById('editQuanHeChuHo').value
    };

    
    fetch(`/nhankhau/${maNhanKhau}`, {
        method: 'PUT',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(formData)
    })
    .then(response => {
        if (!response.ok) {
            // Log the response for debugging
            return response.json().then(errorData => {
                console.error('Server error:', errorData);
                throw new Error(`Server responded with ${response.status}: ${errorData.message || 'Unknown error'}`);
            });
        }
        return response.json();
    })
    .then(data => {
        if (data.success) {
            alert(data.message);
            closeNhanKhauEditModal();
            // Reload to see changes
            location.reload();
        } else {
            alert(data.message || 'Cập nhật không thành công');
        }
    })
    .catch(error => {
        console.error('Error:', error);
        alert(`Đã xảy ra lỗi khi cập nhật nhân khẩu: ${error.message}`);
    });
}

// =================== DELETE NHANKHAU FUNCTIONS ===================
function openDeleteModal(maNhanKhau, hoTen) {
    deleteNhanKhauModal.style.display = 'block';
    document.getElementById('deleteNhanKhauId').value = maNhanKhau;
    document.getElementById('deleteNhanKhauName').textContent = hoTen;
}

function closeDeleteModal() {
    deleteNhanKhauModal.style.display = 'none';
}

function confirmDeleteNhanKhau() {
    const maNhanKhau = document.getElementById('deleteNhanKhauId').value;
    
    fetch(`/nhankhau/${maNhanKhau}`, {
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
        alert('Đã xảy ra lỗi khi xóa nhân khẩu');
    });
}

// =================== GLOBAL EVENT LISTENERS ===================
// Close modals when clicking outside of them
window.onclick = function(event) {
    if (event.target === createNhanKhauModal) {
        closeCreateNhanKhauModal();
    } else if (event.target === viewNhanKhauModal) {
        closeViewModal();
    } else if (event.target === editNhanKhauModal) {
        closeNhanKhauEditModal();
    } else if (event.target === deleteNhanKhauModal) {
        closeDeleteModal();
    }
};