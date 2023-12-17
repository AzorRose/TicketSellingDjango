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
    const dataSeat = seat.getAttribute('dataseat');
    const dataRow = seat.getAttribute('datarow');

    seat.addEventListener('click', () => {
        
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


document.addEventListener("DOMContentLoaded", async function () {
    var seats = Array.from(document.querySelectorAll('.seat'));
    var bookedPlacesCache = null;

    async function getBookedPlaces() {
        try {
            const response = await fetch('/api/get_booked_places/');
            const data = await response.json();
            bookedPlacesCache = data.booked_places;
            // Store in localStorage for caching
            localStorage.setItem('bookedPlacesCache', JSON.stringify(bookedPlacesCache));
            return bookedPlacesCache;
        } catch (error) {
            console.error('Error:', error);
        }
    }

    async function checkSeatStatus(seat, dataSeat, dataRow) {
        if (bookedPlacesCache === null) {
            // If the cache is not available, fetch booked places
            await getBookedPlaces();
        }

        if (bookedPlacesCache.some(place => place.spot_num == dataSeat && place.spot_row == dataRow && place.available == true)) {
            seat.style.fill = '#EEECEC';
            seat.addEventListener('mouseover', () => {
                seat.style.filter = 'none';
                tooltip.style.display = 'none';
            });
            seat.addEventListener('click', () => {
                seat.style.fill = '#EEECEC';
            });
        }
    }

    try {
        const startTime = performance.now();

        // Try to retrieve data from localStorage first
        const cachedData = localStorage.getItem('bookedPlacesCache');
        if (cachedData) {
            bookedPlacesCache = JSON.parse(cachedData);
        } else {
            await getBookedPlaces();
        }

        // Batch requests for all seats
        const promises = seats.map(seat => {
            const dataSeat = seat.getAttribute('dataseat');
            const dataRow = seat.getAttribute('datarow');
            return checkSeatStatus(seat, dataSeat, dataRow);
        });

        // Wait for all promises to resolve
        await Promise.all(promises);

        const endTime = performance.now();
        const elapsedTime = endTime - startTime;

        console.log('All fetch operations completed in', elapsedTime, 'milliseconds');
    } catch (error) {
        console.error('Error:', error);
    }
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