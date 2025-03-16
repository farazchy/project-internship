async function searchFlights() {
    let departure = document.getElementById("departure").value.toUpperCase();
    let destination = document.getElementById("destination").value.toUpperCase();

    if (!departure || !destination) {
        alert("Please enter both departure and destination airports.");
        return;
    }

    let response = await fetch("data/flights.json");
    let flights = await response.json();

    let results = flights.filter(flight =>
        flight.startingAirport === departure && flight.destinationAirport === destination
    );

    if (results.length > 0) {
        alert(`Found ${results.length} flights!`);
        updatePriceTrendChart(results);
        updateCheapestDaysChart(results);
        updateCheapestMonthsChart(results);
        updateAirlineComparisonChart(results);
        updateBestBookingLeadTimeChart(results); // Add the new chart
    } else {
        alert("No flights found.");
    }
}

// 📌 1. Price Trends Over Time (Line Chart)
function updatePriceTrendChart(flights) {
    let ctx = document.getElementById('priceTrendChart').getContext('2d');
    let pricesByDate = {};
    flights.forEach(flight => {
        let date = flight.flightDate;
        if (!pricesByDate[date]) pricesByDate[date] = [];
        pricesByDate[date].push(flight.totalFare);
    });

    let labels = Object.keys(pricesByDate).sort();
    let avgPrices = labels.map(date => {
        let fares = pricesByDate[date];
        return (fares.reduce((a, b) => a + b, 0) / fares.length).toFixed(2);
    });

    if (window.priceTrendChartInstance) {
        window.priceTrendChartInstance.destroy();
    }

    window.priceTrendChartInstance = new Chart(ctx, {
        type: 'line',
        data: {
            labels: labels,
            datasets: [{
                label: 'Average Fare ($)',
                data: avgPrices,
                borderColor: 'blue',
                backgroundColor: 'rgba(0, 0, 255, 0.1)',
                borderWidth: 2,
                fill: true,
                tension: 0.3,
                pointRadius: 4,
                pointBackgroundColor: 'blue'
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: true,
            aspectRatio: 2,
            plugins: {
                tooltip: {
                    callbacks: {
                        label: function(context) {
                            return `Date: ${context.label} | Avg Price: $${context.raw}`;
                        }
                    }
                }
            },
            scales: {
                x: {
                    title: {
                        display: true,
                        text: 'Flight Date',
                        font: { size: 14 }
                    },
                    ticks: {
                        autoSkip: true,
                        maxRotation: 30,
                        minRotation: 20
                    }
                },
                y: {
                    title: {
                        display: true,
                        text: 'Average Fare ($)',
                        font: { size: 14 }
                    },
                    beginAtZero: false
                }
            }
        }
    });
}

// 📌 5. Best Booking Lead Time (Bar Chart)
function updateBestBookingLeadTimeChart(flights) {
    let ctx = document.getElementById('bestBookingLeadTimeChart').getContext('2d');

    // Calculate lead time (difference in days between searchDate and flightDate)
    let leadTimes = flights.map(flight => {
        let searchDate = new Date(flight.searchDate);
        let flightDate = new Date(flight.flightDate);
        let timeDiff = flightDate - searchDate;  // Difference in milliseconds
        return Math.floor(timeDiff / (1000 * 3600 * 24));  // Convert to days
    });

    let labels = flights.map(flight => flight.flightDate);

    new Chart(ctx, {
        type: 'bar',
        data: {
            labels: labels,
            datasets: [{
                label: 'Booking Lead Time (Days)',
                data: leadTimes,
                backgroundColor: 'rgba(75, 192, 192, 0.2)',
                borderColor: 'rgba(75, 192, 192, 1)',
                borderWidth: 1
            }]
        },
        options: {
            responsive: true,
            plugins: {
                tooltip: {
                    callbacks: {
                        label: function(context) {
                            return `Lead Time: ${context.raw} days`;
                        }
                    }
                }
            },
            scales: {
                y: {
                    title: {
                        display: true,
                        text: 'Lead Time (Days)',
                        font: { size: 14 }
                    },
                    beginAtZero: true
                }
            }
        }
    });
}

// 📌 2. Cheapest Days to Fly (Bar Chart)
function updateCheapestDaysChart(flights) {
    let ctx = document.getElementById('cheapestDaysChart').getContext('2d');
    let days = ["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"];
    let pricesByDay = { Sunday: [], Monday: [], Tuesday: [], Wednesday: [], Thursday: [], Friday: [], Saturday: [] };

    flights.forEach(flight => {
        let day = days[new Date(flight.flightDate).getDay()];
        pricesByDay[day].push(flight.totalFare);
    });

    let avgPrices = days.map(day => {
        let fares = pricesByDay[day];
        return fares.length > 0 ? (fares.reduce((a, b) => a + b, 0) / fares.length).toFixed(2) : 0;
    });

    new Chart(ctx, {
        type: 'bar',
        data: { labels: days, datasets: [{ label: 'Average Fare ($)', data: avgPrices, backgroundColor: 'orange' }] }
    });
}

// 📌 3. Cheapest Months to Fly (Bar Chart)
function updateCheapestMonthsChart(flights) {
    let ctx = document.getElementById('cheapestMonthsChart').getContext('2d');
    let months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"];
    let pricesByMonth = {};

    flights.forEach(flight => {
        let month = months[new Date(flight.flightDate).getMonth()];
        if (!pricesByMonth[month]) pricesByMonth[month] = [];
        pricesByMonth[month].push(flight.totalFare);
    });

    let avgPrices = months.map(month => {
        let fares = pricesByMonth[month] || [];
        return fares.length > 0 ? (fares.reduce((a, b) => a + b, 0) / fares.length).toFixed(2) : 0;
    });

    new Chart(ctx, {
        type: 'bar',
        data: { labels: months, datasets: [{ label: 'Average Fare ($)', data: avgPrices, backgroundColor: 'green' }] }
    });
}

// 📌 4. Airline Price Comparison (Bar Chart)
function updateAirlineComparisonChart(flights) {
    let ctx = document.getElementById('airlineComparisonChart').getContext('2d');
    let airlines = {};

    flights.forEach(flight => {
        let airline = flight.segmentsAirlineName;
        if (!airlines[airline]) {
            airlines[airline] = { fares: [], totalFare: 0, count: 0 };
        }
        airlines[airline].fares.push(flight.totalFare);
        airlines[airline].totalFare += flight.totalFare;
        airlines[airline].count++;
    });

    let labels = Object.keys(airlines);
    let avgPrices = labels.map(airline => {
        let data = airlines[airline];
        return (data.totalFare / data.count).toFixed(2);
    });

    new Chart(ctx, {
        type: 'bar',
        data: {
            labels: labels,
            datasets: [{
                label: 'Average Fare ($)',
                data: avgPrices,
                backgroundColor: 'purple'
            }]
        },
        options: {
            responsive: true,
            plugins: {
                tooltip: {
                    callbacks: {
                        label: function(context) {
                            let airline = labels[context.dataIndex];
                            let fares = airlines[airline].fares;

                            let minFare = Math.min(...fares);
                            let maxFare = Math.max(...fares);
                            let avgFare = (fares.reduce((a, b) => a + b, 0) / fares.length).toFixed(2);

                            return [
                                `Airline: ${airline}`,
                                `Avg Fare: $${avgFare}`,
                                `Min Fare: $${minFare}`,
                                `Max Fare: $${maxFare}`
                            ];
                        }
                    }
                }
            },
            scales: { y: { beginAtZero: true } }
        }
    });
}