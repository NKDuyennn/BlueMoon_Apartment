// DOM Elements
const addModal = document.getElementById('addKhoanThuModal');
const editModal = document.getElementById('editKhoanThuModal');
const addForm = document.getElementById('addKhoanThuForm');
const editForm = document.getElementById('editKhoanThuForm');
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

function openEditModal() {
    editModal.style.display = 'block';
}

function closeEditModal() {
    editModal.style.display = 'none';
}

// Close modals when clicking outside
window.onclick = function(event) {
    if (event.target === addModal) {
        closeAddModal();
    }
    if (event.target === editModal) {
        closeEditModal();
    }
};

// Form submission handling
addForm.addEventListener('submit', function(e) {
    e.preventDefault();
    const formData = new FormData(addForm);

    fetch('/khoanthu/add', {
        method: 'POST',
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            alert(data.message);
            closeAddModal();
            location.reload(); // Reload to show the new khoanthu
        } else {
            alert(data.message);
        }
    })
    .catch(error => {
        console.error('Error:', error);
        alert('Đã xảy ra lỗi khi thêm khoản thu');
    });
});

editForm.addEventListener('submit', function(e) {
    e.preventDefault();
    const maKhoanThu = document.getElementById('editMaKhoanThu').value;

    const formData = {
        tenKhoanThu: document.getElementById('editTenKhoanThu').value,
        loaiKhoanThu: document.getElementById('editLoaiKhoanThu').value,
        soTien: document.getElementById('editSoTien').value,
        loaiSoTien: document.getElementById('editLoaiSoTien').value,
        ghiChu: document.getElementById('editGhiChu').value // Thêm trường ghiChu
    };

    fetch(`/khoanthu/${maKhoanThu}`, {
        method: 'PUT',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(formData)
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            alert(data.message);
            closeEditModal();
            location.reload(); // Reload to show updated khoanthu
        } else {
            alert(data.message);
        }
    })
    .catch(error => {
        console.error('Error:', error);
        alert('Đã xảy ra lỗi khi cập nhật khoản thu');
    });
});

// KhoanThu operations
function editKhoanThu(maKhoanThu) {
    // Fetch khoanthu details
    fetch(`/khoanthu/${maKhoanThu}`, {
        method: 'GET'
    })
    .then(response => response.json())
    .then(data => {
        document.getElementById('editMaKhoanThu').value = data.maKhoanThu;
        document.getElementById('editTenKhoanThu').value = data.tenKhoanThu;
        document.getElementById('editLoaiKhoanThu').value = data.loaiKhoanThu;
        document.getElementById('editSoTien').value = data.soTien;
        document.getElementById('editLoaiSoTien').value = data.loaiSoTien;
        document.getElementById('editGhiChu').value = data.ghiChu || ''; // Thêm trường ghiChu, đảm bảo không null

        openEditModal();
    })
    .catch(error => {
        console.error('Error:', error);
        alert('Đã xảy ra lỗi khi lấy thông tin khoản thu');
    });
}

function deleteKhoanThu(maKhoanThu) {
    if (confirm('Bạn có chắc chắn muốn xóa khoản thu này?')) {
        fetch(`/khoanthu/${maKhoanThu}`, {
            method: 'DELETE'
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                alert(data.message);
                location.reload(); // Reload to update the table
            } else {
                alert(data.message);
            }
        })
        .catch(error => {
            console.error('Error:', error);
            alert('Đã xảy ra lỗi khi xóa khoản thu');
        });
    }
}