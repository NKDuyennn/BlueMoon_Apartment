// DOM Elements
const addModal = document.getElementById('addAccountModal');
const editModal = document.getElementById('editAccountModal');
const addForm = document.getElementById('addAccountForm');
const editForm = document.getElementById('editAccountForm');
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

    fetch('/taikhoan/add', {
        method: 'POST',
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            alert(data.message);
            closeAddModal();
            location.reload(); // Reload to show the new account
        } else {
            alert(data.message);
        }
    })
    .catch(error => {
        console.error('Error:', error);
        alert('Đã xảy ra lỗi khi thêm tài khoản');
    });
});

editForm.addEventListener('submit', function(e) {
    e.preventDefault();
    const accountId = document.getElementById('editAccountId').value;

    const formData = {
        hoTen: document.getElementById('editHoTen').value,
        vaiTro: document.getElementById('editVaiTro').value,
        password: document.getElementById('editPassword').value
    };

    fetch(`/taikhoan/${accountId}`, {
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
            location.reload(); // Reload to show updated account
        } else {
            alert(data.message);
        }
    })
    .catch(error => {
        console.error('Error:', error);
        alert('Đã xảy ra lỗi khi cập nhật tài khoản');
    });
});

// Account operations
function editAccount(id) {
    // Fetch account details
    fetch(`/taikhoan/${id}`, {
        method: 'GET'
    })
    .then(response => response.json())
    .then(data => {
        document.getElementById('editAccountId').value = data.id;
        document.getElementById('editUsername').value = data.username;
        document.getElementById('editHoTen').value = data.hoTen;
        document.getElementById('editVaiTro').value = data.vaiTro;
        document.getElementById('editPassword').value = '';

        openEditModal();
    })
    .catch(error => {
        console.error('Error:', error);
        alert('Đã xảy ra lỗi khi lấy thông tin tài khoản');
    });
}

function deleteAccount(id) {
    if (confirm('Bạn có chắc chắn muốn xóa tài khoản này?')) {
        fetch(`/taikhoan/${id}`, {
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
            alert('Đã xảy ra lỗi khi xóa tài khoản');
        });
    }
}