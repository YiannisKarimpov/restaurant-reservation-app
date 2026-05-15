/**
 * Restaurant Reservation App - Main JavaScript File
 * Handles interactivity and dynamic behavior
 */

document.addEventListener('DOMContentLoaded', function() {
    console.log('Restaurant Reservation App loaded');
    
    // Add smooth scrolling for anchor links
    const links = document.querySelectorAll('a[href^="#"]');
    links.forEach(link => {
        link.addEventListener('click', function(e) {
            e.preventDefault();
            const targetId = this.getAttribute('href').substring(1);
            const targetElement = document.getElementById(targetId);
            if (targetElement) {
                targetElement.scrollIntoView({ behavior: 'smooth' });
            }
        });
    });
});

/**
 * Close alert messages after 5 seconds
 */
function closeAlert(alertElement) {
    setTimeout(() => {
        if (alertElement) {
            alertElement.style.transition = 'opacity 0.5s ease';
            alertElement.style.opacity = '0';
            setTimeout(() => alertElement.remove(), 500);
        }
    }, 5000);
}

// Auto-close alerts
document.querySelectorAll('.alert').forEach(alert => closeAlert(alert));
