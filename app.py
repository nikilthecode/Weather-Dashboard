from flask import Flask, render_template, request
import requests
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

API_KEY = os.getenv("OPENWEATHER_API_KEY")

CURRENT_WEATHER_URL = "https://api.openweathermap.org/data/2.5/weather"
FORECAST_URL = "https://api.openweathermap.org/data/2.5/forecast"


def get_forecast_days(forecast_data):
    """Select one forecast entry for each day."""
    forecast_days = []
    selected_dates = set()

    for item in forecast_data.get("list", []):
        date = item["dt_txt"].split(" ")[0]

        if date not in selected_dates:
            forecast_days.append(item)
            selected_dates.add(date)

        if len(forecast_days) == 5:
            break

    return forecast_days


def get_weather_data(params):
    """Fetch current weather and forecast data."""
    current_response = requests.get(
        CURRENT_WEATHER_URL,
        params=params,
        timeout=10
    )

    if current_response.status_code == 404:
        return None, None, "City not found. Please check the city name."

    if current_response.status_code == 401:
        return None, None, "Weather API authentication failed."

    if current_response.status_code == 429:
        return None, None, "Weather service rate limit reached. Please try again later."

    if current_response.status_code != 200:
        print(
            "OpenWeather status:",
            current_response.status_code
        )
        print(
            "OpenWeather response:",
            current_response.text
        )

        return (
            None,
            None,
            "Weather service is currently unavailable."
        )

    weather = current_response.json()

    forecast_response = requests.get(
        FORECAST_URL,
        params=params,
        timeout=10
    )

    if forecast_response.status_code == 401:
        return None, None, "Weather API authentication failed."

    if forecast_response.status_code == 429:
        return (
            None,
            None,
            "Weather service rate limit reached. Please try again later."
        )

    if forecast_response.status_code != 200:
        print(
            "Forecast API status:",
            forecast_response.status_code
        )
        print(
            "Forecast API response:",
            forecast_response.text
        )

        return (
            weather,
            None,
            "Forecast data is currently unavailable."
        )

    forecast = forecast_response.json()

    return weather, forecast, None


@app.route("/", methods=["GET", "POST"])
def home():
    weather = None
    forecast = None
    forecast_days = []
    error = None

    if request.method == "POST":
        city = request.form.get("city", "").strip()

        if not city:
            error = "Please enter a city name."

        elif not API_KEY:
            error = "Weather API key is not configured."

        else:
            params = {
                "q": city,
                "appid": API_KEY,
                "units": "metric"
            }

            try:
                weather, forecast, error = get_weather_data(params)

                if forecast:
                    forecast_days = get_forecast_days(forecast)

            except requests.Timeout:
                error = "The weather service took too long to respond."

            except requests.ConnectionError:
                error = "Could not connect to the weather service."

            except requests.RequestException as e:
                print("Weather request error:", e)
                error = "Could not retrieve weather data."

    return render_template(
        "index.html",
        weather=weather,
        forecast=forecast,
        forecast_days=forecast_days,
        error=error
    )


@app.route("/weather-by-location", methods=["POST"])
def weather_by_location():
    data = request.get_json(silent=True)

    if not data:
        return {
            "error": "Location data is required."
        }, 400

    latitude = data.get("latitude")
    longitude = data.get("longitude")

    if latitude is None or longitude is None:
        return {
            "error": "Latitude and longitude are required."
        }, 400

    if not API_KEY:
        return {
            "error": "Weather API key is not configured."
        }, 500

    params = {
        "lat": latitude,
        "lon": longitude,
        "appid": API_KEY,
        "units": "metric"
    }

    try:
        weather, forecast, error = get_weather_data(params)

        if error:
            return {
                "error": error
            }, 502

        forecast_days = get_forecast_days(forecast)

        return {
            "weather": weather,
            "forecast_days": forecast_days
        }

    except requests.Timeout:
        return {
            "error": "The weather service took too long to respond."
        }, 504

    except requests.ConnectionError:
        return {
            "error": "Could not connect to the weather service."
        }, 503

    except requests.RequestException as e:
        print("Location weather request error:", e)

        return {
            "error": "Could not retrieve weather data."
        }, 500


if __name__ == "__main__":
    app.run(debug=True)