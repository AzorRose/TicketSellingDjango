// Получаем элементы кнопок, полей ввода и контейнера вывода
var button1 = document.getElementById("button1");
var button2 = document.getElementById("button2");
var button3 = document.getElementById("button3");
var output = document.getElementById("output");
var buttons = document.querySelectorAll(".choice");
var inputContainers = document.querySelectorAll(".input-container");

// Добавляем обработчики событий для каждой кнопки
buttons.forEach(function (button, index) {
    button.addEventListener("click", function () {
        // Снимаем класс "active" со всех кнопок
        buttons.forEach(function (btn) {
            btn.classList.remove("active");
        });
        // Добавляем класс "active" к текущей кнопке
        button.classList.add("active");

        // Скрываем все контейнеры и показываем только нужный
        inputContainers.forEach(function (container) {
            container.style.display = "none";
        });
        inputContainers[index].style.display = "block";
    });
});

// Скрываем все контейнеры для начала
inputContainers.forEach(function (container) {
    container.style.display = "none";
});

// Активируем первую кнопку и соответствующий контейнер
buttons[0].classList.add("active");
inputContainers[0].style.display = "block";

// Добавляем обработчики событий для каждой кнопки
button1.addEventListener("click", function () {
    // Скрываем все контейнеры и показываем только нужный
    inputContainers.forEach(function (container) {
        container.style.display = "none";
    });
    inputContainers[0].style.display = "block";
});

button2.addEventListener("click", function () {
    // Скрываем все контейнеры и показываем только нужный
    inputContainers.forEach(function (container) {
        container.style.display = "none";
    });
    inputContainers[1].style.display = "block";
});

button3.addEventListener("click", function () {
    // Скрываем все контейнеры и показываем только нужный
    inputContainers.forEach(function (container) {
        container.style.display = "none";
    });
    inputContainers[2].style.display = "block";
});