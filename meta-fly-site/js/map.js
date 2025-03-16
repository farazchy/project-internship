let map = L.map('map').setView([42.3601, -71.0589], 5); // Default to Boston

L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    attribution: '&copy; OpenStreetMap contributors'
}).addTo(map);

const airportCoordinates = {
    "BOS": [42.3656, -71.0096], // Boston Logan
    "LGA": [40.7769, -73.8740], // LaGuardia
    "JFK": [40.6413, -73.7781], // John F. Kennedy
    "ORD": [41.9742, -87.9073], // Chicago O'Hare
    "MIA": [25.7959, -80.2870], // Miami International
    "SFO": [37.7749, -122.4194], // San Francisco
    "LAX": [33.9416, -118.4085], // Los Angeles
    "DFW": [32.8998, -97.0403], // Dallas Fort Worth
    "ATL": [33.6407, -84.4277], // Atlanta Hartsfield
    "DEN": [39.8561, -104.6737] // Denver International
};

let blueIcon = new L.Icon({
    iconUrl: 'https://raw.githubusercontent.com/pointhi/leaflet-color-markers/master/img/marker-icon-blue.png',
    shadowUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/0.7.7/images/marker-shadow.png',
    iconSize: [25, 41],
    iconAnchor: [12, 41],
    popupAnchor: [1, -34],
    shadowSize: [41, 41]
});

let redIcon = new L.Icon({
    iconUrl: 'https://raw.githubusercontent.com/pointhi/leaflet-color-markers/master/img/marker-icon-red.png',
    shadowUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/0.7.7/images/marker-shadow.png',
    iconSize: [25, 41],
    iconAnchor: [12, 41],
    popupAnchor: [1, -34],
    shadowSize: [41, 41]
});


function updateMap(flights) {
    map.eachLayer(layer => {
        if (layer instanceof L.Marker || layer instanceof L.Polyline) {
            map.removeLayer(layer);
        }
    });

    let cheapestFlights = {};

    flights.forEach(flight => {
        let dest = flight.destinationAirport;
        if (!cheapestFlights[dest] || flight.totalFare < cheapestFlights[dest].totalFare) {
            cheapestFlights[dest] = flight;
        }
    });

    Object.values(cheapestFlights).forEach(flight => {
        let departureCoords = airportCoordinates[flight.startingAirport];
        let destCoords = airportCoordinates[flight.destinationAirport];

        if (departureCoords && destCoords) {
            // Add departure marker
            L.marker(departureCoords, { icon: blueIcon })
                .addTo(map)
                .bindPopup(`<b>Departure: ${flight.startingAirport}</b><br>Time: ${flight.segmentsDepartureTimeRaw}`)
                .openPopup();

            // Add destination marker
            L.marker(destCoords, { icon: redIcon })
                .addTo(map)
                .bindPopup(`<b>Destination: ${flight.destinationAirport}</b><br>Fare: $${flight.totalFare}<br>Duration: ${flight.travelDuration}`)
                .openPopup();

            // Draw a line from departure to destination
            L.polyline([departureCoords, destCoords], { color: 'blue' }).addTo(map);
        } else {
            console.warn(`Missing coordinates for: ${flight.startingAirport} or ${flight.destinationAirport}`);
        }
    });
}

