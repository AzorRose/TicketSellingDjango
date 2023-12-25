// Получаем элемент SVG 
let svg = document.querySelector('.info-form svg');
var eventFilter = document.getElementById("event-section").getAttribute("data-filter");
var eventSlug = document.getElementById("event-section").getAttribute("data-slug");
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
let selectedSeats = {};

seats.forEach(seat => {

    let defaultColor = seat.style.fill;
    const type = seat.getAttribute("class")
    const dataSeat = seat.getAttribute('dataseat');
    const dataRow = seat.getAttribute('datarow');

    seat.addEventListener('click', () => {
        
        if(seat.style.fill === defaultColor) {
        seat.style.fill = 'red';
        selectedSeats[`${type}-${dataRow}-${dataSeat}`] = { type: type, row: dataRow, seat: dataSeat };
        }
        else {
            delete selectedSeats[`${type}-${dataRow}-${dataSeat}`];
            seat.style.fill = defaultColor;
        }
    });

    seat.addEventListener('mouseover', function(event) {
        const dataSeat = seat.getAttribute('dataseat');
        const dataRow = seat.getAttribute('datarow');
        
        seat.style.filter = 'drop-shadow(0 0 3px #666)';
        tooltip.innerHTML = `<p></p>Стол: ${dataSeat}, Место: ${dataRow}</p>`;
        
        tooltip.style.display = 'block';
        
    });
   
    seat.addEventListener('mouseout', () => {
        seat.style.filter = 'none';
        tooltip.style.display = 'none';
    });
});

async function checkSeatAvailability(selectedSeats) {
    // Добавляем выбранные места в данные запроса
    var data = {
        selectedSeats: selectedSeats
    };

    var options = {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(data)
    };

    var url = `http://127.0.0.1:8000/${eventFilter}/${eventSlug}`;

    try {
        const response = await fetch(url, options);
        const responseData = await response.json();

    } catch (error) {
        console.error('Error:', error);
    }
}

var addToCartButton = document.getElementById('add-to-cart-btn');

addToCartButton.addEventListener('click', function () {
    // проверка доступности мест
    checkSeatAvailability(selectedSeats);
});


document.addEventListener("DOMContentLoaded", async function () {
    var seats = Array.from(document.querySelectorAll('.seat'));
    var bookedPlacesCache = null;

    async function getBookedPlaces() {
        try {
            const response = await fetch(`/api/get_booked_places/${eventFilter}/${eventSlug}`);
            if (!response.ok) {
                return;
            }
            
            const data = await response.json();
    
            bookedPlacesCache = data.booked_places;
    
            localStorage.setItem('bookedPlacesCache', JSON.stringify(bookedPlacesCache));
            return bookedPlacesCache;
        } catch (error) {
            console.error('Error:', error);
        }
    }
    
    async function checkSeatStatus(seat, dataSeat, dataRow) {
        if (!bookedPlacesCache) {
            await getBookedPlaces();
        }
       
        const placesArray = Array.isArray(bookedPlacesCache)
            ? bookedPlacesCache
            : (bookedPlacesCache && typeof bookedPlacesCache === 'object')
            ? Object.values(bookedPlacesCache)
            : [];


        if (placesArray.some(place => place.spot_num == dataSeat && place.spot_row == dataRow && place.available == false)) {
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
        await getBookedPlaces();

        const cachedData = localStorage.getItem('bookedPlacesCache');
        if (cachedData) {
            bookedPlacesCache = JSON.parse(cachedData);
            console.log(cachedData);
        } else {
            await getBookedPlaces();
        }

        const promises = seats.map(seat => {
            const dataSeat = seat.getAttribute('dataseat');
            const dataRow = seat.getAttribute('datarow');
            return checkSeatStatus(seat, dataSeat, dataRow);
        });

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