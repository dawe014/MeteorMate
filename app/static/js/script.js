document.addEventListener('DOMContentLoaded', function() {
    loadNavbar();
});

function loadNavbar() {
    fetch('../../templates/navbar.html')
        .then(response => response.text())
        .then(html => {
            document.getElementById('navbar-container').innerHTML = html;
            addDropdownEventListeners();
        })
        .catch(error => {
            console.error('Error fetching navbar:', error);
        });
}

function addDropdownEventListeners() {
    document.querySelectorAll('.dropdown-content a').forEach(item => {
        item.addEventListener('click', function() {
            const selectedUnit = this.getAttribute('data-unit');
            saveSettings(selectedUnit);
        });
    });
}

function saveSettings(selectedUnit) {
    fetch('/settings', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ units: selectedUnit })
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            alert('Settings saved!');
            getForecast();
        }
    })
    .catch(error => {
        console.error('Error saving settings:', error);
    });
}

function getForecast() {
    const location = document.getElementById('location').value;
    
    fetch(`/api/forecast?location=${location}`)
        .then(response => response.json())
        .then(data => {
            if (data.error) {
                displayError(data.error);
            } else {
                displayForecast(data);
            }
        })
        .catch(error => {
            displayError('Error fetching forecast data');
            console.error('Error fetching forecast data:', error);
        });
}

function displayError() {
    document.getElementById('current-weather-heading').innerHTML = `<h1 id="current-weather-heading">Weather Forecast</h1>`
    let ele = document.getElementById('forecast-data');
    ele.innerHTML = `<p>Error: Error fetching forecast data</p>`;
    alert(`Error: Error fetching forecast data `)
    ele.style.display = "NONE";
    
    for (let i = 1; i < 6; i++) {
        let element = document.getElementById(`day-${i}`);
        element.style.display = "none";
    }
      
}

function displayForecast(data) {
    const unit = data.unit === 'metric' ? '°C' : data.unit === 'imperial' ? '°F' : 'K';
    document.getElementById('current-weather-heading').innerHTML = `<h2>Weather Forecast for ${data.location}</h2>`;

    const dailyForecasts = getDailyForecasts(data.forecast);

    // Display the first day's forecast
    if (dailyForecasts.length > 0) {
        displaySingleDayForecast(dailyForecasts[0], 'forecast-data', unit);
        
    }

    // Display the rest of the days' forecasts
    for (let i = 1; i < dailyForecasts.length; i++) {
        displaySingleDayForecast(dailyForecasts[i], `day-${i}`, unit);
    }
}

function displaySingleDayForecast(day, elementId, unit) {
    const date = new Date(day.date);
    const dayName = new Intl.DateTimeFormat('en-US', { weekday: 'long' }).format(date);
    const forecastHtml = `
        <div class="data_display">
            <img src="https://openweathermap.org/img/wn/${day.icon}@2x.png" alt="${day.condition}">
            <h3>${dayName}</h3>
            <p>Temperature: ${day.temp}${unit}</p>
            <p>Pressure: ${day.pressure}</p>
            <p>Humidity: ${day.humidity}</p>
            <p>Condition: ${day.condition}</p>
        </div>
    `;
    let disp = document.getElementById(elementId);
    disp.innerHTML = forecastHtml;
    disp.style.backgroundColor = "rgba(0, 0, 0, 0.5)";
    
}

function getDailyForecasts(forecast) {
    const dailyForecasts = [];
    const uniqueDates = new Set();

    forecast.forEach(item => {
        const date = item.date.split(' ')[0]; // Extract the date part
        if (!uniqueDates.has(date)) {
            uniqueDates.add(date);
            dailyForecasts.push(item);
        }
    });

    return dailyForecasts;
}


/* -------- FOr setting-------*/

document.querySelectorAll('.dropdown-content a').forEach(item => {
    item.addEventListener('click', function() {
        const selectedUnit = this.getAttribute('data-unit');
        fetch('/settings', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ units: selectedUnit })
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                alert('Settings saved!');
            }
        });
    });
});

function showSidebar(){
    const sidebar = document.querySelector('.sidebar');
    sidebar.style.display='flex';
}
function closeSidebar(){
    const sidebar = document.querySelector('.sidebar');
    sidebar.style.display='none';
}