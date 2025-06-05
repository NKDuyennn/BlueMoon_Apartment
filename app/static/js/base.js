document.addEventListener('DOMContentLoaded', function() {
    // Update current date and time
    updateDateTime();
    
    // Update time every minute
    setInterval(updateDateTime, 60000);
    
    // Active menu item highlight
    highlightActiveMenuItem();
});

// Function to update date and time in the header
function updateDateTime() {
    const now = new Date();
    
    // Format time (12-hour format with AM/PM)
    const hours = now.getHours();
    const minutes = now.getMinutes();
    const ampm = hours >= 12 ? 'PM' : 'AM';
    const formattedHours = hours % 12 || 12;
    const formattedMinutes = minutes < 10 ? '0' + minutes : minutes;
    const timeString = `${formattedHours}:${formattedMinutes} ${ampm}`;
    
    // Format date (Month DD, YYYY)
    const months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'];
    const month = months[now.getMonth()];
    const day = now.getDate();
    const year = now.getFullYear();
    const dateString = `${month} ${day < 10 ? '0' + day : day}, ${year}`;
    
    // Update DOM elements
    const timeElement = document.querySelector('.time');
    const dateElement = document.querySelector('.date');
    
    if (timeElement) timeElement.textContent = timeString;
    if (dateElement) dateElement.textContent = dateString;
}

// Function to highlight the current active menu item
function highlightActiveMenuItem() {
    // Get current path
    const currentPath = window.location.pathname;
    
    // Find all menu items
    const menuItems = document.querySelectorAll('.menu-item');
    
    // Loop through menu items and add active class to matching path
    menuItems.forEach(item => {
        const href = item.getAttribute('href');
        if (href && currentPath.includes(href)) {
            item.classList.add('active');
        } else {
            item.classList.remove('active');
        }
    });
}