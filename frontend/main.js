// ============================================================
// Bright Minds - Main JavaScript File
// Shared functionality across all pages
// ============================================================

// ===== NAVBAR HAMBURGER MENU =====
document.addEventListener('DOMContentLoaded', function() {
    // Initialize hamburger menu
    const hamburger = document.getElementById('hamburger');
    const navLinks = document.querySelector('.nav-links');
    
    if (hamburger) {
        hamburger.addEventListener('click', function() {
            if (navLinks.style.display === 'flex') {
                navLinks.style.display = 'none';
            } else {
                navLinks.style.display = 'flex';
            }
        });
    }

    // Close mobile menu when clicking on a link (optional)
    const mobileLinks = document.querySelectorAll('.nav-links a');
    mobileLinks.forEach(link => {
        link.addEventListener('click', () => {
            if (window.innerWidth <= 600) {
                navLinks.style.display = 'none';
            }
        });
    });

    // ===== SCROLL ANIMATIONS =====
    const animateOnScroll = function() {
        const elements = document.querySelectorAll('.feature-card, .step, .course-card, .value-card, .team-card');
        
        elements.forEach(element => {
            const elementPosition = element.getBoundingClientRect().top;
            const screenPosition = window.innerHeight;
            
            if (elementPosition < screenPosition - 50) {
                element.style.opacity = '1';
                element.style.transform = 'translateY(0)';
            }
        });
    };

    // Set initial styles for animation
    const animatedElements = document.querySelectorAll('.feature-card, .step, .course-card, .value-card, .team-card');
    animatedElements.forEach(element => {
        element.style.opacity = '0';
        element.style.transform = 'translateY(30px)';
        element.style.transition = 'opacity 0.6s ease, transform 0.6s ease';
    });

    // Trigger animations on scroll
    window.addEventListener('scroll', animateOnScroll);
    animateOnScroll(); // Run once on load

    // ===== ACTIVE NAVIGATION LINK =====
    const currentPage = window.location.pathname.split('/').pop();
    const navItems = document.querySelectorAll('.nav-links a');
    
    navItems.forEach(item => {
        const href = item.getAttribute('href');
        if (href === currentPage || (currentPage === '' && href === 'index.html')) {
            item.classList.add('active');
        } else if (currentPage === '/' && href === 'index.html') {
            item.classList.add('active');
        }
    });
});

// ===== SMOOTH SCROLL FOR ANCHOR LINKS =====
document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function(e) {
        const target = document.querySelector(this.getAttribute('href'));
        if (target) {
            e.preventDefault();
            target.scrollIntoView({
                behavior: 'smooth',
                block: 'start'
            });
        }
    });
});

// ===== TOOLTIP FUNCTIONALITY (for disability.html tabs) =====
function switchTab(tabId, element) {
    // Hide all tab panels
    const panels = document.querySelectorAll('.tab-panel');
    panels.forEach(panel => {
        panel.classList.remove('active');
    });
    
    // Show selected panel
    const selectedPanel = document.getElementById(`tab-${tabId}`);
    if (selectedPanel) {
        selectedPanel.classList.add('active');
    }
    
    // Update active state on buttons
    const buttons = document.querySelectorAll('.tab-btn');
    buttons.forEach(btn => {
        btn.classList.remove('active');
    });
    
    if (element) {
        element.classList.add('active');
    }
}

// ===== PROGRESS BAR UPDATE (for assessment.html) =====
function updateProgressBar(current, total) {
    const progressFill = document.querySelector('.quiz-progress-fill');
    if (progressFill) {
        const percentage = (current / total) * 100;
        progressFill.style.width = `${percentage}%`;
    }
}

// ===== SCORE ANIMATION =====
function animateScore(element, start, end, duration = 1000) {
    let startTimestamp = null;
    const step = (timestamp) => {
        if (!startTimestamp) startTimestamp = timestamp;
        const progress = Math.min((timestamp - startTimestamp) / duration, 1);
        const currentValue = Math.floor(progress * (end - start) + start);
        if (element) {
            element.textContent = currentValue;
        }
        if (progress < 1) {
            window.requestAnimationFrame(step);
        }
    };
    window.requestAnimationFrame(step);
}

// ===== LOCAL STORAGE HELPERS =====
const Storage = {
    save: (key, data) => {
        try {
            localStorage.setItem(`brightminds_${key}`, JSON.stringify(data));
            return true;
        } catch (e) {
            console.error('Storage save error:', e);
            return false;
        }
    },
    
    get: (key) => {
        try {
            const data = localStorage.getItem(`brightminds_${key}`);
            return data ? JSON.parse(data) : null;
        } catch (e) {
            console.error('Storage get error:', e);
            return null;
        }
    },
    
    remove: (key) => {
        try {
            localStorage.removeItem(`brightminds_${key}`);
            return true;
        } catch (e) {
            console.error('Storage remove error:', e);
            return false;
        }
    },
    
    clear: () => {
        try {
            Object.keys(localStorage).forEach(key => {
                if (key.startsWith('brightminds_')) {
                    localStorage.removeItem(key);
                }
            });
            return true;
        } catch (e) {
            console.error('Storage clear error:', e);
            return false;
        }
    }
};

// ===== USER PROGRESS TRACKING =====
const UserProgress = {
    saveQuizScore: (subject, score, total) => {
        const quizzes = Storage.get('quiz_scores') || [];
        quizzes.push({
            subject,
            score,
            total,
            date: new Date().toISOString(),
            percentage: (score / total) * 100
        });
        Storage.save('quiz_scores', quizzes.slice(-10)); // Keep last 10
    },
    
    getBestScore: (subject) => {
        const quizzes = Storage.get('quiz_scores') || [];
        const subjectQuizzes = quizzes.filter(q => q.subject === subject);
        if (subjectQuizzes.length === 0) return null;
        return Math.max(...subjectQuizzes.map(q => q.percentage));
    },
    
    getAverageScore: (subject) => {
        const quizzes = Storage.get('quiz_scores') || [];
        const subjectQuizzes = quizzes.filter(q => q.subject === subject);
        if (subjectQuizzes.length === 0) return null;
        const sum = subjectQuizzes.reduce((acc, q) => acc + q.percentage, 0);
        return sum / subjectQuizzes.length;
    },
    
    getRecentScores: (limit = 5) => {
        const quizzes = Storage.get('quiz_scores') || [];
        return quizzes.slice(-limit).reverse();
    }
};

// ===== THEME TOGGLE (Optional - Light/Dark Mode) =====
const ThemeManager = {
    init: function() {
        const savedTheme = Storage.get('theme') || 'light';
        this.setTheme(savedTheme);
        this.createToggleButton();
    },
    
    setTheme: function(theme) {
        if (theme === 'dark') {
            document.body.classList.add('dark-theme');
        } else {
            document.body.classList.remove('dark-theme');
        }
        Storage.save('theme', theme);
    },
    
    toggle: function() {
        const isDark = document.body.classList.contains('dark-theme');
        this.setTheme(isDark ? 'light' : 'dark');
    },
    
    createToggleButton: function() {
        // Only add if doesn't exist
        if (document.getElementById('themeToggle')) return;
        
        const button = document.createElement('button');
        button.id = 'themeToggle';
        button.innerHTML = '🌙';
        button.style.cssText = `
            position: fixed;
            bottom: 20px;
            right: 20px;
            width: 50px;
            height: 50px;
            border-radius: 50%;
            background: var(--primary);
            color: white;
            border: none;
            cursor: pointer;
            font-size: 1.5rem;
            box-shadow: 0 4px 12px rgba(0,0,0,0.15);
            z-index: 1000;
            transition: all 0.3s ease;
        `;
        button.onclick = () => this.toggle();
        document.body.appendChild(button);
    }
};

// ===== DARK THEME STYLES (Add to styles.css if you want dark mode) =====
// Add this to styles.css if you want dark mode support:
/*
body.dark-theme {
    --bg: #1a1a2e;
    --bg-card: #16213e;
    --text: #eee;
    --text-muted: #aaa;
    --border: #2a2a4a;
}
*/

// ===== FORM VALIDATION HELPERS =====
const FormValidator = {
    validateEmail: (email) => {
        const re = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
        return re.test(email);
    },
    
    validatePhone: (phone) => {
        const re = /^[\d\s\-()+]{10,15}$/;
        return re.test(phone);
    },
    
    showError: (input, message) => {
        const errorDiv = input.nextElementSibling;
        if (errorDiv && errorDiv.classList.contains('error-message')) {
            errorDiv.textContent = message;
        } else {
            const div = document.createElement('div');
            div.className = 'error-message';
            div.textContent = message;
            div.style.color = 'var(--accent)';
            div.style.fontSize = '0.8rem';
            div.style.marginTop = '0.25rem';
            input.parentNode.insertBefore(div, input.nextSibling);
        }
        input.style.borderColor = 'var(--accent)';
    },
    
    clearError: (input) => {
        const errorDiv = input.nextElementSibling;
        if (errorDiv && errorDiv.classList.contains('error-message')) {
            errorDiv.remove();
        }
        input.style.borderColor = 'var(--border)';
    }
};

// ===== LOADING SPINNER =====
const LoadingSpinner = {
    show: (element) => {
        const spinner = document.createElement('div');
        spinner.className = 'loading-spinner';
        spinner.innerHTML = '<div class="spinner"></div>';
        element.appendChild(spinner);
    },
    
    hide: (element) => {
        const spinner = element.querySelector('.loading-spinner');
        if (spinner) spinner.remove();
    }
};

// Add spinner styles (add to styles.css if needed)
const spinnerStyles = `
.loading-spinner {
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background: rgba(0,0,0,0.5);
    display: flex;
    justify-content: center;
    align-items: center;
    z-index: 9999;
}
.spinner {
    width: 50px;
    height: 50px;
    border: 4px solid var(--border);
    border-top-color: var(--primary);
    border-radius: 50%;
    animation: spin 1s linear infinite;
}
@keyframes spin {
    to { transform: rotate(360deg); }
}
`;

// Add spinner styles if not already present
if (!document.querySelector('#spinner-styles')) {
    const style = document.createElement('style');
    style.id = 'spinner-styles';
    style.textContent = spinnerStyles;
    document.head.appendChild(style);
}

// ===== NOTIFICATION SYSTEM =====
const Notification = {
    show: (message, type = 'info', duration = 3000) => {
        const notification = document.createElement('div');
        notification.className = `notification notification-${type}`;
        notification.textContent = message;
        notification.style.cssText = `
            position: fixed;
            top: 20px;
            right: 20px;
            padding: 12px 20px;
            background: ${type === 'success' ? '#4CAF50' : type === 'error' ? '#f44336' : '#2196F3'};
            color: white;
            border-radius: 8px;
            z-index: 10000;
            animation: slideIn 0.3s ease;
            box-shadow: 0 4px 12px rgba(0,0,0,0.15);
        `;
        
        document.body.appendChild(notification);
        
        setTimeout(() => {
            notification.style.animation = 'slideOut 0.3s ease';
            setTimeout(() => notification.remove(), 300);
        }, duration);
    }
};

// Add notification animations
const notificationStyles = `
@keyframes slideIn {
    from { transform: translateX(100%); opacity: 0; }
    to { transform: translateX(0); opacity: 1; }
}
@keyframes slideOut {
    from { transform: translateX(0); opacity: 1; }
    to { transform: translateX(100%); opacity: 0; }
}
`;

if (!document.querySelector('#notification-styles')) {
    const style = document.createElement('style');
    style.id = 'notification-styles';
    style.textContent = notificationStyles;
    document.head.appendChild(style);
}

// ===== EXPORT FUNCTIONS FOR GLOBAL USE =====
window.BrightMinds = {
    Storage,
    UserProgress,
    ThemeManager,
    FormValidator,
    LoadingSpinner,
    Notification,
    animateScore,
    updateProgressBar,
    switchTab
};

// ===== RESPONSIVE TABLE HANDLER =====
function makeTablesResponsive() {
    const tables = document.querySelectorAll('table');
    tables.forEach(table => {
        if (!table.parentElement.classList.contains('table-responsive')) {
            const wrapper = document.createElement('div');
            wrapper.className = 'table-responsive';
            wrapper.style.overflowX = 'auto';
            table.parentNode.insertBefore(wrapper, table);
            wrapper.appendChild(table);
        }
    });
}

// Run on load
document.addEventListener('DOMContentLoaded', () => {
    makeTablesResponsive();
});

// ===== CONSOLE WELCOME MESSAGE =====
console.log('%c🧠 Bright Minds - AI-Powered Learning Platform', 'color: #6C63FF; font-size: 16px; font-weight: bold;');
console.log('%cTogether, we illuminate the path to learning for every child.', 'color: #FF6B6B; font-size: 12px;');