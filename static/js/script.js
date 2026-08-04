
const weatherForm = document.getElementById("weather-form");
const loadingMessage = document.getElementById("loading-message");

function showLoading() {
    if (loadingMessage) {
        loadingMessage.hidden = false;
    }
}

function hideLoading() {
    if (loadingMessage) {
        loadingMessage.hidden = true;
    }
}

if (weatherForm) {
    weatherForm.addEventListener("submit", function () {
        showLoading();
    });
}


const locationButton = document.getElementById("location-btn");


if (locationButton) {
    locationButton.addEventListener("click", function () {
        if (!navigator.geolocation) {
            alert("Geolocation is not supported by your browser.");
            return;
        }

        showLoading();

        locationButton.textContent = "📍 Getting Location...";
        locationButton.disabled = true;

        navigator.geolocation.getCurrentPosition(
            handleLocationSuccess,
            handleLocationError
        );
    });
}


function handleLocationSuccess(position) {
    const latitude = position.coords.latitude;
    const longitude = position.coords.longitude;

    fetch("/weather-by-location", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({
            latitude: latitude,
            longitude: longitude
        })
    })
        .then(response => {
            return response.json().then(data => ({
                ok: response.ok,
                data: data
            }));
        })
        .then(result => {
            if (!result.ok) {
                alert(
                    result.data.error ||
                    "Could not retrieve weather data."
                );
                return;
            }

            if (result.data.error) {
                alert(result.data.error);
                return;
            }

            updateWeatherDisplay(result.data.weather);
            updateForecastDisplay(result.data.forecast_days);
        })
        .catch(error => {
            console.error("Location weather error:", error);
            alert("Could not retrieve weather for your location.");
        })
        .finally(() => {
            hideLoading();

            locationButton.textContent = "📍 Use My Location";
            locationButton.disabled = false;
        });
}


function handleLocationError(error) {
    let message = "Unable to get your location.";

    if (error.code === error.PERMISSION_DENIED) {
        message = "Location permission was denied.";
    } else if (error.code === error.POSITION_UNAVAILABLE) {
        message = "Your location is currently unavailable.";
    } else if (error.code === error.TIMEOUT) {
        message = "Location request timed out.";
    }

    alert(message);

    hideLoading();

    locationButton.textContent = "📍 Use My Location";
    locationButton.disabled = false;
}


function updateWeatherDisplay(data) {
    const cityName = document.getElementById("city-name");
    const description = document.getElementById("weather-description");
    const temperature = document.getElementById("temperature");
    const feelsLike = document.getElementById("feels-like");
    const humidity = document.getElementById("humidity");
    const windSpeed = document.getElementById("wind-speed");
    const visibility = document.getElementById("visibility");
    const weatherIcon = document.querySelector(".weather-icon");

    cityName.textContent = `${data.name}, ${data.sys.country}`;

    description.textContent =
        data.weather[0].description.charAt(0).toUpperCase() +
        data.weather[0].description.slice(1);

    temperature.textContent = Math.round(data.main.temp);

    feelsLike.textContent =
        `${Math.round(data.main.feels_like)}°C`;

    humidity.textContent =
        `${data.main.humidity}%`;

    windSpeed.textContent =
        `${(data.wind.speed * 3.6).toFixed(1)} km/h`;

    visibility.textContent =
        `${(data.visibility / 1000).toFixed(1)} km`;

    weatherIcon.innerHTML = `
        <img
            src="https://openweathermap.org/img/wn/${data.weather[0].icon}@2x.png"
            alt="${data.weather[0].description}"
        >
    `;
}


function updateForecastDisplay(forecastDays) {
    const forecastContainer =
        document.getElementById("forecast-container");

    if (!forecastContainer) {
        return;
    }

    forecastContainer.innerHTML = "";

    if (!Array.isArray(forecastDays) || forecastDays.length === 0) {
        forecastContainer.innerHTML = `
            <div class="forecast-card">
                <h3>Forecast Unavailable</h3>

                <div class="forecast-icon">
                    🌤️
                </div>

                <p>--°C</p>

                <small>
                    Forecast data is currently unavailable.
                </small>
            </div>
        `;

        return;
    }

    forecastDays.forEach(item => {
        const date = new Date(item.dt_txt);

        const formattedDate = date.toLocaleDateString("en-US", {
            month: "short",
            day: "numeric"
        });

        const description = item.weather[0].description;

        const capitalizedDescription =
            description.charAt(0).toUpperCase() +
            description.slice(1);

        const temperature = Math.round(item.main.temp);

        const icon = item.weather[0].icon;

        const forecastCard = document.createElement("div");
        forecastCard.className = "forecast-card";

        forecastCard.innerHTML = `
            <h3>${formattedDate}</h3>

            <img
                src="https://openweathermap.org/img/wn/${icon}@2x.png"
                alt="${description}"
            >

            <p>${temperature}°C</p>

            <small>${capitalizedDescription}</small>
        `;

        forecastContainer.appendChild(forecastCard);
    });
}