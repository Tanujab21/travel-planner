# AI Travel Planner ✈️🌍

An AI-powered travel planning web application built with **Flask**, **Bootstrap 5**, **SQLite**, **OpenWeatherMap API**, **OpenStreetMap Nominatim**, and **Ollama (Llama 3.2)**.

The application generates personalized travel plans based on the user's **budget**, **destination**, and **trip duration**. It automatically fetches weather information, optionally validates destinations using geocoding services, and uses AI to create a complete travel itinerary.

---

## Features

### 🌤 Weather Integration

* Fetches current weather information using OpenWeatherMap API.
* Includes weather details in AI-generated travel recommendations.
* Gracefully falls back to seasonal assumptions if the API is unavailable.

### 📍 Destination Validation

* Uses OpenStreetMap Nominatim API to verify destinations.
* Retrieves nearby points of interest when available.

### 🤖 AI-Powered Travel Planning

Generates:

#### 1. Day-by-Day Itinerary

* Suggested activities for each day
* Local attractions
* Food recommendations
* Budget-conscious planning

#### 2. Weather-Based Packing List

* Clothing recommendations
* Travel essentials
* Weather-specific items

#### 3. Hotel Inquiry Email

* Professional hotel reservation inquiry
* Polite and customizable template

### 💾 Trip History

* Stores every generated travel plan in SQLite.
* View previous trips.
* Click a previous trip to automatically refill the form.
* Easily regenerate and compare plans.

### 🎨 Modern UI

* Responsive Bootstrap 5 interface
* Tabbed result sections
* Mobile-friendly design

---

## Tech Stack

### Backend

* Flask
* SQLite3
* Requests

### Frontend

* HTML5
* Bootstrap 5
* JavaScript

### AI Model

* Ollama
* llama3.2:latest

### APIs

* OpenWeatherMap API
* OpenStreetMap Nominatim API

---

## Project Structure

```text
AI-Travel-Planner/
│
├── app.py
├── db.sqlite
├── requirements.txt
├── README.md
│
├── templates/
│   └── index.html
│
├── static/
│   ├── css/
│   └── js/
│
└── screenshots/
```

---

## Database Schema

### trips

| Column          | Type                |
| --------------- | ------------------- |
| id              | INTEGER PRIMARY KEY |
| destination     | TEXT                |
| budget          | TEXT                |
| days            | INTEGER             |
| weather_summary | TEXT                |
| itinerary       | TEXT                |
| packing_list    | TEXT                |
| hotel_email     | TEXT                |
| created_at      | TIMESTAMP           |

---

## Installation

### 1. Clone Repository

```bash
git clone https://github.com/yourusername/AI-Travel-Planner.git
cd AI-Travel-Planner
```

### 2. Create Virtual Environment

```bash
python -m venv venv
```

Activate:

Windows

```bash
venv\Scripts\activate
```

Linux/Mac

```bash
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

---

## Install Ollama

Download and install Ollama:

https://ollama.com

Pull the model:

```bash
ollama pull llama3.2:latest
```

Start Ollama:

```bash
ollama serve
```

Verify:

```bash
ollama list
```

---

## Configure API Keys

Create a `.env` file:

```env
OPENWEATHER_API_KEY=your_api_key_here
```

Get your API key from:

https://openweathermap.org/api

---

## Run Application

```bash
python app.py
```

Open:

```text
http://127.0.0.1:5000
```

---

## AI Prompt Flow

The application combines:

* User Budget
* Destination
* Number of Days
* Current Weather
* Nearby Attractions

into a single prompt:

```text
Create:
1. Day-by-day itinerary
2. Packing list
3. Hotel inquiry email

Destination: Paris
Budget: ₹50,000
Days: 5

Weather:
18°C, light rain

Nearby Attractions:
Eiffel Tower
Louvre Museum
Notre Dame

Generate detailed travel recommendations.
```

The prompt is sent to:

```text
http://localhost:11434/api/generate
```

using:

```json
{
  "model": "llama3.2:latest",
  "prompt": "..."
}
```

---

## Error Handling

The application handles:

* Weather API failures
* Geocoding API failures
* Ollama connection issues
* Invalid destinations
* Missing user input

Fallback travel suggestions are generated using seasonal assumptions.

---

## Future Enhancements

* Google Maps Integration
* PDF Export
* Budget Breakdown Charts
* Multi-City Trips
* Flight Recommendations
* Hotel Search APIs
* User Authentication
* Trip Sharing

---

## Screenshots

Add screenshots inside the `screenshots/` folder.

Example:

```markdown
![Home Page](screenshots/home.png)

![Generated Plan](screenshots/result.png)
```

---

## Requirements

```text
Flask
requests
python-dotenv
sqlite3
```

Generate automatically:

```bash
pip freeze > requirements.txt
```

---

## Author

Snehal Pisale

BCA Final Year Project / AI Application Development

---

## License

This project is licensed under the MIT License.

Feel free to use and modify for educational and personal projects.
