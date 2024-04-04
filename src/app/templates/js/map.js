// Map config
let config = {
  minZoom: 7,
  maxZoom: 18,
};
// Default map magnificaton
const zoom = 10;
// Default co-ordinates
const lat = 3.128099;
const lng = 101.678678;
const map = L.map("map", config).setView([lat, lng], zoom);

let catchment_radius = 5000; // 5km
let circles = [];

L.tileLayer("https://tile.openstreetmap.org/{z}/{x}/{y}.png", {
  attribution:
    '© <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors',
}).addTo(map);

function circlesOverlap(circle1, circle2) {
  var center1 = circle1.getLatLng();
  var center2 = circle2.getLatLng();
  var distance = center1.distanceTo(center2);

  return distance < 2 * catchment_radius;
}

$(document).ready(function () {
  $.getJSON("/get-data", function (data) {
    for (let i = 0; i < data.length; i++) {
      const lat = data[i].latitude;
      const lng = data[i].longitude;
      const popupText = data[i].name;

      // Adds markers to every point on the map
      marker = new L.marker([lat, lng]).bindPopup(popupText).addTo(map);

      // Adds catchment radius to every point on the map
      var circle = L.circle([lat, lng], {
        color: "red",
        fillColor: "#f03",
        fillOpacity: 0.1,
        radius: catchment_radius,
      }).addTo(map);

      circles.push(circle);
    }

    var overlappingCircles = [];

    for (var i = 0; i < circles.length; i++) {
      for (var j = i + 1; j < circles.length; j++) {
        if (circlesOverlap(circles[i], circles[j])) {
          if (!overlappingCircles.includes(circles[i])) {
            overlappingCircles.push(circles[i]);
          }
          if (!overlappingCircles.includes(circles[j])) {
            overlappingCircles.push(circles[j]);
          }
        }
      }
    }

    // Changing the color of overlapping circles to highlight them
    overlappingCircles.forEach((circle) => {
      circle.setStyle({
        color: "blue",
        fillColor: "#30f",
      });
    });
  });
});
