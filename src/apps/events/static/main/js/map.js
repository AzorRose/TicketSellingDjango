function init() {
    let map = new ymaps.Map('map', {
        center: [46.32980857304796,48.05038341628097],
        zoom: 17
    });
    var myPlacemark = new ymaps.Placemark([46.329608724353555,48.05026378735787],
    );
    map.geoObjects.add(myPlacemark);
    map.controls.remove('geolocationControl'); // удаляем геолокацию
    map.controls.remove('searchControl'); // удаляем поиск
    map.controls.remove('trafficControl'); // удаляем контроль трафика
    map.controls.remove('typeSelector'); // удаляем тип
    map.controls.remove('fullscreenControl'); // удаляем кнопку перехода в полноэкранный режим
    map.controls.remove('rulerControl'); // удаляем контрол правил
    map.behaviors.disable(['scrollZoom']); // отключаем скролл карты (опционально)
}

ymaps.ready(init);