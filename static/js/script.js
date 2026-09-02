const PRODUCT_COLORS = ["blue", "orange", "purple", "green", "red", "cyan"];
let PRODUCTS = [];
let cart = [];

function readProducts() {
    const element = document.querySelector("#products-data");
    if (!element) return [];

    try {
        return JSON.parse(element.textContent);
    } catch {
        return [];
    }
}

function productById(id) {
    return PRODUCTS.find((product) => product.id === id);
}

function productInitials(name) {
    return name
        .split(/\s+/)
        .filter(Boolean)
        .slice(0, 2)
        .map((part) => part[0].toUpperCase())
        .join("");
}

function productColor(product) {
    return PRODUCT_COLORS[(product.id - 1) % PRODUCT_COLORS.length];
}

function escapeHtml(value) {
    const element = document.createElement("span");
    element.textContent = String(value);
    return element.innerHTML;
}

function money(value) {
    return Number(value).toLocaleString("pt-BR", {
        style: "currency",
        currency: "BRL"
    });
}

function cartQuantity() {
    return cart.reduce((total, item) => total + item.quantity, 0);
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
    window.setTimeout(() => toast.classList.remove("show"), 2600);
}

async function requestJson(url, options = {}) {
    const response = await fetch(url, {
        ...options,
        headers: {
            "Content-Type": "application/json",
            ...(options.headers || {})
        }
    });
    const data = await response.json().catch(() => ({}));

    if (!response.ok) {
        throw new Error(data.erro || "Não foi possível concluir a operação.");
    }
    return data;
}

async function loadCart() {
    const data = await requestJson("/api/carrinho");
    cart = data.itens;
    updateCartCount();
}

async function addToCart(productId) {
    const data = await requestJson(`/api/carrinho/itens/${productId}`, {
        method: "POST",
        body: JSON.stringify({ quantidade: 1 })
    });
    cart = data.itens;
    updateCartCount();
    renderCatalog();
    showToast("Produto adicionado ao carrinho.");
}

function calculateTotal(items) {
    return items.reduce((total, item) => {
        const product = productById(item.id);
        return product ? total + product.price * item.quantity : total;
    }, 0);
}

function renderCatalog() {
    const grid = document.querySelector("[data-product-grid]");
    if (!grid) return;

    if (PRODUCTS.length === 0) {
        grid.innerHTML = `
            <div class="empty-state">
                <span aria-hidden="true">0</span>
                <h2>Nenhum produto disponível</h2>
                <p>O catálogo ainda não possui produtos cadastrados.</p>
            </div>
        `;
        return;
    }

    grid.innerHTML = PRODUCTS.map((product) => {
        const cartItem = cart.find((item) => item.id === product.id);
        const atLimit = (cartItem?.quantity || 0) >= product.stock;
        const unavailable = product.stock <= 0 || atLimit;
        const buttonText = product.stock <= 0 ? "Sem estoque" : "Adicionar ao carrinho";

        return `
            <article class="product-card">
                <div class="product-visual ${productColor(product)}" aria-hidden="true">
                    <span>${escapeHtml(productInitials(product.name))}</span>
                </div>
                <div class="product-info">
                    <p class="product-category">${escapeHtml(product.category)} · ${product.stock} em estoque</p>
                    <h3>${escapeHtml(product.name)}</h3>
                    <p class="product-price">${money(product.price)}</p>
                    <button class="button primary full${unavailable ? " disabled" : ""}"
                            type="button"
                            data-add-product="${product.id}"
                            ${unavailable ? "disabled" : ""}>
                        ${buttonText}
                    </button>
                </div>
            </article>
        `;
    }).join("");
}

async function changeQuantity(productId, change) {
    const data = await requestJson(`/api/carrinho/itens/${productId}`, {
        method: "PATCH",
        body: JSON.stringify({ alteracao: change })
    });
    cart = data.itens;
    updateCartCount();
    renderCart();
}

async function removeFromCart(productId) {
    const data = await requestJson(`/api/carrinho/itens/${productId}`, {
        method: "DELETE"
    });
    cart = data.itens;
    updateCartCount();
    renderCart();
    showToast("Produto removido do carrinho.");
}

function renderCart() {
    const container = document.querySelector("[data-cart-items]");
    if (!container) return;

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
                    <div class="mini-visual ${productColor(product)}" aria-hidden="true">${escapeHtml(productInitials(product.name))}</div>
                    <div class="cart-item-info">
                        <p>${escapeHtml(product.category)}</p>
                        <h2>${escapeHtml(product.name)}</h2>
                        <strong>${money(product.price)}</strong>
                    </div>
                    <div class="quantity-control" aria-label="Quantidade de ${escapeHtml(product.name)}">
                        <button type="button" data-change="-1" data-product-id="${product.id}" aria-label="Diminuir quantidade">−</button>
                        <span>${item.quantity}</span>
                        <button type="button" data-change="1" data-product-id="${product.id}" aria-label="Aumentar quantidade" ${item.quantity >= product.stock ? "disabled" : ""}>+</button>
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
}

function bindCartEvents() {
    const container = document.querySelector("[data-cart-items]");
    if (!container) return;

    container.addEventListener("click", async (event) => {
        const quantityButton = event.target.closest("[data-change]");
        const removeButton = event.target.closest("[data-remove]");

        try {
            if (quantityButton) {
                quantityButton.disabled = true;
                await changeQuantity(
                    Number(quantityButton.dataset.productId),
                    Number(quantityButton.dataset.change)
                );
            } else if (removeButton) {
                removeButton.disabled = true;
                await removeFromCart(Number(removeButton.dataset.remove));
            }
        } catch (error) {
            showToast(error.message);
            renderCart();
        }
    });
}

function renderCheckout() {
    const container = document.querySelector("[data-checkout-items]");
    if (!container) return;

    if (cart.length === 0) {
        window.location.href = "/carrinho";
        return;
    }

    container.innerHTML = cart.map((item) => {
        const product = productById(item.id);
        if (!product) return "";
        return `
            <div class="checkout-item">
                <span>${item.quantity} × ${escapeHtml(product.name)}</span>
                <strong>${money(product.price * item.quantity)}</strong>
            </div>
        `;
    }).join("");

    document.querySelector("[data-checkout-total]").textContent = money(calculateTotal(cart));
}

function bindCheckoutForm() {
    const form = document.querySelector("[data-checkout-form]");
    if (!form) return;

    form.addEventListener("submit", async (event) => {
        event.preventDefault();
        if (!form.reportValidity()) return;

        const button = form.querySelector("button[type='submit']");
        button.disabled = true;

        try {
            const dados = Object.fromEntries(new FormData(form).entries());
            const response = await requestJson("/api/checkout", {
                method: "POST",
                body: JSON.stringify(dados)
            });
            sessionStorage.setItem("techstore_order", String(response.pedido_id));
            cart = [];
            window.location.href = "/sucesso";
        } catch (error) {
            showToast(error.message);
            button.disabled = false;
        }
    });
}

function renderSuccess() {
    const element = document.querySelector("[data-order-number]");
    if (!element) return;
    element.textContent = `#${sessionStorage.getItem("techstore_order") || "000001"}`;
}

document.addEventListener("DOMContentLoaded", async () => {
    PRODUCTS = readProducts();
    localStorage.removeItem("techstore_cart");

    try {
        await loadCart();
    } catch (error) {
        showToast(error.message);
    }

    renderCatalog();
    renderCart();
    bindCartEvents();
    renderCheckout();
    bindCheckoutForm();
    renderSuccess();

    const grid = document.querySelector("[data-product-grid]");
    grid?.addEventListener("click", async (event) => {
        const button = event.target.closest("[data-add-product]");
        if (!button) return;

        button.disabled = true;
        try {
            await addToCart(Number(button.dataset.addProduct));
        } catch (error) {
            showToast(error.message);
            renderCatalog();
        }
    });
});
