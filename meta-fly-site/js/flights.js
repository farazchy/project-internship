async function searchFlights() {
    let departure = document.getElementById("departure").value.toUpperCase();
    let destination = document.getElementById("destination").value.toUpperCase();

    if (!departure || !destination) {
        alert("Please enter both departure and destination airports.");
        return;
    }

    let response = await fetch("../data/flights.json");
    let flights = await response.json();

    // Filter flights by departure and destination
    let results = flights.filter(flight =>
        flight.startingAirport === departure && flight.destinationAirport === destination
    );

    if (results.length > 0) {
        alert(`Found ${results.length} flights!`);
        updateMap(results);
        updateChart(results);
        updateWhenToFlyChart(results);
    } else {
        alert("No flights found.");
    }
}
