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

seats.forEach(seat => {

    let defaultColor = seat.style.fill;

    seat.addEventListener('click', () => {
        if(seat.style.fill === defaultColor) {
        seat.style.fill = 'red';
        } else {
        seat.style.fill = defaultColor;
        }
    });

    seat.addEventListener('mouseover', () => {
        seat.style.filter = 'drop-shadow(0 0 3px #666)';
    });
    
    seat.addEventListener('mouseout', () => {
        seat.style.filter = 'none';
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