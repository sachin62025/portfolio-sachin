// Wait for DOM to be fully loaded
document.addEventListener('DOMContentLoaded', function() {
    // Initialize AOS animation library
    AOS.init({
        duration: 800,
        easing: 'ease-in-out',
        once: true,
        mirror: false
    });

    // Initialize skill progress bars
    initSkillBars();

    // Add smooth scrolling to all navigation links
    document.querySelectorAll('.nav-link, .footer-nav a, .smooth-scroll').forEach(link => {
        link.addEventListener('click', function(e) {
            // Only if the link is an internal anchor
            if (this.getAttribute('href').startsWith('#')) {
                e.preventDefault();
                const targetId = this.getAttribute('href');
                const targetElement = document.querySelector(targetId);
                
                if (targetElement) {
                    window.scrollTo({
                        top: targetElement.offsetTop - 70,
                        behavior: 'smooth'
                    });
                    
                    // Close mobile menu if open
                    const navbarToggler = document.querySelector('.navbar-toggler');
                    const navbarCollapse = document.querySelector('.navbar-collapse');
                    if (navbarCollapse.classList.contains('show')) {
                        navbarToggler.click();
                    }
                }
            }
        });
    });

    // Form validation for contact form
    const contactForm = document.getElementById('contactForm');
    if (contactForm) {
        contactForm.addEventListener('submit', function(e) {
            let valid = true;
            
            // Reset previous validation messages
            document.querySelectorAll('.invalid-feedback').forEach(el => el.remove());
            document.querySelectorAll('.is-invalid').forEach(el => el.classList.remove('is-invalid'));
            
            // Validate name
            const nameInput = document.getElementById('name');
            if (!nameInput.value.trim()) {
                valid = false;
                addValidationError(nameInput, 'Please enter your name');
            }
            
            // Validate email
            const emailInput = document.getElementById('email');
            const emailPattern = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
            if (!emailInput.value.trim() || !emailPattern.test(emailInput.value.trim())) {
                valid = false;
                addValidationError(emailInput, 'Please enter a valid email address');
            }
            
            // Validate subject
            const subjectInput = document.getElementById('subject');
            if (!subjectInput.value.trim()) {
                valid = false;
                addValidationError(subjectInput, 'Please enter a subject');
            }
            
            // Validate message
            const messageInput = document.getElementById('message');
            if (!messageInput.value.trim() || messageInput.value.trim().length < 10) {
                valid = false;
                addValidationError(messageInput, 'Please enter a message (minimum 10 characters)');
            }
            
            // If form is not valid, prevent submission
            if (!valid) {
                e.preventDefault();
            }
        });
    }

    // Navbar color change on scroll
    window.addEventListener('scroll', function() {
        const navbar = document.querySelector('.navbar');
        if (window.scrollY > 50) {
            navbar.classList.add('navbar-scrolled');
        } else {
            navbar.classList.remove('navbar-scrolled');
        }
    });

    // Auto-hide alert messages after 5 seconds
    const alerts = document.querySelectorAll('.alert');
    if (alerts.length > 0) {
        setTimeout(() => {
            alerts.forEach(alert => {
                // Create fade out effect
                alert.style.opacity = '1';
                (function fadeOut() {
                    if ((alert.style.opacity -= 0.1) < 0) {
                        alert.style.display = 'none';
                    } else {
                        requestAnimationFrame(fadeOut);
                    }
                })();
            });
        }, 5000);
    }
});

// Initialize skill progress bars with animation
function initSkillBars() {
    const skillLevels = document.querySelectorAll('.skill-level');
    
    // Set up intersection observer to animate when visible
    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                // Get width from data attribute and apply it
                const width = entry.target.getAttribute('data-width');
                entry.target.style.width = width;
                
                // Stop observing after animation is triggered
                observer.unobserve(entry.target);
            }
        });
    }, { threshold: 0.1 });
    
    // Observe each skill level element
    skillLevels.forEach(skill => {
        observer.observe(skill);
    });
}

// Helper function to add validation error messages
function addValidationError(inputElement, message) {
    inputElement.classList.add('is-invalid');
    
    const feedbackDiv = document.createElement('div');
    feedbackDiv.className = 'invalid-feedback';
    feedbackDiv.textContent = message;
    
    inputElement.parentNode.appendChild(feedbackDiv);
}
