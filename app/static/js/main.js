// Enhanced main JavaScript file
class NexaStore {
    constructor() {
        this.init();
    }

    init() {
        this.setupEventListeners();
        this.setupAnimations();
        this.setupCart();
    }

    setupEventListeners() {
        // Mobile menu
        const mobileMenuButton = document.getElementById('mobileMenuButton');
        const mobileMenu = document.getElementById('mobileMenu');
        
        if (mobileMenuButton && mobileMenu) {
            mobileMenuButton.addEventListener('click', () => {
                mobileMenu.classList.toggle('hidden');
            });
        }

        // Close mobile menu when clicking outside
        document.addEventListener('click', (e) => {
            if (!e.target.closest('#mobileMenu') && !e.target.closest('#mobileMenuButton')) {
                mobileMenu.classList.add('hidden');
            }
        });

        // Smooth scrolling for anchor links
        document.querySelectorAll('a[href^="#"]').forEach(anchor => {
            anchor.addEventListener('click', function (e) {
                e.preventDefault();
                const target = document.querySelector(this.getAttribute('href'));
                if (target) {
                    target.scrollIntoView({
                        behavior: 'smooth',
                        block: 'start'
                    });
                }
            });
        });
    }

    setupAnimations() {
        // Intersection Observer for scroll animations
        const observerOptions = {
            threshold: 0.1,
            rootMargin: '0px 0px -50px 0px'
        };

        const observer = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    entry.target.classList.add('animate-fade-in');
                }
            });
        }, observerOptions);

        // Observe elements with animation classes
        document.querySelectorAll('.card-hover, .animate-on-scroll').forEach(el => {
            observer.observe(el);
        });
    }

    setupCart() {
        // Cart functionality will be enhanced here
    }

    async addToCart(productId, quantity = 1) {
        try {
            const formData = new URLSearchParams();
            formData.append('product_id', productId);
            formData.append('quantity', quantity);

            const response = await fetch('/add-to-cart', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/x-www-form-urlencoded',
                },
                body: formData
            });

            const data = await response.json();

            if (data.success) {
                this.showNotification(data.message, 'success');
                this.updateCartCount(data.cart_count);
                return true;
            } else {
                this.showNotification(data.message, 'error');
                return false;
            }
        } catch (error) {
            this.showNotification('Network error. Please try again.', 'error');
            return false;
        }
    }

    showNotification(message, type = 'info') {
        const toast = document.getElementById('toast');
        const toastMessage = document.getElementById('toastMessage');
        const toastIcon = document.getElementById('toastIcon');

        if (!toast || !toastMessage || !toastIcon) return;

        // Set message and style
        toastMessage.textContent = message;

        const styles = {
            success: {
                bg: 'bg-green-500',
                icon: 'fa-check'
            },
            error: {
                bg: 'bg-red-500',
                icon: 'fa-exclamation'
            },
            info: {
                bg: 'bg-blue-500',
                icon: 'fa-info'
            }
        };

        const style = styles[type] || styles.info;
        toastIcon.className = `w-6 h-6 ${style.bg} rounded-full flex items-center justify-center`;
        toastIcon.innerHTML = `<i class="fas ${style.icon} text-white text-xs"></i>`;

        // Show toast
        toast.classList.remove('translate-x-full', 'opacity-0');
        toast.classList.add('opacity-100');

        // Hide after delay
        setTimeout(() => {
            toast.classList.add('translate-x-full', 'opacity-0');
            toast.classList.remove('opacity-100');
        }, 3000);
    }

    updateCartCount(count) {
        // Update all cart count elements
        document.querySelectorAll('.fa-shopping-bag').forEach(icon => {
            const parent = icon.parentElement;
            let badge = parent.querySelector('.absolute');

            if (count > 0) {
                if (!badge) {
                    badge = document.createElement('span');
                    badge.className = 'absolute -top-1 -right-1 bg-secondary-500 text-white rounded-full w-5 h-5 text-xs flex items-center justify-center font-medium';
                    parent.appendChild(badge);
                }
                badge.textContent = count;
                badge.classList.add('animate-pulse');
                setTimeout(() => badge.classList.remove('animate-pulse'), 1000);
            } else if (badge) {
                badge.remove();
            }
        });
    }

    // Price range filter with debounce
    debounce(func, wait) {
        let timeout;
        return function executedFunction(...args) {
            const later = () => {
                clearTimeout(timeout);
                func(...args);
            };
            clearTimeout(timeout);
            timeout = setTimeout(later, wait);
        };
    }
}

// Initialize when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    window.necaStore = new NexaStore();
});

// Global addToCart function for HTML onclick attributes
window.addToCart = async function(productId, quantity = 1) {
    if (window.necaStore) {
        return await window.necaStore.addToCart(productId, quantity);
    }
    return false;
};