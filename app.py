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

                        # Select one forecast entry for each day
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

                elif current_response.status_code == 404:
                    error = "City not found. Please check the city name."

                elif current_response.status_code == 401:
                    error = "Weather API authentication failed."

                else:
                    print(
                        "OpenWeather status:",
                        current_response.status_code
                    )

                    print(
                        "OpenWeather response:",
                        current_response.text
                    )

                    error = (
                        f"Weather service error: "
                        f"{current_response.status_code}"
                    )

            except requests.RequestException as e:
                print("Connection error:", e)
                error = "Could not connect to the weather service."

    return render_template(
        "index.html",
        weather=weather,
        forecast=forecast,
        forecast_days=forecast_days,
        error=error
    )


if __name__ == "__main__":
    app.run(debug=True)