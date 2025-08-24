// Main JavaScript for AI Roleplay Trainer

// Global utilities
window.RoleplayTrainer = {
    // Show notification
    showNotification: function(message, type = 'info') {
        const notification = document.createElement('div');
        notification.className = `fixed top-4 right-4 z-50 p-4 rounded-lg shadow-lg max-w-sm transform transition-all duration-300 translate-x-full opacity-0`;
        
        const typeClasses = {
            'success': 'bg-green-500 text-white',
            'error': 'bg-red-500 text-white',
            'warning': 'bg-yellow-500 text-white',
            'info': 'bg-blue-500 text-white'
        };
        
        notification.className += ` ${typeClasses[type] || typeClasses.info}`;
        notification.innerHTML = `
            <div class="flex items-center justify-between">
                <span>${message}</span>
                <button onclick="this.parentElement.parentElement.remove()" class="ml-2 text-white hover:text-gray-200">
                    <i class="fas fa-times"></i>
                </button>
            </div>
        `;
        
        document.body.appendChild(notification);
        
        // Animate in
        setTimeout(() => {
            notification.classList.remove('translate-x-full', 'opacity-0');
        }, 100);
        
        // Auto remove after 5 seconds
        setTimeout(() => {
            notification.classList.add('translate-x-full', 'opacity-0');
            setTimeout(() => notification.remove(), 300);
        }, 5000);
    },
    
    // Format timestamp
    formatTime: function(timestamp) {
        const date = new Date(timestamp);
        return date.toLocaleTimeString('en-US', {
            hour: '2-digit',
            minute: '2-digit',
            hour12: false
        });
    },
    
    // Format duration
    formatDuration: function(seconds) {
        const minutes = Math.floor(seconds / 60);
        const remainingSeconds = seconds % 60;
        return `${minutes}:${remainingSeconds.toString().padStart(2, '0')}`;
    },
    
    // Debounce function
    debounce: function(func, wait) {
        let timeout;
        return function executedFunction(...args) {
            const later = () => {
                clearTimeout(timeout);
                func(...args);
            };
            clearTimeout(timeout);
            timeout = setTimeout(later, wait);
        };
    },
    
    // Smooth scroll to element
    scrollTo: function(element, offset = 0) {
        const elementPosition = element.offsetTop;
        const offsetPosition = elementPosition - offset;
        
        window.scrollTo({
            top: offsetPosition,
            behavior: 'smooth'
        });
    },
    
    // Copy text to clipboard
    copyToClipboard: function(text) {
        if (navigator.clipboard && window.isSecureContext) {
            return navigator.clipboard.writeText(text).then(() => {
                this.showNotification('Copied to clipboard!', 'success');
            }).catch(() => {
                this.showNotification('Failed to copy text', 'error');
            });
        } else {
            // Fallback for older browsers
            const textArea = document.createElement('textarea');
            textArea.value = text;
            textArea.style.position = 'fixed';
            textArea.style.left = '-999999px';
            textArea.style.top = '-999999px';
            document.body.appendChild(textArea);
            textArea.focus();
            textArea.select();
            
            try {
                document.execCommand('copy');
                this.showNotification('Copied to clipboard!', 'success');
            } catch (err) {
                this.showNotification('Failed to copy text', 'error');
            } finally {
                textArea.remove();
            }
        }
    },
    
    // Local storage helpers
    storage: {
        set: function(key, value) {
            try {
                localStorage.setItem(key, JSON.stringify(value));
                return true;
            } catch (e) {
                console.error('Failed to save to localStorage:', e);
                return false;
            }
        },
        
        get: function(key, defaultValue = null) {
            try {
                const item = localStorage.getItem(key);
                return item ? JSON.parse(item) : defaultValue;
            } catch (e) {
                console.error('Failed to read from localStorage:', e);
                return defaultValue;
            }
        },
        
        remove: function(key) {
            try {
                localStorage.removeItem(key);
                return true;
            } catch (e) {
                console.error('Failed to remove from localStorage:', e);
                return false;
            }
        }
    }
};

// Initialize app when DOM is loaded
document.addEventListener('DOMContentLoaded', function() {
    // Add click handlers for copy buttons
    document.querySelectorAll('[data-copy]').forEach(button => {
        button.addEventListener('click', function() {
            const text = this.getAttribute('data-copy');
            window.RoleplayTrainer.copyToClipboard(text);
        });
    });
    
    // Add smooth scrolling to anchor links
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function(e) {
            e.preventDefault();
            const target = document.querySelector(this.getAttribute('href'));
            if (target) {
                window.RoleplayTrainer.scrollTo(target, 100);
            }
        });
    });
    
    // Handle form submissions with loading states
    document.querySelectorAll('form').forEach(form => {
        form.addEventListener('submit', function(e) {
            const submitButton = this.querySelector('button[type="submit"]');
            if (submitButton && !submitButton.disabled) {
                const originalContent = submitButton.innerHTML;
                submitButton.disabled = true;
                submitButton.innerHTML = '<i class="fas fa-spinner fa-spin mr-2"></i>Loading...';
                
                // Re-enable after 10 seconds as fallback
                setTimeout(() => {
                    submitButton.disabled = false;
                    submitButton.innerHTML = originalContent;
                }, 10000);
            }
        });
    });
    
    // Auto-resize textareas
    document.querySelectorAll('textarea[data-auto-resize]').forEach(textarea => {
        function resize() {
            textarea.style.height = 'auto';
            textarea.style.height = textarea.scrollHeight + 'px';
        }
        
        textarea.addEventListener('input', resize);
        resize(); // Initial resize
    });
    
    // Handle modal close on backdrop click
    document.querySelectorAll('.modal-backdrop').forEach(backdrop => {
        backdrop.addEventListener('click', function(e) {
            if (e.target === this) {
                this.classList.add('hidden');
                this.classList.remove('flex');
            }
        });
    });
    
    // Handle escape key for modals
    document.addEventListener('keydown', function(e) {
        if (e.key === 'Escape') {
            const openModal = document.querySelector('.modal-backdrop.flex');
            if (openModal) {
                openModal.classList.add('hidden');
                openModal.classList.remove('flex');
            }
        }
    });
    
    // Add tooltips (simple implementation)
    document.querySelectorAll('[data-tooltip]').forEach(element => {
        element.addEventListener('mouseenter', function() {
            const tooltip = document.createElement('div');
            tooltip.className = 'absolute z-50 px-2 py-1 text-sm text-white bg-gray-800 rounded shadow-lg pointer-events-none';
            tooltip.textContent = this.getAttribute('data-tooltip');
            tooltip.style.top = this.offsetTop - 35 + 'px';
            tooltip.style.left = this.offsetLeft + (this.offsetWidth / 2) - (tooltip.offsetWidth / 2) + 'px';
            document.body.appendChild(tooltip);
            this._tooltip = tooltip;
        });
        
        element.addEventListener('mouseleave', function() {
            if (this._tooltip) {
                this._tooltip.remove();
                delete this._tooltip;
            }
        });
    });
    
    // Performance: Lazy load images
    if ('IntersectionObserver' in window) {
        const imageObserver = new IntersectionObserver((entries, observer) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    const img = entry.target;
                    img.src = img.dataset.src;
                    img.classList.remove('lazy');
                    observer.unobserve(img);
                }
            });
        });
        
        document.querySelectorAll('img[data-src]').forEach(img => {
            imageObserver.observe(img);
        });
    }
    
    // Add loading states to buttons on click
    document.querySelectorAll('button[data-loading]').forEach(button => {
        button.addEventListener('click', function() {
            if (!this.disabled) {
                const originalText = this.textContent;
                this.disabled = true;
                this.innerHTML = '<i class="fas fa-spinner fa-spin mr-2"></i>Loading...';
                
                // Reset after 5 seconds as fallback
                setTimeout(() => {
                    this.disabled = false;
                    this.textContent = originalText;
                }, 5000);
            }
        });
    });
});

// Handle page visibility changes
document.addEventListener('visibilitychange', function() {
    if (document.hidden) {
        // Page is hidden - pause any timers or animations
        console.log('Page hidden');
    } else {
        // Page is visible - resume activities
        console.log('Page visible');
    }
});

// Error handling
window.addEventListener('error', function(e) {
    console.error('JavaScript error:', e.error);
    // You could send error reports to your analytics here
});

// Performance monitoring
window.addEventListener('load', function() {
    // Log performance metrics if needed
    if (window.performance && window.performance.timing) {
        const timing = window.performance.timing;
        const loadTime = timing.loadEventEnd - timing.navigationStart;
        console.log('Page load time:', loadTime + 'ms');
    }
});