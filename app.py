from flask import Flask, render_template, request
import requests
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

API_KEY = os.getenv("OPENWEATHER_API_KEY")

CURRENT_WEATHER_URL = "https://api.openweathermap.org/data/2.5/weather"
FORECAST_URL = "https://api.openweathermap.org/data/2.5/forecast"


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

        else:
            current_params = {
                "q": city,
                "appid": API_KEY,
                "units": "metric"
            }

            forecast_params = {
                "q": city,
                "appid": API_KEY,
                "units": "metric"
            }

            try:
                current_response = requests.get(
                    CURRENT_WEATHER_URL,
                    params=current_params,
                    timeout=10
                )

                forecast_response = requests.get(
                    FORECAST_URL,
                    params=forecast_params,
                    timeout=10
                )

                if current_response.status_code == 200:
                    weather = current_response.json()

                    if forecast_response.status_code == 200:
                        forecast = forecast_response.json()

                        selected_dates = set()

                        for item in forecast["list"]:
                            date = item["dt_txt"].split(" ")[0]

                            if date not in selected_dates:
                                forecast_days.append(item)
                                selected_dates.add(date)

                            if len(forecast_days) == 5:
                                break

                    else:
                        print(
                            "Forecast API error:",
                            forecast_response.status_code
                        )

                        if forecast_response.status_code == 401:
                            error = "Weather API authentication failed."
                        elif forecast_response.status_code >= 500:
                            error = "Weather service is temporarily unavailable."
                        else:
                            error = "Could not retrieve the weather forecast."

                elif current_response.status_code == 404:
                    error = "City not found. Please check the city name."

                elif current_response.status_code == 401:
                    error = "Weather API authentication failed."

                elif current_response.status_code >= 500:
                    error = "Weather service is temporarily unavailable."

                else:
                    print(
                        "OpenWeather status:",
                        current_response.status_code
                    )

                    print(
                        "OpenWeather response:",
                        current_response.text
                    )

                    error = "Unable to retrieve weather information."

            except requests.Timeout:
                print("Weather request timed out.")
                error = "The weather service took too long to respond."

            except requests.ConnectionError:
                print("Could not connect to the weather service.")
                error = "Could not connect to the weather service."

            except requests.RequestException as e:
                print("Weather request error:", e)
                error = "Something went wrong while retrieving weather data."

    return render_template(
        "index.html",
        weather=weather,
        forecast=forecast,
        forecast_days=forecast_days,
        error=error
    )


@app.route("/weather-by-location", methods=["POST"])
def weather_by_location():
    data = request.get_json()

    if not data:
        return {"error": "Location data is required."}, 400

    latitude = data.get("latitude")
    longitude = data.get("longitude")

    if latitude is None or longitude is None:
        return {"error": "Latitude and longitude are required."}, 400

    try:
        latitude = float(latitude)
        longitude = float(longitude)

    except (TypeError, ValueError):
        return {
            "error": "Invalid location coordinates."
        }, 400

    if not (-90 <= latitude <= 90):
        return {
            "error": "Invalid latitude value."
        }, 400

    if not (-180 <= longitude <= 180):
        return {
            "error": "Invalid longitude value."
        }, 400

    params = {
        "lat": latitude,
        "lon": longitude,
        "appid": API_KEY,
        "units": "metric"
    }

    try:
        current_response = requests.get(
            CURRENT_WEATHER_URL,
            params=params,
            timeout=10
        )

        forecast_response = requests.get(
            FORECAST_URL,
            params=params,
            timeout=10
        )

        if current_response.status_code == 401:
            return {
                "error": "Weather API authentication failed."
            }, 401

        if current_response.status_code != 200:
            return {
                "error": "Could not retrieve current weather."
            }, current_response.status_code

        if forecast_response.status_code == 401:
            return {
                "error": "Weather API authentication failed."
            }, 401

        if forecast_response.status_code != 200:
            return {
                "error": "Could not retrieve weather forecast."
            }, forecast_response.status_code

        weather = current_response.json()
        forecast = forecast_response.json()

        forecast_days = []
        selected_dates = set()

        for item in forecast["list"]:
            date = item["dt_txt"].split(" ")[0]

            if date not in selected_dates:
                forecast_days.append(item)
                selected_dates.add(date)

            if len(forecast_days) == 5:
                break

        return {
            "weather": weather,
            "forecast_days": forecast_days
        }

    except requests.Timeout:
        print("Location weather request timed out.")

        return {
            "error": "The weather service took too long to respond."
        }, 504

    except requests.ConnectionError:
        print("Location weather connection failed.")

        return {
            "error": "Could not connect to the weather service."
        }, 503

    except requests.RequestException as e:
        print("Location weather request error:", e)

        return {
            "error": "Something went wrong while retrieving weather data."
        }, 500


if __name__ == "__main__":
    app.run(debug=True)