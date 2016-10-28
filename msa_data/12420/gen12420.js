var map = L.map('map').setView([35.9908385, -78.9005222], 3);

var OpenStreetMap_Mapnik = L.tileLayer('http://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
	maxZoom: 19,
	attribution: '&copy; <a href="http://www.openstreetmap.org/copyright">OpenStreetMap</a>'
}).addTo(map);

//var myStyle = {
//    "color": "#000066",
//    "weight": 1,
//    "fillOpacity": 0.7,
//    "opacity": .9
//};

function addDataToMap(data, map) {
    var dataLayer = L.geoJson(data, {style: function(feature) 
    	{return {color: feature.properties.stroke, 
    			 fillColor: feature.properties.fill,
    			 weight: 1,
    			 fillOpacity: 0.7}}});
    dataLayer.addTo(map);
}

$.getJSON("geoJSON/12420_tract.geojson", function(data) { addDataToMap(data, map); });

var myIcon = L.icon({
    iconSize: [20, 20],
    iconAnchor: [10, 10],
    labelAnchor: [6, 0] // as I want the label to appear 2px past the icon (10 + 2 - 6)
});

L.marker([30.2672, -97.7431], {opacity: 0.01, icon:myIcon}).bindTooltip('Label here', {noHide: true, direction: 'auto'}).addTo(map);