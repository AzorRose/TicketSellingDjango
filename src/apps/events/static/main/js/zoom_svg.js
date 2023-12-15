// Получаем элемент SVG 
let svg = document.querySelector('.info-form svg');

// Текущий масштаб
let scale = 1;

// Текущее смещение
let panX = 0;
let panY = 0;

const minZoom = 1;
const maxZoom = 3;

function zoom(scale) {
    svg.style.transition = "transform 0.2s";
    setTimeout(() => {
        svg.style.transition = "";
    }, 200);
}

// Кнопки управления масштабом
document.getElementById('zoom-in').addEventListener('click', () => {
  scale *= 1.5;
  scale = Math.min(maxZoom, Math.max(minZoom, scale));
  svg.style.transform = `scale(${scale}) translate(${panX}px, ${panY}px)`; 
  zoom(scale);
});

document.getElementById('zoom-out').addEventListener('click', () => {
  scale /= 1.5;
  scale = Math.min(maxZoom, Math.max(minZoom, scale));
  svg.style.transform = `scale(${scale}) translate(${panX}px, ${panY}px)`;
  zoom(scale);
});
  
let seats = document.querySelectorAll('.seat');
let seatInfoDiv = document.getElementById('footer-place-container');
let tooltip = document.getElementById('tooltip');

seats.forEach(seat => {

    let defaultColor = seat.style.fill;

    seat.addEventListener('click', () => {
        const dataSeat = seat.getAttribute('dataseat');
        const dataRow = seat.getAttribute('datarow');
        if(seat.style.fill === defaultColor) {
        seat.style.fill = 'red';
        var data = {
            key1: dataRow,
            key2: dataSeat
            };
            
            // Опции запроса
            var options = {
            method: 'POST', // Метод запроса
            headers: {
            'Content-Type': 'application/json' // Тип содержимого (JSON, например)
            },
            body: JSON.stringify(data) // Преобразование объекта в JSON и установка в тело запроса
            };
            
            // URL вашего Django-обработчика
            var url = 'http://127.0.0.1:8000/concerts/chudnevets-1';
            
            // Отправка запроса с использованием Fetch API
            fetch(url, options)
            .then(response => response.json()) // Распарсить ответ в JSON
            .then(data => {
            // Обработка ответа от сервера
            console.log('Success:', data);
            })
            .catch(error => {
            // Обработка ошибок
            console.error('Error:', error);
            });

        } else {
        seat.style.fill = defaultColor;
        }
    });

    seat.addEventListener('mouseover', function(event) {
        const dataSeat = seat.getAttribute('dataseat');
        const dataRow = seat.getAttribute('datarow');
        const viewportWidth = window.innerWidth || document.documentElement.clientWidth;
        const viewportHeight = window.innerHeight || document.documentElement.clientHeight;

        // Check and adjust tooltip position if necessary
        if (event.clientX + tooltip.offsetWidth > viewportWidth) {
            tooltip.style.left = `${viewportWidth - tooltip.offsetWidth - 10}px`;
        }

        if (event.clientY + tooltip.offsetHeight > viewportHeight) {
            tooltip.style.top = `${viewportHeight - tooltip.offsetHeight - 10}px`;
        }

        seat.style.filter = 'drop-shadow(0 0 3px #666)';
        tooltip.innerHTML = `<p></p>Стол: ${dataSeat}, Место: ${dataRow}</p>`;
        
        tooltip.style.display = 'block';
        
    });
   
    
    seat.addEventListener('mouseout', () => {
        seat.style.filter = 'none';
        tooltip.style.display = 'none';
    });
});


document.addEventListener("DOMContentLoaded", function () {
    // Получаем все элементы с классом "seat"
    var seats = document.querySelectorAll('.seat');

    // Создаем функцию для выполнения fetch
    function checkSeatStatus(seat, dataSeat, dataRow) {
        
        return fetch('/api/get_booked_places/')
            .then(response => response.json())
            .then(data => {
                if (data.booked_places.some(place => place.spot_num == dataSeat && place.spot_row == dataRow && place.available == true)) {
                    seat.style.fill = '#EEECEC';
                    seat.addEventListener('mouseover', () => {
                        seat.style.filter = 'none';
                        tooltip.style.display = 'none';
                    });
                    seat.addEventListener('click', e => {
                        seat.style.fill = '#EEECEC';
                    });
                }
            })
            .catch(error => console.error('Error:', error));
    }

    // Создаем массив промисов для всех fetch операций
    var promises = [];

    // Проходим по каждому элементу
    seats.forEach(function (seat) {
        // Получаем значения атрибутов dataseat и datarow
        var dataSeat = seat.getAttribute('dataseat');
        var dataRow = seat.getAttribute('datarow');

        // Добавляем промис в массив
        var promise = checkSeatStatus(seat, dataSeat, dataRow);

        // Добавляем промис в массив
        promises.push(promise);
    });

    // Ждем, пока все промисы завершатся
    Promise.all(promises)
        .then(() => {
            // Все fetch операции завершены
            console.log('All fetch operations completed');
        });
});




let startX, startY;

svg.addEventListener('mousedown', e => {
startX = e.clientX;
startY = e.clientY;
});

svg.addEventListener('mousemove', e => {

    if(!startX || !startY) return;
    
    let dx = e.clientX - startX;
    let dy = e.clientY - startY; 
    
    panX += dx;
    panY += dy;
    
    svg.style.transform = `translate(${panX}px, ${panY}px) scale(${scale})`;
    
    startX = e.clientX; 
    startY = e.clientY;
});

svg.addEventListener('mouseup', () => {
    startX = null;
    startY = null; 
  });