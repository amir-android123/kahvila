// ===== LANGUAGE SWITCHING =====
let currentLanguage = localStorage.getItem('language') || 'fi';

const translations = {
    fi: {
        cartEmpty: 'Ostoskorisi on tyhjä',
        addedToCart: 'lisätty koriin!',
        total: 'Yhteensä:'
    },
    en: {
        cartEmpty: 'Your cart is empty',
        addedToCart: 'added to cart!',
        total: 'Total:'
    },
    sv: {
        cartEmpty: 'Din kundvagn är tom',
        addedToCart: 'tillagd i kundvagnen!',
        total: 'Totalt:'
    },
    ar: {
        cartEmpty: 'سلة التسوق فارغة',
        addedToCart: 'تمت الإضافة إلى السلة!',
        total: 'المجموع:'
    },
    fa: {
        cartEmpty: 'سبد خرید شما خالی است',
        addedToCart: 'به سبد اضافه شد!',
        total: 'جمع:'
    }
};

function setLanguage(lang) {
    currentLanguage = lang;
    localStorage.setItem('language', lang);
    
    // Update HTML lang attribute
    document.documentElement.lang = lang;
    
    // Handle RTL for Arabic and Persian
    if (lang === 'ar' || lang === 'fa') {
        document.documentElement.dir = 'rtl';
        document.body.classList.add('rtl');
    } else {
        document.documentElement.dir = 'ltr';
        document.body.classList.remove('rtl');
    }
    
    // Update language button active states
    document.querySelectorAll('.lang-btn').forEach(btn => {
        btn.classList.remove('active');
        if (btn.dataset.lang === lang) {
            btn.classList.add('active');
        }
    });
    
    // Update all elements with data-lang attributes
    document.querySelectorAll('[data-lang-fi], [data-lang-en], [data-lang-sv], [data-lang-ar], [data-lang-fa]').forEach(el => {
        const text = el.getAttribute(`data-lang-${lang}`);
        if (text) {
            el.innerHTML = text;
        }
    });
    
    // Update page title
    if (lang === 'fi') {
        document.title = 'Kahvila Bon Bon - Aito italialainen kahvila Helsingissä';
    } else if (lang === 'sv') {
        document.title = 'Kahvila Bon Bon - Autentiskt italienskt café i Helsingfors';
    } else if (lang === 'ar') {
        document.title = 'مقهى بون بون - مقهى إيطالي أصيل في هلسنكي';
    } else if (lang === 'fa') {
        document.title = 'کافه بن بن - کافه ایتالیایی اصیل در هلسینکی';
    } else {
        document.title = 'Kahvila Bon Bon - Authentic Italian Café in Helsinki';
    }
    
    // Update cart UI with current language
    updateCartUI();
}

function initLanguage() {
    setLanguage(currentLanguage);
}

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
    
    // Get translation
    const t = translations[currentLanguage];
    
    // Update items
    if (cart.length === 0) {
        cartItems.innerHTML = `
            <div class="empty-cart">
                <i class="fas fa-shopping-basket"></i>
                <p>${t.cartEmpty}</p>
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
    const t = translations[currentLanguage];
    
    // Add translation suffix for cart message
    const displayMessage = message.includes('added to cart') 
        ? message.replace('added to cart!', t.addedToCart)
        : message + ' ' + t.addedToCart;
    
    toastMessage.textContent = displayMessage;
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


// Close cart on escape key
document.addEventListener('keydown', (e) => {
    if (e.key === 'Escape') {
        closeCart();
    }
});

// ===== BUSINESS FORM FUNCTIONALITY =====

// Handle business form submission
function handleBusinessFormSubmit(event) {
    event.preventDefault();
    
    const form = event.target;
    const formData = new FormData(form);
    
    // Build email body
    const businessName = formData.get('businessName');
    const contactName = formData.get('contactName');
    const contactEmail = formData.get('contactEmail');
    const contactPhone = formData.get('contactPhone') || 'Not provided';
    const message = formData.get('message');
    
    // Create email content
    const subject = encodeURIComponent(`B2B Inquiry from ${businessName}`);
    const body = encodeURIComponent(
`BUSINESS INQUIRY

Company: ${businessName}
Contact Person: ${contactName}
Email: ${contactEmail}
Phone: ${contactPhone}

Message:
${message}

---
Sent via Bon Bon Business Contact Form`
    );
    
    // Open email client
    window.location.href = `mailto:info@bonboncoffee.shop?subject=${subject}&body=${body}`;
    
    // Show success message
    showBusinessFormSuccess();
}

// Show success message after form submission
function showBusinessFormSuccess() {
    const successMessages = {
        fi: 'Kiitos yhteydenotosta! Sähköpostiohjelmasi avautuu.',
        en: 'Thank you! Your email client is opening.',
        sv: 'Tack! Din e-postklient öppnas.',
        ar: 'شكرًا! يتم فتح برنامج البريد الإلكتروني.',
        fa: 'متشکریم! کلاینت ایمیل باز می‌شود.'
    };
    
    const message = successMessages[currentLanguage] || successMessages['en'];
    showToast(message);
}

// Update DOMContentLoaded to include business form initialization
document.addEventListener('DOMContentLoaded', () => {
    createParticles();
    initScrollAnimations();
    initNavbarScroll();
    initSmoothScroll();
    updateCartUI();
    loadProductsFromJSON();
    initLanguage();
});
