# 🌦️ Weather Dashboard

A responsive weather dashboard built with Flask and the OpenWeather API. The application allows users to search for a city and view current weather conditions along with a multi-day forecast.

🔗 **Live Demo:** https://weather-dashboard-1-witx.onrender.com

---

## 📌 Overview

The Weather Dashboard is a full-stack web application developed using Python and Flask.

Users can search for a city and retrieve real-time weather information through the OpenWeather API. The application also supports browser-based location detection and provides forecast information through a simple and responsive interface.

The project was developed incrementally, tested locally, version-controlled with Git and GitHub, and deployed to Render using Gunicorn.

---

## ✨ Features

- 🔎 Search weather by city name
- 📍 Get weather using the user's current location
- 🌡️ Display current temperature
- 🌤️ Display current weather conditions
- 💧 Display humidity
- 💨 Display wind information
- 📅 Display upcoming weather forecast
- ⏳ Loading state while weather data is retrieved
- ⚠️ Handles API and request errors
- 📱 Responsive web interface
- 🔐 API key protected using environment variables
- ☁️ Deployed and accessible online through Render

---

## 📸 Screenshots

### Dashboard

![Weather Dashboard](screenshots/dashboard.png)

### Weather Search Result and Forecast

![Weather Search Result](screenshots/weather-result.png)

---

## 🛠️ Technologies Used

### Backend

- Python
- Flask
- Requests
- python-dotenv
- Gunicorn

### Frontend

- HTML5
- CSS3
- JavaScript

### API

- OpenWeather API

### Development & Deployment

- Git
- GitHub
- Render

---

## 🏗️ Project Structure

```text
Weather-Dashboard/
│
├── screenshots/
│   ├── dashboard.png
│   └── weather-result.png
│
├── static/
│   ├── css/
│   │   └── style.css
│   └── js/
│       └── script.js
│
├── templates/
│   └── index.html
│
├── .gitignore
├── app.py
├── README.md
└── requirements.txt
