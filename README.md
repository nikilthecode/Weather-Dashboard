# 🌦️ Weather Dashboard

A responsive weather dashboard built with Flask and the OpenWeather API. The application allows users to search for a city and view current weather conditions along with a multi-day forecast.

🔗 **Live Demo:** https://weather-dashboard-1-witx.onrender.com

---

## 📌 Overview

The Weather Dashboard is a full-stack web application developed with Python and Flask.

Users can search for a city and retrieve real-time weather information through the OpenWeather API. The application also supports browser-based location detection and provides forecast information in a simple, responsive interface.

The project was developed incrementally, tested locally, version-controlled with Git, and deployed to Render using Gunicorn.

---

## ✨ Features

- 🔎 Search weather by city name
- 📍 Detect weather using the user's current location
- 🌡️ Display current temperature
- 💧 Display humidity information
- 💨 Display wind information
- 🌤️ Display weather conditions
- 📅 View upcoming weather forecast
- ⏳ Loading state while weather data is retrieved
- ⚠️ Handles API and request errors
- 📱 Responsive web interface
- 🔐 API key stored securely using environment variables
- ☁️ Deployed online using Render

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
├── requirements.txt
└── README.md