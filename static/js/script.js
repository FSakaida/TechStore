const PRODUCTS = [
    { id: 1, name: "Notebook Lenovo", category: "Computadores", price: 3499.90, icon: "NB", color: "blue" },
    { id: 2, name: "Mouse Logitech", category: "Acessórios", price: 129.90, icon: "MS", color: "orange" },
    { id: 3, name: "Teclado Mecânico", category: "Acessórios", price: 299.90, icon: "TC", color: "purple" },
    { id: 4, name: "Monitor 24 polegadas", category: "Monitores", price: 899.90, icon: "MN", color: "green" },
    { id: 5, name: "Headset USB", category: "Áudio", price: 219.90, icon: "HS", color: "red" },
    { id: 6, name: "Webcam Full HD", category: "Vídeo", price: 189.90, icon: "WC", color: "cyan" }
];

const CART_KEY = "techstore_cart";

function readCart() {
    try {
        return JSON.parse(localStorage.getItem(CART_KEY)) || [];
    } catch {
        return [];
    }
}

function saveCart(cart) {
    localStorage.setItem(CART_KEY, JSON.stringify(cart));
    updateCartCount();
}

function money(value) {
    return value.toLocaleString("pt-BR", {
        style: "currency",
        currency: "BRL"
    });
}

function cartQuantity() {
    return readCart().reduce((total, item) => total + item.quantity, 0);
}

function updateCartCount() {
    document.querySelectorAll("[data-cart-count]").forEach((element) => {
        element.textContent = cartQuantity();
    });
}

function showToast(message) {
    const toast = document.querySelector("[data-toast]");
    if (!toast) return;

    toast.textContent = message;
    toast.classList.add("show");
    window.setTimeout(() => toast.classList.remove("show"), 2200);
}

function addToCart(productId) {
    const cart = readCart();
    const existing = cart.find((item) => item.id === productId);

    if (existing) {
        existing.quantity += 1;
    } else {
        cart.push({ id: productId, quantity: 1 });
    }

    saveCart(cart);
    showToast("Produto adicionado ao carrinho.");
}

function productById(id) {
    return PRODUCTS.find((product) => product.id === id);
}

function calculateTotal(cart) {
    return cart.reduce((total, item) => {
        const product = productById(item.id);
        return product ? total + product.price * item.quantity : total;
    }, 0);
}

function renderCatalog() {
    const grid = document.querySelector("[data-product-grid]");
    if (!grid) return;

    grid.innerHTML = PRODUCTS.map((product) => `
        <article class="product-card">
            <div class="product-visual ${product.color}" aria-hidden="true">
                <span>${product.icon}</span>
            </div>
            <div class="product-info">
                <p class="product-category">${product.category}</p>
                <h3>${product.name}</h3>
                <p class="product-price">${money(product.price)}</p>
                <button class="button primary full" type="button" data-add-product="${product.id}">
                    Adicionar ao carrinho
                </button>
            </div>
        </article>
    `).join("");

    grid.addEventListener("click", (event) => {
        const button = event.target.closest("[data-add-product]");
        if (button) addToCart(Number(button.dataset.addProduct));
    });
}

function changeQuantity(productId, change) {
    const cart = readCart();
    const item = cart.find((cartItem) => cartItem.id === productId);
    if (!item) return;

    item.quantity += change;
    const updatedCart = cart.filter((cartItem) => cartItem.quantity > 0);
    saveCart(updatedCart);
    renderCart();
}

function removeFromCart(productId) {
    saveCart(readCart().filter((item) => item.id !== productId));
    renderCart();
    showToast("Produto removido do carrinho.");
}

function renderCart() {
    const container = document.querySelector("[data-cart-items]");
    if (!container) return;

    const cart = readCart();
    const checkoutLink = document.querySelector("[data-checkout-link]");

    if (cart.length === 0) {
        container.innerHTML = `
            <div class="empty-state">
                <span aria-hidden="true">0</span>
                <h2>Seu carrinho está vazio</h2>
                <p>Adicione algum produto para continuar.</p>
                <a class="button primary" href="/">Ver produtos</a>
            </div>
        `;
        checkoutLink?.classList.add("disabled");
    } else {
        container.innerHTML = cart.map((item) => {
            const product = productById(item.id);
            if (!product) return "";

            return `
                <article class="cart-item">
                    <div class="mini-visual ${product.color}" aria-hidden="true">${product.icon}</div>
                    <div class="cart-item-info">
                        <p>${product.category}</p>
                        <h2>${product.name}</h2>
                        <strong>${money(product.price)}</strong>
                    </div>
                    <div class="quantity-control" aria-label="Quantidade de ${product.name}">
                        <button type="button" data-change="-1" data-product-id="${product.id}" aria-label="Diminuir quantidade">−</button>
                        <span>${item.quantity}</span>
                        <button type="button" data-change="1" data-product-id="${product.id}" aria-label="Aumentar quantidade">+</button>
                    </div>
                    <button class="remove-button" type="button" data-remove="${product.id}">Remover</button>
                </article>
            `;
        }).join("");
        checkoutLink?.classList.remove("disabled");
    }

    const total = calculateTotal(cart);
    document.querySelector("[data-subtotal]").textContent = money(total);
    document.querySelector("[data-total]").textContent = money(total);

    container.onclick = (event) => {
        const quantityButton = event.target.closest("[data-change]");
        const removeButton = event.target.closest("[data-remove]");

        if (quantityButton) {
            changeQuantity(Number(quantityButton.dataset.productId), Number(quantityButton.dataset.change));
        }
        if (removeButton) {
            removeFromCart(Number(removeButton.dataset.remove));
        }
    };
}

function renderCheckout() {
    const container = document.querySelector("[data-checkout-items]");
    if (!container) return;

    const cart = readCart();
    if (cart.length === 0) {
        window.location.href = "/carrinho";
        return;
    }

    container.innerHTML = cart.map((item) => {
        const product = productById(item.id);
        if (!product) return "";
        return `
            <div class="checkout-item">
                <span>${item.quantity} × ${product.name}</span>
                <strong>${money(product.price * item.quantity)}</strong>
            </div>
        `;
    }).join("");

    document.querySelector("[data-checkout-total]").textContent = money(calculateTotal(cart));

    const form = document.querySelector("[data-checkout-form]");
    form.addEventListener("submit", (event) => {
        event.preventDefault();
        if (!form.reportValidity()) return;

        const orderNumber = String(Date.now()).slice(-6);
        sessionStorage.setItem("techstore_order", orderNumber);
        localStorage.removeItem(CART_KEY);
        window.location.href = "/sucesso";
    });
}

function renderSuccess() {
    const element = document.querySelector("[data-order-number]");
    if (!element) return;
    element.textContent = `#${sessionStorage.getItem("techstore_order") || "000001"}`;
}

document.addEventListener("DOMContentLoaded", () => {
    updateCartCount();
    renderCatalog();
    renderCart();
    renderCheckout();
    renderSuccess();
});
