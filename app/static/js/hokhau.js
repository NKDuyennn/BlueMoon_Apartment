// DOM Elements
let addModal, editModal, confirmDeleteModal, addForm, editForm, searchInput, searchMembers;

document.addEventListener('DOMContentLoaded', function() {
    // Initialize DOM elements
    addModal = document.getElementById('addHoKhauModal');
    editModal = document.getElementById('editHoKhauModal');
    confirmDeleteModal = document.getElementById('confirmDeleteModal');
    addForm = document.getElementById('addHoKhauForm');
    editForm = document.getElementById('editHoKhauForm');
    searchInput = document.getElementById('searchInput');
    searchMembers = document.getElementById('searchMembers');

    // Set default date values
    const today = new Date().toISOString().split('T')[0];
    
    // Set date fields for add form
    const addDateFields = document.querySelectorAll('#addHoKhauForm [id$="_display"], #addHoKhauForm [id$="Lap"], #addHoKhauForm [id$="CapNhat"]');
    addDateFields.forEach(field => {
        if (field) field.value = today;
    });
    
    // Set date fields for edit form
    const editDateFields = document.querySelectorAll('#editHoKhauForm [id$="_display"], #editHoKhauForm [id$="CapNhat"]');
    editDateFields.forEach(field => {
        if (field) field.value = today;
    });

    // Initialize search functionality
    if (searchInput) {
        searchInput.addEventListener('keyup', function() {
            const searchTerm = this.value.toLowerCase();
            filterTable(searchTerm);
        });
    }

    // Initialize search for members table
    if (searchMembers) {
        searchMembers.addEventListener('keyup', function() {
            const searchTerm = this.value.toLowerCase();
            const tableRows = document.querySelectorAll('.account-table tbody tr');
            
            tableRows.forEach(row => {
                const rowText = row.textContent.toLowerCase();
                if (rowText.includes(searchTerm)) {
                    row.style.display = '';
                    row.classList.add('visible');
                } else {
                    row.style.display = 'none';
                    row.classList.remove('visible');
                }
            });
        });
    }

    // Initialize pagination
    initPagination();

    // Initialize form submission handlers
    if (addForm) {
        addForm.addEventListener('submit', handleAddFormSubmit);
    }

    if (editForm) {
        editForm.addEventListener('submit', handleEditFormSubmit);
    }

    // Modal close on outside click
    window.onclick = function(event) {
        if (event.target === addModal) {
            closeAddModal();
        } else if (event.target === editModal) {
            closeHoKhauEditModal();
        } else if (event.target === confirmDeleteModal) {
            closeConfirmDeleteModal();
        }
    };

    // Initialize all delete buttons to use the confirmation modal
    initDeleteButtons();
});

// Initialize delete buttons to show confirmation first
function initDeleteButtons() {
    const deleteButtons = document.querySelectorAll('.delete-btn, button[onclick^="deleteHoKhau"]');
    
    deleteButtons.forEach(button => {
        // Remove the original onclick handler
        const originalOnClick = button.getAttribute('onclick');
        let maHoKhau = null;
        
        if (originalOnClick) {
            // Extract maHoKhau from the onclick attribute
            const match = originalOnClick.match(/deleteHoKhau\(['"]?([^'"()]*)['"]?\)/);
            if (match && match[1]) {
                maHoKhau = match[1];
            }
            button.removeAttribute('onclick');
        } else {
            // If there's no onclick, try to get maHoKhau from data attribute
            maHoKhau = button.dataset.maHoKhau;
        }
        
        if (maHoKhau) {
            // Set up the new click handler to show confirmation
            button.addEventListener('click', function(e) {
                e.preventDefault();
                confirmDeleteHoKhau(maHoKhau);
            });
        }
    });
}

// Modal functions
function openAddModal() {
    if (!addModal) return;
    addModal.style.display = 'block';
    if (addForm) addForm.reset();
    
    // Set date values
    const today = new Date().toISOString().split('T')[0];
    document.querySelectorAll('#addHoKhauForm [id$="_display"], #addHoKhauForm [id$="Lap"], #addHoKhauForm [id$="CapNhat"]').forEach(field => {
        if (field) field.value = today;
    });
}

function closeAddModal() {
    if (addModal) addModal.style.display = 'none';
}

function openHoKhauEditModal() {
    if (editModal) editModal.style.display = 'block';
}

function closeHoKhauEditModal() {
    if (editModal) editModal.style.display = 'none';
}

function confirmDeleteHoKhau(maHoKhau) {
    if (!confirmDeleteModal) return;
    confirmDeleteModal.style.display = 'block';
    
    const confirmBtn = document.getElementById('confirmDeleteBtn');
    if (confirmBtn) {
        // Remove any previous event listeners
        const newConfirmBtn = confirmBtn.cloneNode(true);
        confirmBtn.parentNode.replaceChild(newConfirmBtn, confirmBtn);
        
        // Add new click handler
        newConfirmBtn.addEventListener('click', function() {
            deleteHoKhau(maHoKhau);
            closeConfirmDeleteModal();
        });
    }
}

function closeConfirmDeleteModal() {
    if (confirmDeleteModal) confirmDeleteModal.style.display = 'none';
}

// Form submission handlers
function handleAddFormSubmit(e) {
    e.preventDefault();
    const formData = new FormData(addForm);
    
    // Debug logging
    console.log("Form data being submitted:");
    for (let pair of formData.entries()) {
        console.log(pair[0] + ': ' + pair[1]);
    }
    
    // Make sure chuHo is properly included
    if (!formData.has('chuHo')) {
        formData.append('chuHo', '0');
    }

    fetch('/hokhau/add', {
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
        alert('Đã xảy ra lỗi khi thêm hộ khẩu');
    });
}

function handleEditFormSubmit(e) {
    e.preventDefault();
    const formData = new FormData(editForm);
    const maHoKhau = document.getElementById('editMaHoKhau') ? 
                     document.getElementById('editMaHoKhau').value : 
                     document.querySelector('h1').textContent.split('Mã ')[1].trim();
    
    // Debug logging
    console.log("Form data being submitted:");
    for (let pair of formData.entries()) {
        console.log(pair[0] + ': ' + pair[1]);
    }

    // Make sure chuHo is properly included
    if (!formData.has('chuHo')) {
        formData.append('chuHo', '0');
    }

    fetch(`/hokhau/${maHoKhau}/update`, {
        method: 'PUT',
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            alert(data.message);
            closeHoKhauEditModal();
            location.reload();
        } else {
            alert(data.message);
        }
    })
    .catch(error => {
        console.error('Error:', error);
        alert('Đã xảy ra lỗi khi cập nhật hộ khẩu');
    });
}

// Delete functionality
function deleteHoKhau(maHoKhau) {
    fetch(`/hokhau/${maHoKhau}/delete`, {
        method: 'DELETE',
        headers: {
            'X-CSRFToken': getCSRFToken(),
            'Content-Type': 'application/json'
        }
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            alert(data.message);
            window.location.href = '/hokhau'; // Redirect to hokhau list
        } else {
            alert(data.message || 'Có lỗi xảy ra khi xóa hộ khẩu');
        }
    })
    .catch(error => {
        console.error('Error:', error);
        alert('Đã xảy ra lỗi khi xóa hộ khẩu');
    });
}

// Helper function to get CSRF token
function getCSRFToken() {
    // Try from meta tag
    const metaTag = document.querySelector('meta[name="csrf-token"]');
    if (metaTag) {
        return metaTag.getAttribute('content');
    }
    
    // Try from cookie
    const cookie = document.cookie.split(';').find(c => c.trim().startsWith('csrf_token='));
    if (cookie) {
        return cookie.split('=')[1];
    }
    
    return '';
}

// Helper function to show alerts
function showAlert(type, message) {
    const alertDiv = document.createElement('div');
    alertDiv.className = `alert alert-${type}`;
    alertDiv.textContent = message;
    
    const container = document.querySelector('.container');
    if (container) {
        container.insertBefore(alertDiv, container.firstChild.nextSibling);
        
        // Automatically remove alert after 5 seconds
        setTimeout(() => {
            alertDiv.remove();
        }, 5000);
    }
}

// Pagination functionality
function initPagination() {
    const rowsPerPage = 10;
    const rows = document.querySelectorAll('.hokhau-row');
    const totalRows = rows.length;
    const totalPages = Math.ceil(totalRows / rowsPerPage);
    
    // Get UI elements
    const pageNumbers = document.getElementById('page-numbers');
    const prevButton = document.getElementById('prev-page');
    const nextButton = document.getElementById('next-page');
    const startRecord = document.getElementById('start-record');
    const endRecord = document.getElementById('end-record');
    const totalRecords = document.getElementById('total-records');
    
    // Exit if pagination elements aren't found
    if (!pageNumbers || !prevButton || !nextButton || !startRecord || !endRecord || !totalRecords) {
        return;
    }
    
    // Update total records
    totalRecords.textContent = totalRows;
    
    // Clear old page numbers
    pageNumbers.innerHTML = '';
    
    // Create page number buttons
    for (let i = 1; i <= totalPages; i++) {
        const pageNumber = document.createElement('div');
        pageNumber.classList.add('page-number');
        pageNumber.textContent = i;
        pageNumber.dataset.page = i;
        pageNumber.addEventListener('click', function() {
            goToPage(i);
        });
        pageNumbers.appendChild(pageNumber);
    }
    
    // Handle prev/next buttons
    prevButton.addEventListener('click', function() {
        const currentPage = parseInt(pageNumbers.dataset.currentPage || 1);
        if (currentPage > 1) {
            goToPage(currentPage - 1);
        }
    });
    
    nextButton.addEventListener('click', function() {
        const currentPage = parseInt(pageNumbers.dataset.currentPage || 1);
        if (currentPage < totalPages) {
            goToPage(currentPage + 1);
        }
    });
    
    // Default to first page
    if (totalPages > 0) {
        goToPage(1);
    }
}

// Go to specific page
function goToPage(pageNum) {
    const rowsPerPage = 10;
    const rows = document.querySelectorAll('.hokhau-row');
    const totalRows = rows.length;
    const totalPages = Math.ceil(totalRows / rowsPerPage);
    
    // Get UI elements
    const pageNumbers = document.getElementById('page-numbers');
    const prevButton = document.getElementById('prev-page');
    const nextButton = document.getElementById('next-page');
    const startRecord = document.getElementById('start-record');
    const endRecord = document.getElementById('end-record');
    
    if (!pageNumbers || !prevButton || !nextButton || !startRecord || !endRecord) {
        return;
    }
    
    // Calculate start and end indexes
    const startIndex = (pageNum - 1) * rowsPerPage;
    const endIndex = Math.min(startIndex + rowsPerPage, totalRows);
    
    // Hide all rows
    rows.forEach(row => {
        row.classList.remove('visible');
    });
    
    // Show rows for current page
    for (let i = startIndex; i < endIndex; i++) {
        rows[i].classList.add('visible');
    }
    
    // Update display info
    startRecord.textContent = totalRows > 0 ? startIndex + 1 : 0;
    endRecord.textContent = endIndex;
    
    // Update page button states
    const pageButtons = document.querySelectorAll('.page-number');
    pageButtons.forEach(btn => {
        btn.classList.remove('active');
        if (parseInt(btn.dataset.page) === pageNum) {
            btn.classList.add('active');
        }
    });
    
    // Update prev/next button states
    prevButton.disabled = pageNum === 1;
    nextButton.disabled = pageNum === totalPages;
    
    // Save current page
    pageNumbers.dataset.currentPage = pageNum;
}

// Filter table by search term
function filterTable(searchTerm) {
    const rowsPerPage = 10;
    const rows = document.querySelectorAll('.hokhau-row');
    const filteredRows = [];
    
    // Filter rows by keyword
    rows.forEach(row => {
        const rowText = row.textContent.toLowerCase();
        if (rowText.includes(searchTerm)) {
            row.dataset.filtered = 'true';
            filteredRows.push(row);
        } else {
            row.dataset.filtered = 'false';
            row.classList.remove('visible');
        }
    });
    
    // Get UI elements
    const pageNumbers = document.getElementById('page-numbers');
    const prevButton = document.getElementById('prev-page');
    const nextButton = document.getElementById('next-page');
    const startRecord = document.getElementById('start-record');
    const endRecord = document.getElementById('end-record');
    const totalRecords = document.getElementById('total-records');
    
    if (!pageNumbers || !prevButton || !nextButton || !startRecord || !endRecord || !totalRecords) {
        return;
    }
    
    // Calculate pages for filtered results
    const totalFilteredRows = filteredRows.length;
    const totalFilteredPages = Math.ceil(totalFilteredRows / rowsPerPage);
    
    // Update total records display
    totalRecords.textContent = totalFilteredRows;
    
    // Clear old page numbers
    pageNumbers.innerHTML = '';
    
    // Create new page number buttons
    for (let i = 1; i <= totalFilteredPages; i++) {
        const pageNumber = document.createElement('div');
        pageNumber.classList.add('page-number');
        pageNumber.textContent = i;
        pageNumber.dataset.page = i;
        pageNumber.addEventListener('click', function() {
            goToFilteredPage(i, filteredRows);
        });
        pageNumbers.appendChild(pageNumber);
    }
    
    // Handle empty results
    if (totalFilteredPages === 0) {
        startRecord.textContent = '0';
        endRecord.textContent = '0';
        prevButton.disabled = true;
        nextButton.disabled = true;
    } else {
        // Show first page of filtered results
        goToFilteredPage(1, filteredRows);
        
        // Handle prev/next buttons
        prevButton.addEventListener('click', function() {
            const currentPage = parseInt(pageNumbers.dataset.currentPage || 1);
            if (currentPage > 1) {
                goToFilteredPage(currentPage - 1, filteredRows);
            }
        });
        
        nextButton.addEventListener('click', function() {
            const currentPage = parseInt(pageNumbers.dataset.currentPage || 1);
            if (currentPage < totalFilteredPages) {
                goToFilteredPage(currentPage + 1, filteredRows);
            }
        });
    }
}

// Go to filtered page
function goToFilteredPage(pageNum, filteredRows) {
    const rowsPerPage = 10;
    const totalFilteredRows = filteredRows.length;
    const totalFilteredPages = Math.ceil(totalFilteredRows / rowsPerPage);
    
    // Get UI elements
    const pageNumbers = document.getElementById('page-numbers');
    const prevButton = document.getElementById('prev-page');
    const nextButton = document.getElementById('next-page');
    const startRecord = document.getElementById('start-record');
    const endRecord = document.getElementById('end-record');
    
    if (!pageNumbers || !prevButton || !nextButton || !startRecord || !endRecord) {
        return;
    }
    
    // Calculate start and end indexes
    const startIndex = (pageNum - 1) * rowsPerPage;
    const endIndex = Math.min(startIndex + rowsPerPage, totalFilteredRows);
    
    // Hide all rows
    const allRows = document.querySelectorAll('.hokhau-row');
    allRows.forEach(row => {
        row.classList.remove('visible');
    });
    
    // Show rows for current page
    for (let i = startIndex; i < endIndex; i++) {
        filteredRows[i].classList.add('visible');
    }
    
    // Update display info
    startRecord.textContent = totalFilteredRows > 0 ? startIndex + 1 : 0;
    endRecord.textContent = endIndex;
    
    // Update page button states
    const pageButtons = document.querySelectorAll('.page-number');
    pageButtons.forEach(btn => {
        btn.classList.remove('active');
        if (parseInt(btn.dataset.page) === pageNum) {
            btn.classList.add('active');
        }
    });
    
    // Update prev/next button states
    prevButton.disabled = pageNum === 1;
    nextButton.disabled = pageNum === totalFilteredPages;
    
    // Save current page
    pageNumbers.dataset.currentPage = pageNum;
}

