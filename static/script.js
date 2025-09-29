// Подключение Telegram WebApp API
const tg = window.Telegram.WebApp;
tg.expand();
tg.ready();

// Получаем элементы
const orderCard = document.getElementById("orderCard");
const catalogCard = document.getElementById("catalogCard");
const sendBtn = document.getElementById("sendBtn");
const status = document.getElementById("status");
const mainContent = document.querySelector(".main");


// ======== Для выбора доставки =========
const deliverySelect = document.getElementById("delivery");
const metroBlock = document.getElementById("metroBlock");
const metroSelect = document.getElementById("metro"); // <--- добавили

deliverySelect.addEventListener("change", () => {
  if (deliverySelect.value === "pickup") {
    metroBlock.style.display = "none"; // скрываем весь блок
  } else if (deliverySelect.value === "delivery") {
    metroBlock.style.display = "block"; // показываем
  }
});

// ======== Для выбора доставки =========



// Автозаполнение username
try {
  const user = tg.initDataUnsafe && tg.initDataUnsafe.user ? tg.initDataUnsafe.user : null;
  if (user) {
    const username = user.username ? '@' + user.username : (user.first_name || '');
    if (username) document.getElementById('username').value = username;
  }
} catch (e) {
  console.warn("initDataUnsafe unavailable", e);
}

// ======= ФУНКЦИИ =======
function openOrder() {
  orderCard.classList.add("show");
  mainContent.classList.add("blur");
}

function closeOrder() {
  orderCard.classList.remove("show");
  mainContent.classList.remove("blur");
}

function openCatalog() {
  catalogCard.classList.add("show");
  mainContent.classList.add("blur");
}

function closeCatalog() {
  catalogCard.classList.remove("show");
  mainContent.classList.remove("blur");
}

// ======= ВАЛИДАЦИЯ =======
function validate() {
  const username = document.getElementById('username').value.trim();
  const item = document.getElementById('item').value.trim();
  const count = document.getElementById('count').value.trim();
  const delivery = document.getElementById('delivery').value.trim();
  const metro = document.getElementById('metro').value;

  const countNum = Number(count);
  if (!username || !item || isNaN(countNum) || countNum <= 0 || !delivery) return false;
  if (delivery === "delivery" && !metro) return false;

  const metroName = deliverySelect.value === "delivery" 
    ? metroSelect.options[metroSelect.selectedIndex].text : "";

  return true;
}

// ======= ОТПРАВКА =======
sendBtn.addEventListener('click', () => {
  if (!validate()) {
    status.textContent = "Заполните все поля правильно.";
    return;
  }

  const metroName = deliverySelect.value === "delivery" 
    ? metroSelect.options[metroSelect.selectedIndex].text 
    : "";

  const data = {
    username: document.getElementById('username').value.trim(),
    size: document.getElementById('size').value,
    item: document.getElementById('item').value.trim(),
    count: document.getElementById('count').value.trim(),
    delivery: deliverySelect.value,
    metro: metroName
  };

  try {
    tg.sendData(JSON.stringify(data));
    status.textContent = "Отправлено. Закрываю WebApp...";
    sendBtn.disabled = true;
    setTimeout(() => tg.close(), 700);
  } catch (err) {
    status.textContent = "Ошибка: " + (err.message || err);
  }
});


