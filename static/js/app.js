// Корзина
let cart = JSON.parse(localStorage.getItem('lada_cart')) || [];

function saveCart() {
    localStorage.setItem('lada_cart', JSON.stringify(cart));
    updateCartUI();
}

function updateCartUI() {
    const count = cart.reduce((sum, item) => sum + item.quantity, 0);
    document.getElementById('cart-count').textContent = count;

    const cartItems = document.getElementById('cart-items');
    const totalPriceEl = document.getElementById('cart-total-price');

    if (cart.length === 0) {
        cartItems.innerHTML = `
            <div class="cart-empty">
                <i class="fas fa-shopping-cart"></i>
                <p>Корзина пуста</p>
                <span>Добавьте запчасти из каталога</span>
            </div>
        `;
        totalPriceEl.textContent = '0 ₽';
        return;
    }

    let total = 0;
    cartItems.innerHTML = cart.map(item => {
        total += item.price * item.quantity;
        return `
            <div class="cart-item">
                <div class="cart-item-image"><i class="fas fa-cog"></i></div>
                <div class="cart-item-info">
                    <div class="cart-item-name">${item.name}</div>
                    <div class="cart-item-meta">${item.model} | Арт: ${item.article}</div>
                    <div class="cart-item-price">${item.price.toLocaleString('ru-RU')} ₽</div>
                    <div class="cart-item-actions">
                        <button class="qty-btn" onclick="changeQty('${item.id}', -1)">−</button>
                        <span class="qty-value">${item.quantity}</span>
                        <button class="qty-btn" onclick="changeQty('${item.id}', 1)">+</button>
                        <button class="remove-item" onclick="removeFromCart('${item.id}')">
                            <i class="fas fa-trash"></i> Удалить
                        </button>
                    </div>
                </div>
            </div>
        `;
    }).join('');

    totalPriceEl.textContent = total.toLocaleString('ru-RU') + ' ₽';
}

function addToCart(id, name, price, article, model) {
    const existing = cart.find(item => item.id === id);
    if (existing) {
        existing.quantity++;
    } else {
        cart.push({ id, name, price, article, model, quantity: 1 });
    }
    saveCart();

    // Анимация
    const btn = event.target.closest('.add-to-cart-btn');
    const originalText = btn.innerHTML;
    btn.innerHTML = '<i class="fas fa-check"></i> Добавлено';
    btn.style.background = '#28a745';
    setTimeout(() => {
        btn.innerHTML = originalText;
        btn.style.background = '';
    }, 1500);
}

function changeQty(id, delta) {
    const item = cart.find(i => i.id === id);
    if (!item) return;
    item.quantity += delta;
    if (item.quantity <= 0) {
        cart = cart.filter(i => i.id !== id);
    }
    saveCart();
}

function removeFromCart(id) {
    cart = cart.filter(i => i.id !== id);
    saveCart();
}

function toggleCart() {
    document.getElementById('cart-sidebar').classList.toggle('active');
    document.getElementById('cart-overlay').classList.toggle('active');
}

function checkout() {
    if (cart.length === 0) {
        alert('Корзина пуста!');
        return;
    }
    const total = cart.reduce((sum, item) => sum + item.price * item.quantity, 0);
    alert(`Заказ оформлен!\nСумма: ${total.toLocaleString('ru-RU')} ₽\n\n(В реальном приложении здесь будет форма оформления)`);
    cart = [];
    saveCart();
    toggleCart();
}

// Фильтры и сортировка
function initCatalogFilters() {
    const partsGrid = document.getElementById('parts-grid');
    if (!partsGrid) return;

    const cards = Array.from(partsGrid.querySelectorAll('.part-card'));
    const searchInput = document.getElementById('catalog-search');
    const sortSelect = document.getElementById('sort-select');
    const priceMin = document.getElementById('price-min');
    const priceMax = document.getElementById('price-max');
    const noResults = document.getElementById('no-results');

    function filterAndSort() {
        const searchTerm = searchInput.value.toLowerCase();
        const sortValue = sortSelect.value;
        const minPrice = parseInt(priceMin.value) || 0;
        const maxPrice = parseInt(priceMax.value) || Infinity;
        const selectedCategory = document.querySelector('input[name="category"]:checked')?.value || 'all';
        const selectedStock = document.querySelector('input[name="stock"]:checked')?.value || 'all';

        let visible = [];

        cards.forEach(card => {
            const name = card.dataset.name.toLowerCase();
            const article = card.dataset.article.toLowerCase();
            const price = parseInt(card.dataset.price);
            const category = card.dataset.category;
            const stock = card.dataset.stock;

            const matchesSearch = name.includes(searchTerm) || article.includes(searchTerm);
            const matchesCategory = selectedCategory === 'all' || category === selectedCategory;
            const matchesStock = selectedStock === 'all' || stock === selectedStock;
            const matchesPrice = price >= minPrice && price <= maxPrice;

            if (matchesSearch && matchesCategory && matchesStock && matchesPrice) {
                visible.push(card);
                card.style.display = '';
            } else {
                card.style.display = 'none';
            }
        });

        // Сортировка
        visible.sort((a, b) => {
            if (sortValue === 'name') {
                return a.dataset.name.localeCompare(b.dataset.name);
            } else if (sortValue === 'price_asc') {
                return parseInt(a.dataset.price) - parseInt(b.dataset.price);
            } else if (sortValue === 'price_desc') {
                return parseInt(b.dataset.price) - parseInt(a.dataset.price);
            }
            return 0;
        });

        visible.forEach(card => partsGrid.appendChild(card));

        noResults.style.display = visible.length === 0 ? 'block' : 'none';
    }

    searchInput?.addEventListener('input', filterAndSort);
    sortSelect?.addEventListener('change', filterAndSort);
    priceMin?.addEventListener('input', filterAndSort);
    priceMax?.addEventListener('input', filterAndSort);

    document.querySelectorAll('input[name="category"]').forEach(radio => {
        radio.addEventListener('change', function() {
            document.querySelectorAll('#category-filters .filter-option').forEach(opt => opt.classList.remove('active'));
            this.closest('.filter-option').classList.add('active');
            filterAndSort();
        });
    });

    document.querySelectorAll('input[name="stock"]').forEach(radio => {
        radio.addEventListener('change', function() {
            this.closest('.filter-options').querySelectorAll('.filter-option').forEach(opt => opt.classList.remove('active'));
            this.closest('.filter-option').classList.add('active');
            filterAndSort();
        });
    });
}

// Глобальный поиск
function initGlobalSearch() {
    const searchInput = document.getElementById('global-search');
    const searchResults = document.getElementById('search-results');
    let debounceTimer;

    if (!searchInput) return;

    searchInput.addEventListener('input', function() {
        clearTimeout(debounceTimer);
        const query = this.value.trim();

        if (query.length < 2) {
            searchResults.classList.remove('active');
            return;
        }

        debounceTimer = setTimeout(() => {
            fetch(`/api/search?q=${encodeURIComponent(query)}`)
                .then(r => r.json())
                .then(data => {
                    if (data.length === 0) {
                        searchResults.innerHTML = '<div class="search-result-item">Ничего не найдено</div>';
                    } else {
                        searchResults.innerHTML = data.slice(0, 8).map(item => `
                            <a href="/model/${item.model_id}" class="search-result-item">
                                <div class="result-name">${item.name}</div>
                                <div class="result-meta">${item.model_name} | ${item.category} | Арт: ${item.article}</div>
                                <div class="result-price">${item.price.toLocaleString('ru-RU')} ₽</div>
                            </a>
                        `).join('');
                    }
                    searchResults.classList.add('active');
                });
        }, 300);
    });

    document.addEventListener('click', function(e) {
        if (!e.target.closest('.search-box')) {
            searchResults.classList.remove('active');
        }
    });
}

// Инициализация
document.addEventListener('DOMContentLoaded', function() {
    updateCartUI();
    initCatalogFilters();
    initGlobalSearch();
});


