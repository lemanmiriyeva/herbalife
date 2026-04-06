$(document).ready(function () {

    var owl = $('.owl-carousel1');

    owl.owlCarousel({
        items: 1,
        loop: true,
        margin: 0,
        autoplay: true,
        autoplayTimeout: 3000,
        dots: true,
        nav: true,
        autoplayHoverPause: true
    });

});


$('.tabs-carousel').owlCarousel({
    items: 4,
    margin: 20,
    dots: false,
    nav: true,
    navText: [
        '<span class="me-2 fa fa-chevron-left"></span>',
        '<span class="ms-2 fa fa-chevron-right"></span>'
    ],
    responsive: {
        0: { items: 1 },
        600: { items: 3 },
        1000: { items: 4 }
    }
});

$('.tab-item').on('click', function () {

    var target = $(this).data('target');

    // button active
    $('.tab-item').removeClass('active');
    $(this).addClass('active');

    // content dəyiş
    $('.tab-pane').removeClass('show active');
    $(target).addClass('show active');

});
$(document).ready(function () {
    $(".owl-carousel3").owlCarousel({
        items: 1,
        loop: true,
        margin: 10,
        nav: true,
        dots: true,
        navText: ['<span>‹</span>', '<span>›</span>'],
        autoplay: false,
        autoplayTimeout: 5000,
        smartSpeed: 700
    });
});


$(document).ready(function () {
    $('.testimonial-carousel').owlCarousel({
        loop: true,
        margin: 20,
        nav: true,
        dots: true,
        autoplay: true,
        autoplayTimeout: 5000,
        autoplayHoverPause: true,
        navText: ['<span>‹</span>', '<span>›</span>'],
        responsive: {
            0: {
                items: 1
            },
            768: {
                items: 2
            },
            1024: {
                items: 3
            }
        }
    });
});

$(document).ready(function () {
    $('.articles-carousel').owlCarousel({
        loop: true,
        margin: 20,
        nav: true,
        dots: true,
        autoplay: true,
        autoplayTimeout: 5000,
        autoplayHoverPause: true,
        navText: ['<span>‹</span>', '<span>›</span>'],
        responsive: {
            0: {
                items: 1
            },
            768: {
                items: 2
            },
            1024: {
                items: 3
            }
        }
    });
});
$(document).ready(function () {
    var owl = $('.owl-carousel1');
    owl.owlCarousel({
        items: 1, loop: true, margin: 0, autoplay: true,
        autoplayTimeout: 3000, dots: true, nav: true, autoplayHoverPause: true
    });
});

$('.tabs-carousel').owlCarousel({
    items: 4, margin: 20, dots: false, nav: true,
    navText: ['<span class="me-2 fa fa-chevron-left"></span>', '<span class="ms-2 fa fa-chevron-right"></span>'],
    responsive: { 0: { items: 1 }, 600: { items: 3 }, 1000: { items: 4 } }
});

$('.tab-item').on('click', function () {
    var target = $(this).data('target');
    $('.tab-item').removeClass('active');
    $(this).addClass('active');
    $('.tab-pane').removeClass('show active');
    $(target).addClass('show active');
});

$(document).ready(function () {
    $(".owl-carousel3").owlCarousel({
        items: 1, loop: true, margin: 10, nav: true, dots: true,
        navText: ['<span>‹</span>', '<span>›</span>'], smartSpeed: 700
    });
    $('.testimonial-carousel').owlCarousel({
        loop: true, margin: 20, nav: true, dots: true, autoplay: true,
        autoplayTimeout: 5000, autoplayHoverPause: true,
        navText: ['<span>‹</span>', '<span>›</span>'],
        responsive: { 0: { items: 1 }, 768: { items: 2 }, 1024: { items: 3 } }
    });
    $('.articles-carousel').owlCarousel({
        loop: true, margin: 20, nav: true, dots: true, autoplay: true,
        autoplayTimeout: 5000, autoplayHoverPause: true,
        navText: ['<span>‹</span>', '<span>›</span>'],
        responsive: { 0: { items: 1 }, 768: { items: 2 }, 1024: { items: 3 } }
    });
});

/* ════════════════════════════════════════════════════════════
   main.js — Herbalife | API-driven frontend
   ════════════════════════════════════════════════════════════ */
'use strict';

const t = key => (window.DJANGO_TRANS && window.DJANGO_TRANS[key]) || key;

/* ── API ─────────────────────────────────────────────────── */
const API = {
    get(url) {
        return fetch(url, { credentials: 'same-origin' }).then(r => r.json());
    },
    post(url, data) {
        return fetch(url, {
            method: 'POST', credentials: 'same-origin',
            headers: { 'Content-Type': 'application/json', 'X-CSRFToken': getCsrf() },
            body: JSON.stringify(data),
        }).then(r => r.json());
    },
    patch(url, data) {
        return fetch(url, {
            method: 'PATCH', credentials: 'same-origin',
            headers: { 'Content-Type': 'application/json', 'X-CSRFToken': getCsrf() },
            body: JSON.stringify(data),
        }).then(r => r.json());
    },
    delete(url) {
        return fetch(url, {
            method: 'POST', credentials: 'same-origin',
            headers: { 'X-CSRFToken': getCsrf() },
        }).then(r => r.json());
    },
};

function getCsrf() {
    const m = document.cookie.match(/csrftoken=([^;]+)/);
    return m ? m[1] : '';
}

/* ── Product card ────────────────────────────────────────── */
function productCard(p, linkPrefix = '/products/') {
    const image = p.image
        ? `<img src="${p.image}" alt="${p.name}" class="product-image">`
        : `<img src="https://www.herbalife.com/dmassets/market-reusable-assets/amer/united-states/images/canister/pc-64z1-us.png:pdp-w875h783?fmt=webp-alpha" alt="${p.name}" class="product-image">`;
    const badge = p.badge ? `<span class="product-badge">${p.badge}</span>` : '';
    const flavor = p.flavor_name ? `<div class="product-flavor">
        ${p.flavor_color ? `<span class="flavor-dot" style="background-color:${p.flavor_color};"></span>` : ''}
        <span class="flavor-name">${p.flavor_name}</span></div>` : '';
    const size = p.size ? `<div class="product-size">${p.size}</div>` : '';
    const priceNote = p.price_note ? `<span class="product-price-small">${p.price_note}</span>` : '';
    const addBtn = p.is_addable
        ? `<button class="add-btn" onclick="cartAdd(${p.id}, event)">${t('add_btn')}</button><button class="wishlist-btn"
           data-wishlist-btn="${p.id}"
           title="Sevimlilərə əlavə et">
     <i class="far fa-heart"></i>
   </button>` : '';
    return `
    <div class="product-card" data-product-id="${p.id}">
        ${badge}
        <a href="${linkPrefix}${p.slug}/">${image}</a>
        <div class="product-info">
            ${flavor}
            <div class="product-name">
                <a href="${linkPrefix}${p.slug}/" style="color:inherit;text-decoration:none;">${p.name}</a>
            </div>
            ${size}
            <div class="product-footer">
                <div class="product-price">$${p.final_price}${priceNote}</div>
                ${addBtn}
            </div>
        </div>
    </div>`;
}

/* ── CART ────────────────────────────────────────────────── */
let cartState = { total_items: 0, total_price: '0.00', items: [] };

function updateCartBadge() {
    document.querySelectorAll('.cart-badge').forEach(el => {
        el.textContent = cartState.total_items;
        el.style.display = cartState.total_items > 0 ? 'flex' : 'none';
    });
}

function loadCart() {
    API.get('/api/cart/').then(data => {
        cartState = data;
        updateCartBadge();
        if (document.getElementById('cartPageRoot')) renderCartPage();
    });
}

function cartAdd(productId, e) {
    if (e) e.preventDefault();
    const qty = parseInt(document.getElementById('detailQty')?.value || '1');
    API.post('/api/cart/add/', { product_id: productId, quantity: qty })
        .then(data => { cartState = data; updateCartBadge(); showToast(t('toast_added')); });
}

function cartUpdate(itemId, quantity) {
    API.patch(`/api/cart/items/${itemId}/`, { quantity })
        .then(data => {
            cartState = data; updateCartBadge();
            if (document.getElementById('cartPageRoot')) renderCartPage();
        });
}

function cartRemove(itemId) {
    API.delete(`/api/cart/items/${itemId}/delete/`)
        .then(data => {
            cartState = data; updateCartBadge();
            if (document.getElementById('cartPageRoot')) renderCartPage();
        });
}

/* ── PRODUCTS PAGE ───────────────────────────────────────── */
function initProductsPage() {
    const grid = document.getElementById('productGrid');
    const countEl = document.getElementById('productCount');
    const catSlider = document.getElementById('categorySliderInner');
    if (!grid) return;

    const urlP = new URLSearchParams(location.search);
    let currentParams = {
        category: urlP.get('category') || '',
        sort: urlP.get('sort') || '',
        search: urlP.get('search') || '',
        flavors: urlP.getAll('flavor'),
        sizes: urlP.getAll('size'),
        prices: urlP.getAll('price'),
    };

    API.get('/api/categories/').then(cats => {
        if (!catSlider) return;
        catSlider.innerHTML =
            `<div class="category-item${!currentParams.category ? ' active' : ''}" data-slug="">
                <span>${t('all_products')}</span>
             </div>` +
            cats.map(c =>
                `<div class="category-item${currentParams.category === c.slug ? ' active' : ''}" data-slug="${c.slug}">
                    <span>${c.name}</span>
                 </div>`
            ).join('');

        if (typeof $ !== 'undefined' && $.fn.owlCarousel) {
            const $slider = $('#categorySliderInner');
            if ($slider.hasClass('owl-loaded')) {
                $slider.trigger('destroy.owl.carousel').removeClass('owl-loaded owl-drag');
                $slider.find('.owl-stage-outer').children().unwrap();
            }
            $slider.owlCarousel({
                loop: false, margin: 20, nav: true, dots: false,
                navText: ['<span class="fa fa-chevron-left"></span>', '<span class="fa fa-chevron-right"></span>'],
                responsive: { 0: { items: 2 }, 600: { items: 3 }, 1000: { items: 4 } },
            });
        }

        catSlider.addEventListener('click', e => {
            const item = e.target.closest('.category-item');
            if (!item) return;
            currentParams.category = item.dataset.slug;
            catSlider.querySelectorAll('.category-item').forEach(i => i.classList.remove('active'));
            item.classList.add('active');
            loadProducts();
        });
    });

    const sortEl = document.getElementById('sortSelect');
    if (sortEl) {
        sortEl.value = currentParams.sort;
        sortEl.addEventListener('change', () => { currentParams.sort = sortEl.value; loadProducts(); });
    }

    function renderFilterSection(containerId, title, items, type) {
        const el = document.getElementById(containerId);
        if (!el) return;
        const prefix = containerId === 'desktopFilterContent' ? 'd' : 'm';
        el.innerHTML += `
        <div class="filter-section">
            <div class="filter-title">${title}<i class="fas fa-chevron-up"></i></div>
            <div id="${prefix}-${type}-list">
                ${items.map((item, i) => `
                <div class="filter-option">
                    <input type="checkbox" id="${prefix}-${type}-${i}"
                           data-type="${type}" data-value="${item}"
                           ${(type === 'flavor' ? currentParams.flavors : currentParams.sizes).includes(item) ? 'checked' : ''}>
                    <label for="${prefix}-${type}-${i}">${item}</label>
                </div>`).join('')}
            </div>
        </div>`;
    }

    function renderPriceSection(containerId) {
        const el = document.getElementById(containerId);
        if (!el) return;
        const prefix = containerId === 'desktopFilterContent' ? 'd' : 'm';
        const prices = [
            { label: '< $25', value: 'lt25' }, { label: '$25 – $50', value: '25-50' },
            { label: '$50 – $100', value: '50-100' }, { label: '> $100', value: 'gt100' },
        ];
        el.innerHTML += `
        <div class="filter-section">
            <div class="filter-title">${t('filter_price')}<i class="fas fa-chevron-up"></i></div>
            ${prices.map((p, i) => `
            <div class="filter-option">
                <input type="checkbox" id="${prefix}-price-${i}"
                       data-type="price" data-value="${p.value}"
                       ${(currentParams.prices || []).includes(p.value) ? 'checked' : ''}>
                <label for="${prefix}-price-${i}">${p.label}</label>
            </div>`).join('')}
        </div>`;
    }

    function loadFilters() {
        API.get('/api/filters/').then(data => {
            ['desktopFilterContent', 'mobileFilterContent'].forEach(id => {
                const el = document.getElementById(id);
                if (!el) return;
                el.innerHTML = '';
                if (data.flavors.length) renderFilterSection(id, t('filter_flavor'), data.flavors, 'flavor');
                renderPriceSection(id);
                if (data.sizes.length) renderFilterSection(id, t('filter_size'), data.sizes, 'size');
            });
            document.querySelectorAll('[data-type]').forEach(cb => {
                cb.addEventListener('change', onFilterChange);
            });
        });
    }

    function onFilterChange(e) {
        const src = e.target;
        document.querySelectorAll(
            `[data-type="${src.dataset.type}"][data-value="${CSS.escape(src.dataset.value)}"]`
        ).forEach(twin => { if (twin !== src) twin.checked = src.checked; });
        const checked = [...document.querySelectorAll('[data-type]:checked')];
        currentParams.flavors = checked.filter(c => c.dataset.type === 'flavor').map(c => c.dataset.value);
        currentParams.sizes = checked.filter(c => c.dataset.type === 'size').map(c => c.dataset.value);
        currentParams.prices = checked.filter(c => c.dataset.type === 'price').map(c => c.dataset.value);
        loadProducts();
    }

    loadFilters();

    const openBtn = document.getElementById('openFilter');
    const closeBtn = document.getElementById('closeFilter');
    const sidebar = document.getElementById('mobileFilterSidebar');
    const overlay = document.getElementById('filterOverlay');
    const applyBtn = document.getElementById('applyFilters');
    const clearBtn = document.querySelector('.clear-filters');

    if (openBtn) openBtn.addEventListener('click', () => { sidebar?.classList.add('active'); overlay?.classList.add('active'); });
    if (closeBtn) closeBtn.addEventListener('click', closeSidebar);
    if (overlay) overlay.addEventListener('click', closeSidebar);
    if (applyBtn) applyBtn.addEventListener('click', closeSidebar);
    if (clearBtn) clearBtn.addEventListener('click', () => {
        currentParams.flavors = []; currentParams.sizes = []; currentParams.prices = [];
        document.querySelectorAll('[data-type]').forEach(cb => cb.checked = false);
        loadProducts();
    });

    function closeSidebar() {
        sidebar?.classList.remove('active');
        overlay?.classList.remove('active');
    }

    let cachedProducts = [];

    function renderProducts(data) {
        cachedProducts = data;
        if (countEl) { countEl.textContent = `${data.length} ${t('products_count') || 'Products'}`; countEl.dataset.count = data.length; }
        if (!data.length) {
            grid.innerHTML = `<div style="padding:60px;text-align:center;color:#6c757d;grid-column:1/-1;">${t('no_products')}</div>`;
            return;
        }
        grid.innerHTML = data.map(p => productCard(p)).join('');
    }

    function loadProducts() {
        grid.innerHTML = `<div style="padding:60px;text-align:center;color:#6c757d;">${t('loading')}</div>`;
        const params = new URLSearchParams();
        if (currentParams.category) params.set('category', currentParams.category);
        if (currentParams.sort) params.set('sort', currentParams.sort);
        if (currentParams.search) params.set('search', currentParams.search);
        currentParams.flavors.forEach(f => params.append('flavor', f));
        currentParams.sizes.forEach(s => params.append('size', s));
        (currentParams.prices || []).forEach(p => params.append('price', p));
        API.get(`/api/products/?${params}`).then(data => renderProducts(data));
    }

    loadProducts();
}   // ← initProductsPage bağlandı

/* ── PRODUCT DETAIL PAGE ─────────────────────────────────── */
function initProductDetailPage() {
    const root = document.getElementById('productDetailRoot');
    if (!root) return;
    const slug = root.dataset.slug;
    if (!slug) return;

    root.innerHTML = `<div style="padding:80px;text-align:center;color:#6c757d;">${t('loading')}</div>`;

    function renderDetail(p) {
        const image = p.image
            ? `<img src="${p.image}" alt="${p.name}" class="main-image">`
            : `<img src="https://www.herbalife.com/dmassets/market-reusable-assets/amer/united-states/images/canister/pc-64z1-us.png:pdp-w875h783?fmt=webp-alpha" alt="${p.name}" class="main-image">`;
        const discountHtml = p.discount_price
            ? `<span style="text-decoration:line-through;color:#aaa;font-size:1.4rem;">$${p.price}</span>` : '';
        const related = p.related?.length
            ? `<div class="container mt-5">
                 <h3 style="color:#2d5f5d;font-weight:300;margin-bottom:24px;">${t('related')}</h3>
                 <div class="product-grid">${p.related.map(r => productCard(r)).join('')}</div>
               </div>` : '';
        root.innerHTML = `
        <section class="product-section">
            <div class="container">
                <div class="row">
                    <div class="col-lg-6">
                        <div class="product-gallery">
                            <div class="main-image-container">
                                ${p.badge ? `<div class="product-badges"><span class="badge-new">${p.badge}</span></div>` : ''}
                                ${image}
                            </div>
                        </div>
                    </div>
                    <div class="col-lg-6">
                        <div class="product-info">
                            ${p.category ? `<div style="color:#6c757d;font-size:.9rem;margin-bottom:8px;">${p.category.name}</div>` : ''}
                            <h1 class="product-title">${p.name}</h1>
                            ${p.flavor_name ? `<div style="display:flex;align-items:center;gap:8px;margin-bottom:12px;">
                                ${p.flavor_color ? `<span style="width:14px;height:14px;border-radius:50%;background:${p.flavor_color};display:inline-block;"></span>` : ''}
                                <span style="color:#6c757d;">${p.flavor_name}</span></div>` : ''}
                            <div class="product-price">$${p.final_price}</div>
                            ${discountHtml}
                            ${p.size ? `<div class="sku-number">${p.size}</div>` : ''}
                            ${p.description ? `<p class="product-subtitle">${p.description}</p>` : ''}
                            <div class="quantity-label">Qty</div>
                            <div class="quantity-selector">
                                <button class="quantity-btn" onclick="changeQty(-1)"><i class="fas fa-minus"></i></button>
                                <input id="detailQty" type="number" class="quantity-value"
                                       value="1" min="1" max="${p.stock}"
                                       style="border:none;text-align:center;width:50px;font-size:1.1rem;font-weight:600;">
                                <button class="quantity-btn" onclick="changeQty(1)"><i class="fas fa-plus"></i></button>
                            </div>
                            ${p.stock > 0
                ? `<button class="add-to-cart-btn" onclick="cartAdd(${p.id}, event)"
                                       style="background:#2d5f5d;color:#fff;border:none;padding:14px 40px;border-radius:30px;font-size:1rem;font-weight:600;cursor:pointer;margin-top:10px;">
                                       ${t('add_to_bag')}</button>`
                : `<button disabled style="background:#ddd;color:#999;border:none;padding:14px 40px;border-radius:30px;font-size:1rem;margin-top:10px;">
                                       ${t('out_of_stock')}</button>`
            }
                        </div>
                    </div>
                </div>
            </div>
        </section>
        ${related}`;
    }

    API.get(`/api/products/${slug}/`).then(p => renderDetail(p));
}   // ← initProductDetailPage bağlandı

function changeQty(delta) {
    const input = document.getElementById('detailQty');
    if (!input) return;
    input.value = Math.min(parseInt(input.max) || 99, Math.max(1, parseInt(input.value) + delta));
}

/* ── CART PAGE ───────────────────────────────────────────── */
function renderCartPage() {
    const root = document.getElementById('cartPageRoot');
    const totalEl = document.getElementById('cartSummaryTotal');
    const countEl = document.getElementById('cartSummaryCount');
    if (!root) return;

    if (!cartState.items.length) {
        root.innerHTML = `
        <div style="padding:80px;text-align:center;color:#6c757d;">
            <p style="font-size:1.3rem;margin-bottom:16px;">${t('cart_empty')}</p>
            <a href="/products" style="color:#2d5f5d;font-weight:600;font-size:1rem;">${t('cart_continue')}</a>
        </div>`;
        if (totalEl) totalEl.textContent = '$0.00';
        if (countEl) countEl.textContent = '0';
        const titleEl = document.querySelector('.cart-page-title');
        if (titleEl) titleEl.textContent = `${t('cart_title')} (0)`;
        return;
    }

    const titleEl = document.querySelector('.cart-page-title');
    if (titleEl) titleEl.textContent = `${t('cart_title')} (${cartState.total_items})`;
    if (totalEl) totalEl.textContent = `$${cartState.total_price}`;
    if (countEl) countEl.textContent = cartState.total_items;

    root.innerHTML = cartState.items.map(item => `
    <div class="cart-item" id="ci-${item.id}">
        ${item.product.image
            ? `<img src="${item.product.image}" alt="${item.product.name}" class="item-image">`
            : `<img src="https://www.herbalife.com/dmassets/market-reusable-assets/amer/united-states/images/canister/pc-64z1-us.png:pdp-w875h783?fmt=webp-alpha" alt="${item.product.name}" class="item-image">`}
        <div class="item-details">
            <div class="item-name">${item.product.name}</div>
            <div class="item-price">$${item.product.final_price} <span class="price-label">${t('cart_price')}</span></div>
            ${item.product.flavor_name ? `
            <div class="item-flavor">${t('cart_flavor')}
                ${item.product.flavor_color ? `<span class="flavor-dot" style="background-color:${item.product.flavor_color};"></span>` : ''}
                ${item.product.flavor_name}
            </div>` : ''}
            <div class="item-actions">
                <div class="quantity-selector">
                    <button class="quantity-btn" onclick="cartUpdate(${item.id}, ${item.quantity - 1})"><i class="fas fa-minus"></i></button>
                    <span class="quantity-value">${item.quantity}</span>
                    <button class="quantity-btn" onclick="cartUpdate(${item.id}, ${item.quantity + 1})"><i class="fas fa-plus"></i></button>
                </div>
                <button class="action-link" onclick="cartRemove(${item.id})">${t('cart_remove')}</button>
            </div>
            <div style="font-size:.9rem;color:#6c757d;margin-top:6px;">
                ${t('cart_subtotal')} <strong>$${item.subtotal}</strong>
            </div>
        </div>
    </div>`).join('');
}   // ← renderCartPage bağlandı

function initCartPage() {
    if (!document.getElementById('cartPageRoot')) return;
    loadCart();
}

/* ── LIVE SEARCH ─────────────────────────────────────────── */
function initHeaderSearch() {
    const input = document.getElementById('headerSearchInput');
    const dropdown = document.getElementById('headerSearchDropdown');
    if (!input || !dropdown) return;

    let timer;
    input.addEventListener('input', function () {
        clearTimeout(timer);
        const q = this.value.trim();
        if (q.length < 2) { dropdown.style.display = 'none'; return; }
        timer = setTimeout(() => {
            API.get(`/api/search/suggest/?q=${encodeURIComponent(q)}`).then(data => {
                if (!data.results.length) { dropdown.style.display = 'none'; return; }
                dropdown.innerHTML = data.results.map(p => `
                <li>
                    <a href="/products/${p.slug}/" style="display:flex;align-items:center;gap:10px;padding:8px 14px;text-decoration:none;color:#222;"
                       onmouseover="this.style.background='#f9f0ef'" onmouseout="this.style.background=''">
                        ${p.image
                        ? `<img src="${p.image}" style="width:40px;height:40px;object-fit:cover;border-radius:6px;flex-shrink:0;">`
                        : `<div style="width:40px;height:40px;border-radius:6px;background:#2d5f5d;color:#fff;display:flex;align-items:center;justify-content:center;font-weight:700;">${p.name[0]}</div>`}
                        <span style="flex:1;font-size:13px;">${p.name}</span>
                        <span style="font-size:13px;font-weight:600;color:#2d5f5d;">$${p.final_price}</span>
                    </a>
                </li>`).join('') +
                    `<li style="border-top:1px solid #f0f0f0;">
                    <a href="/products?search=${encodeURIComponent(q)}"
                       style="display:block;padding:9px 14px;text-align:center;font-size:13px;font-weight:600;color:#2d5f5d;text-decoration:none;">
                        ${t('see_all')} →
                    </a>
                </li>`;
                dropdown.style.display = 'block';
            });
        }, 300);
    });

    input.addEventListener('keydown', e => {
        if (e.key === 'Enter') { e.preventDefault(); const q = input.value.trim(); if (q) location.href = `/products?search=${encodeURIComponent(q)}`; }
        if (e.key === 'Escape') dropdown.style.display = 'none';
    });
    document.addEventListener('click', e => {
        if (!dropdown.contains(e.target) && e.target !== input) dropdown.style.display = 'none';
    });
}   // ← initHeaderSearch bağlandı

function toggleSearchBox() {
    const box = document.getElementById('headerSearchBox');
    if (!box) return;
    const visible = box.style.display !== 'none';
    box.style.display = visible ? 'none' : 'block';
    if (!visible) document.getElementById('headerSearchInput')?.focus();
}

/* ── TOAST ───────────────────────────────────────────────── */
function showToast(msg, type = 'success') {
    let container = document.getElementById('toastContainer');
    if (!container) {
        container = document.createElement('div');
        container.id = 'toastContainer';
        container.style.cssText = 'position:fixed;bottom:24px;right:24px;z-index:9999;display:flex;flex-direction:column;gap:10px;';
        document.body.appendChild(container);
    }
    const toast = document.createElement('div');
    toast.style.cssText = `background:${type === 'success' ? '#2d5f5d' : '#e8483b'};color:#fff;padding:12px 20px;border-radius:10px;font-size:14px;box-shadow:0 4px 20px rgba(0,0,0,.2);opacity:0;transform:translateY(10px);transition:opacity .3s,transform .3s;max-width:280px;`;
    toast.textContent = msg;
    container.appendChild(toast);
    requestAnimationFrame(() => { toast.style.opacity = '1'; toast.style.transform = 'translateY(0)'; });
    setTimeout(() => { toast.style.opacity = '0'; setTimeout(() => toast.remove(), 300); }, 3000);
}   // ← showToast bağlandı

/* ── CHECKOUT LOGIN CHECK ────────────────────────────────── */
function checkLoginBeforeCheckout(e) {
    e.preventDefault();
    if (cartState.total_items === 0) {
        showToast(t('cart_empty'), 'error');
        return false;
    }
    API.get('/api/auth/status/').then(data => {
        window.location.href = data.authenticated ? '/checkout/' : '/login/?next=/checkout/';
    });
    return false;
}

/* ── INIT ────────────────────────────────────────────────── */
document.addEventListener('DOMContentLoaded', function () {
    loadCart();
    initHeaderSearch();
    const path = location.pathname;
    if (path === '/' || path === '') initHomePage();
    if (path.startsWith('/products') && !path.includes('/products/')) initProductsPage();
    if (path.startsWith('/products/')) initProductDetailPage();
    if (path === '/cart' || path === '/cart/') initCartPage();
});

function initHomePage() { }   // Home static templatedir, JS lazım deyil

(function () {

    const API_STORE_INFO = window.API_URLS.storeInfo;
    const API_STORE_SWITCH = window.API_URLS.storeSwitch;

    let activeStoreCode = null;
    async function detectAndSetLocation() {
        try {
            const stored = sessionStorage.getItem('store_selected');
            if (stored) return;

            const geo = await fetch('/api/location/').then(r => r.json());
            const countryCode = geo.country_code;

            const countryToStore = {
                'AZ': 'AZ',
                'US': 'US',
                'RU': 'RU',
                'TR': 'TR',
            };

            const storeCode = countryToStore[countryCode];
            if (storeCode && storeCode !== activeStoreCode) {
                await window.switchStore(storeCode);
                sessionStorage.setItem('store_selected', '1');
            }
        } catch (e) {
            console.log('Location detect failed:', e);
        }
    }

    async function initStoreSwitcher() {
        try {
            const data = await fetch(API_STORE_INFO).then(r => r.json());
            const active = data.active;
            const all = data.all;

            activeStoreCode = active ? active.code : null;


            if (active) {
                document.getElementById('storeFlag').innerHTML = '<i class="fa-solid fa-location-dot"></i>';
                document.getElementById('storeCurrency').textContent = active.currency;
            }

            // Dropdown siyahısını doldur
            const list = document.getElementById('storeList');
            list.innerHTML = all.map(s => `
            <button class="store-option ${s.code === activeStoreCode ? 'active' : ''}"
                    data-code="${s.code}">
                <span class="flag">${s.flag_emoji || '🌍'}</span>
                <span class="info">
                    <span class="name">${s.name}</span>
                    <span class="currency">${s.currency}</span>
                </span>
                <i class="fas fa-check check"></i>
            </button>`).join('');

            // Event delegation
            document.getElementById('storeList').addEventListener('click', function (e) {
                const btn = e.target.closest('.store-option');
                if (btn) window.switchStore(btn.dataset.code);
            });
        } catch (e) {
            document.getElementById('storeList').innerHTML =
                '<div style="padding:16px;color:#aaa;font-size:.85rem">{% trans "Failed to load stores." %}</div>';
        }
    }

    window.toggleStoreDropdown = function () {
        const dd = document.getElementById('storeDropdown');
        const chv = document.getElementById('storeChevron');
        if (!dd || !chv) return;
        dd.classList.toggle('open');
        chv.classList.toggle('rotated');
    };

    // Dışarı tıklayanda kapat
    document.addEventListener('click', function (e) {
        if (!document.getElementById('storeSwitcher').contains(e.target)) {
            document.getElementById('storeDropdown').classList.remove('open');
            document.getElementById('storeChevron').classList.remove('rotated');
        }
    });

    window.switchStore = async function (code) {
        if (code === activeStoreCode) {
            toggleStoreDropdown();
            return;
        }
        try {
            const res = await fetch(API_STORE_SWITCH, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json', 'X-CSRFToken': getCookie('csrftoken') },
                body: JSON.stringify({ store_code: code })
            });
            const data = await res.json();
            if (data.success) {
                // Navbar-ı güncəllə
                window.location.reload();
                document.getElementById('storeFlag').innerHTML = '<i class="fa-solid fa-location-dot"></i>';
                document.getElementById('storeCurrency').textContent = data.store.currency;
                activeStoreCode = code;

                // Active class-ları güncəllə
                document.querySelectorAll('.store-option').forEach(btn => {
                    btn.classList.toggle('active', btn.dataset.code === code);
                });

                toggleStoreDropdown();

                // Səhifəni refresh et ki məhsullar yenilənsin
                // (əgər products API-si zaten store-a görə filter edirsə)
                if (typeof loadProducts === 'function') loadProducts();
                if (typeof loadPosts === 'function') loadPosts();
                // Yox əgər tam reload istəyirsənsə:
                // window.location.reload();
            }
        } catch (e) {
            console.error('Store switch failed:', e);
        }
    };

    function getCookie(name) {
        let v = null;
        document.cookie.split(';').forEach(c => {
            c = c.trim();
            if (c.startsWith(name + '=')) v = decodeURIComponent(c.slice(name.length + 1));
        });
        return v;
    }

    // storeBtn click
    document.getElementById('storeBtn').addEventListener('click', function (e) {
        e.stopPropagation();
        window.toggleStoreDropdown();
    });

    // Siyahı loading skeletonu göstər
    document.getElementById('storeList').innerHTML = `
    <div class="store-loading">
        <div class="store-sk" style="width:80%"></div>
        <div class="store-sk" style="width:65%"></div>
        <div class="store-sk" style="width:75%"></div>
    </div>`;

    initStoreSwitcher();
})();