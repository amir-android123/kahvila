// ===== CART FUNCTIONALITY =====
let cart = [];

function addToCart(name, price) {
    const existingItem = cart.find(item => item.name === name);
    
    if (existingItem) {
        existingItem.quantity++;
    } else {
        cart.push({ name, price, quantity: 1 });
    }
    
    updateCartUI();
    showToast(`${name} added to cart!`);
}

function removeFromCart(index) {
    cart.splice(index, 1);
    updateCartUI();
}

function updateQuantity(index, change) {
    cart[index].quantity += change;
    if (cart[index].quantity <= 0) {
        removeFromCart(index);
    } else {
        updateCartUI();
    }
}

function updateCartUI() {
    const cartCount = document.getElementById('cartCount');
    const cartItems = document.getElementById('cartItems');
    const cartTotal = document.getElementById('cartTotal');
    
    // Update count
    const totalItems = cart.reduce((sum, item) => sum + item.quantity, 0);
    cartCount.textContent = totalItems;
    
    // Update items
    if (cart.length === 0) {
        cartItems.innerHTML = `
            <div class="empty-cart">
                <i class="fas fa-shopping-basket"></i>
                <p>Your cart is empty</p>
            </div>
        `;
    } else {
        cartItems.innerHTML = cart.map((item, index) => `
            <div class="cart-item">
                <div class="cart-item-info">
                    <div class="cart-item-name">${item.name}</div>
                    <div class="cart-item-price">€${item.price.toFixed(2)}</div>
                    <div class="cart-item-quantity">
                        <button onclick="updateQuantity(${index}, -1)">
                            <i class="fas fa-minus"></i>
                        </button>
                        <span>${item.quantity}</span>
                        <button onclick="updateQuantity(${index}, 1)">
                            <i class="fas fa-plus"></i>
                        </button>
                    </div>
                </div>
            </div>
        `).join('');
    }
    
    // Update total
    const total = cart.reduce((sum, item) => sum + (item.price * item.quantity), 0);
    cartTotal.textContent = `€${total.toFixed(2)}`;
}

// ===== CART SIDEBAR =====
function openCart() {
    document.getElementById('cartSidebar').classList.add('active');
    document.getElementById('cartOverlay').classList.add('active');
    document.body.style.overflow = 'hidden';
}

function closeCart() {
    document.getElementById('cartSidebar').classList.remove('active');
    document.getElementById('cartOverlay').classList.remove('active');
    document.body.style.overflow = '';
}

// ===== TOAST NOTIFICATION =====
function showToast(message) {
    const toast = document.getElementById('toast');
    const toastMessage = document.getElementById('toastMessage');
    
    toastMessage.textContent = message;
    toast.classList.add('active');
    
    setTimeout(() => {
        toast.classList.remove('active');
    }, 3000);
}

// ===== PARTICLES =====
function createParticles() {
    const container = document.getElementById('particles');
    const particleCount = 30;
    
    for (let i = 0; i < particleCount; i++) {
        const particle = document.createElement('div');
        particle.className = 'particle';
        particle.style.left = Math.random() * 100 + '%';
        particle.style.animationDelay = Math.random() * 15 + 's';
        particle.style.animationDuration = (15 + Math.random() * 10) + 's';
        container.appendChild(particle);
    }
}

// ===== SCROLL ANIMATIONS =====
function initScrollAnimations() {
    const elements = document.querySelectorAll('[data-aos]');
    
    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.style.opacity = '1';
                entry.target.style.transform = 'translateY(0)';
            }
        });
    }, { threshold: 0.1 });
    
    elements.forEach(el => {
        el.style.opacity = '0';
        el.style.transform = 'translateY(30px)';
        el.style.transition = 'opacity 0.6s ease, transform 0.6s ease';
        observer.observe(el);
    });
}

// ===== NAVBAR SCROLL EFFECT =====
function initNavbarScroll() {
    const navbar = document.querySelector('.navbar');
    
    window.addEventListener('scroll', () => {
        if (window.scrollY > 50) {
            navbar.style.padding = '0.75rem 0';
            navbar.style.background = 'rgba(13, 11, 9, 0.98)';
        } else {
            navbar.style.padding = '1rem 0';
            navbar.style.background = 'rgba(13, 11, 9, 0.95)';
        }
    });
}

// ===== SMOOTH SCROLL FOR NAV LINKS =====
function initSmoothScroll() {
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function(e) {
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

// ===== LOAD PRODUCTS FROM JSON =====
async function loadProductsFromJSON() {
    try {
        const response = await fetch('products.json');
        if (!response.ok) {
            console.log('No products.json found, using default products');
            return;
        }
        
        const products = await response.json();
        if (products.length > 0) {
            updateProductDisplay(products);
        }
    } catch (error) {
        console.log('Error loading products:', error);
    }
}

function updateProductDisplay(products) {
    const productsSection = document.getElementById('products');
    if (!productsSection) return;
    
    const productGrid = productsSection.querySelector('.product-grid');
    if (!productGrid) return;
    
    // Clear existing products
    productGrid.innerHTML = '';
    
    // Add new products
    products.forEach(product => {
        const productCard = document.createElement('div');
        productCard.className = 'product-card';
        productCard.innerHTML = `
            <div class="product-image">
                <img src="${product.image_url}" alt="${product.name}" loading="lazy">
            </div>
            <div class="product-info">
                <h3 class="product-name">${product.name}</h3>
                <div class="product-footer">
                    <span class="product-price">€${product.price.toFixed(2)}</span>
                    <button class="btn-primary" onclick="addToCart('${product.name.replace(/'/g, "\\'")}', ${product.price})">
                        <i class="fas fa-shopping-cart"></i> Add to Cart
                    </button>
                </div>
            </div>
        `;
        productGrid.appendChild(productCard);
    });
    
    // Reinitialize scroll animations for new elements
    initScrollAnimations();
}

// ===== INITIALIZE =====
document.addEventListener('DOMContentLoaded', () => {
    createParticles();
    initScrollAnimations();
    initNavbarScroll();
    initSmoothScroll();
    updateCartUI();
    loadProductsFromJSON();
});

// Close cart on escape key
document.addEventListener('keydown', (e) => {
    if (e.key === 'Escape') {
        closeCart();
    }
});
