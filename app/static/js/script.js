/**
 * Restaurant Reservation App - Main JavaScript File
 * Handles interactivity and dynamic behavior
 */

document.addEventListener('DOMContentLoaded', function() {
    console.log('Restaurant Reservation App loaded');

    // Smooth scrolling for anchor links
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

    // Mobile hamburger toggle
    const hamburgerToggle = document.getElementById('hamburgerToggle');
    const mobileNav = document.getElementById('mobileNav');

    if (hamburgerToggle && mobileNav) {
        hamburgerToggle.addEventListener('click', function(e) {
            e.stopPropagation();
            mobileNav.classList.toggle('open');
            if (searchExpanded) searchExpanded.classList.remove('open');
            hamburgerToggle.textContent = mobileNav.classList.contains('open') ? '✕' : '☰';
        });
    }

    // Mobile search toggle
    const searchToggle = document.getElementById('searchToggle');
    const searchExpanded = document.getElementById('searchExpanded');

    if (searchToggle && searchExpanded) {
        searchToggle.addEventListener('click', function(e) {
            e.stopPropagation();
            searchExpanded.classList.toggle('open');
            if (mobileNav) mobileNav.classList.remove('open');
            if (hamburgerToggle) hamburgerToggle.textContent = '☰';
            if (searchExpanded.classList.contains('open')) {
                searchExpanded.querySelector('input').focus();
            }
        });
    }

    // Mobile group toggles
    document.querySelectorAll('.mobile-group-toggle').forEach(function(btn) {
        btn.addEventListener('click', function(e) {
            e.stopPropagation();
            const group = this.closest('.mobile-group');
            const menu = group.querySelector('.mobile-group-menu');
            const isOpen = menu.classList.contains('open');
            document.querySelectorAll('.mobile-group-menu').forEach(m => m.classList.remove('open'));
            document.querySelectorAll('.mobile-group').forEach(g => g.classList.remove('open'));
            if (!isOpen) {
                menu.classList.add('open');
                group.classList.add('open');
            }
        });
    });

    document.addEventListener('click', function(e) {
        if (mobileNav && hamburgerToggle &&
            !hamburgerToggle.contains(e.target) && !mobileNav.contains(e.target)) {
            mobileNav.classList.remove('open');
            hamburgerToggle.textContent = '☰';
        }
        if (searchExpanded && searchToggle &&
            !searchToggle.contains(e.target) && !searchExpanded.contains(e.target)) {
            searchExpanded.classList.remove('open');
        }
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
