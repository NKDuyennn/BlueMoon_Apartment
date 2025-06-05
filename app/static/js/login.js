document.addEventListener('DOMContentLoaded', function() {
    // Handle login form submission
    const loginForm = document.getElementById('loginForm');
    
    if (loginForm) {
        loginForm.addEventListener('submit', function(event) {
            event.preventDefault();
            
            const username = document.getElementById('username').value;
            const password = document.getElementById('password').value;
            
            // Basic validation
            if (!username || !password) {
                showError('Vui lòng nhập cả tên đăng nhập và mật khẩu.');
                return;
            }
            
            // Prepare data for POST request
            const loginData = {
                username: username,
                password: password
            };
            
            // Send login request to server
            fetch('/login', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(loginData)
            })
            .then(response => {
                if (response.redirected) {
                    // Nếu server chuyển hướng, client sẽ đi theo
                    window.location.href = response.url;
                } else {
                    // Xử lý phản hồi JSON cho trường hợp lỗi
                    return response.json().then(data => {
                        if (data.error) {
                            showError(data.error);
                        }
                    });
                }
            })
            .catch(error => {
                showError('Đã xảy ra lỗi kết nối. Vui lòng thử lại sau.');
                console.error('Login error:', error);
            });
        });
    }
    
    // Handle signup button click
    const signUpBtn = document.querySelector('.sign-up-btn');
    
    if (signUpBtn) {
        signUpBtn.addEventListener('click', function(event) {
            event.preventDefault();
            window.location.href = '/register';
        });
    }
    
    // Handle forgotten password link
    const forgotPasswordLink = document.querySelector('.forgot-password a');
    
    if (forgotPasswordLink) {
        forgotPasswordLink.addEventListener('click', function(event) {
            event.preventDefault();
            window.location.href = '/reset-password';
        });
    }
    
    // Helper function to show error messages
    function showError(message) {
        // Check if error message element exists, create if not
        let errorElement = document.getElementById('login-error');
        if (!errorElement) {
            errorElement = document.createElement('div');
            errorElement.id = 'login-error';
            errorElement.className = 'error-message';
            loginForm.prepend(errorElement);
        }
        
        // Display error message
        errorElement.textContent = message;
        errorElement.style.display = 'block';
    }
    
    // Helper function to show success messages
    function showSuccess(message) {
        // Check if success message element exists, create if not
        let successElement = document.getElementById('login-success');
        if (!successElement) {
            successElement = document.createElement('div');
            successElement.id = 'login-success';
            successElement.className = 'success-message';
            loginForm.prepend(successElement);
        }
        
        // Display success message
        successElement.textContent = message;
        successElement.style.display = 'block';
    }
});