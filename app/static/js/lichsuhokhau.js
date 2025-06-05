// Search functionality
document.addEventListener('DOMContentLoaded', function() {
    // Khởi tạo phân trang khi trang được tải lên
    initPagination();
    
    const searchInput = document.getElementById('searchInput');
    if (searchInput) {
        searchInput.addEventListener('keyup', function() {
            const searchValue = this.value.toLowerCase();
            
            if (searchValue.trim() === '') {
                // Nếu ô tìm kiếm trống, hiển thị lại phân trang bình thường
                initPagination();
            } else {
                // Nếu có từ khóa tìm kiếm, lọc bảng
                filterTable(searchValue);
            }
        });
    }
});

// Modal functionality
const viewModal = document.getElementById('viewLichSuModal');

// =================== VIEW LICHSUHOKHAU FUNCTIONS ===================
function openViewModal(id) {
    // Show the modal
    viewModal.style.display = 'block';
    
    // Fetch lichsuhokhau details
    fetch(`/lichsuhokhau/${id}`, {
        method: 'GET'
    })
    .then(response => {
        if (!response.ok) {
            throw new Error('Không thể tải dữ liệu');
        }
        return response.json();
    })
    .then(data => {
        // Populate modal with data
        document.getElementById('viewId').textContent = data.id;
        document.getElementById('viewLoaiThayDoi').textContent = data.loaiThayDoi;
        document.getElementById('viewMaHoKhau').textContent = data.maHoKhau;
        document.getElementById('viewMaNhanKhau').textContent = data.maNhanKhau;
        document.getElementById('viewNoiDung').textContent = data.noiDung || 'Không có nội dung';
        
        // Format the date if it exists
        if (data.thoiGian) {
            document.getElementById('viewThoiGian').textContent = formatDate(data.thoiGian, true);
        } else {
            document.getElementById('viewThoiGian').textContent = '';
        }
    })
    .catch(error => {
        console.error('Error:', error);
        alert('Đã xảy ra lỗi khi lấy thông tin lịch sử hộ khẩu');
        closeViewModal();
    });
}

function closeViewModal() {
    viewModal.style.display = 'none';
}

// Close modal when clicking outside the modal content
window.onclick = function(event) {
    if (event.target === viewModal) {
        closeViewModal();
    }
};

// Helper function for date formatting
function formatDate(dateString, includeTime = false) {
    const date = new Date(dateString);
    
    if (isNaN(date.getTime())) {
        return '';
    }
    
    const formattedDate = `${String(date.getDate()).padStart(2, '0')}/${String(date.getMonth() + 1).padStart(2, '0')}/${date.getFullYear()}`;
    
    if (includeTime) {
        return `${formattedDate} ${String(date.getHours()).padStart(2, '0')}:${String(date.getMinutes()).padStart(2, '0')}`;
    }
    
    return formattedDate;
}

// Pagination functionality
function initPagination() {
    const rowsPerPage = 10;
    const rows = document.querySelectorAll('.lichsuhokhau-row');
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
        console.error("Không tìm thấy các phần tử phân trang");
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
    } else {
        console.log("Không có dữ liệu để hiển thị");
    }
}

// Go to specific page
function goToPage(pageNum) {
    const rowsPerPage = 10;
    const rows = document.querySelectorAll('.lichsuhokhau-row');
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
    const rows = document.querySelectorAll('.lichsuhokhau-row');
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
        
        // Update prev/next button event listeners
        prevButton.onclick = function() {
            const currentPage = parseInt(pageNumbers.dataset.currentPage || 1);
            if (currentPage > 1) {
                goToFilteredPage(currentPage - 1, filteredRows);
            }
        };
        
        nextButton.onclick = function() {
            const currentPage = parseInt(pageNumbers.dataset.currentPage || 1);
            if (currentPage < totalFilteredPages) {
                goToFilteredPage(currentPage + 1, filteredRows);
            }
        };
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
    const allRows = document.querySelectorAll('.lichsuhokhau-row');
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