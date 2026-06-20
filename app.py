from flask import Flask, render_template, request
import sqlite3
import requests
from datetime import datetime

app = Flask(__name__)

DB_NAME = "db.sqlite"

# =========================
# DATABASE
# =========================

def init_db():
    conn = sqlite3.connect(DB_NAME)

    conn.execute("""
    CREATE TABLE IF NOT EXISTS trips (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        destination TEXT,
        budget TEXT,
        days INTEGER,
        weather_summary TEXT,
        itinerary TEXT,
        packing_list TEXT,
        hotel_email TEXT,
        created_at TEXT
    )
    """)

    conn.commit()
    conn.close()

init_db()

# =========================
# WEATHER
# =========================

OPENWEATHER_API_KEY = "YOUR_OPENWEATHER_API_KEY"


def get_weather(destination):
    try:
        url = (
            f"https://api.openweathermap.org/data/2.5/weather"
            f"?q={destination}&appid={OPENWEATHER_API_KEY}&units=metric"
        )

        r = requests.get(url, timeout=10)

        if r.status_code == 200:
            data = r.json()

            desc = data["weather"][0]["description"]
            temp = data["main"]["temp"]

            return f"{desc}, {temp}°C"

    except Exception:
        pass

    return "Weather unavailable. Assume moderate seasonal conditions."


# =========================
# GEOCODING + POI
# =========================

def get_location_info(destination):
    try:
        headers = {
            "User-Agent": "TravelPlanner/1.0"
        }

        geo_url = (
            f"https://nominatim.openstreetmap.org/search"
            f"?q={destination}&format=json&limit=1"
        )

        r = requests.get(
            geo_url,
            headers=headers,
            timeout=10
        )

        results = r.json()

        if results:
            return results[0]["display_name"]

    except Exception:
        pass

    return destination


# =========================
# OLLAMA
# =========================

def generate_trip_plan(destination, budget, days, weather):

    prompt = f"""
You are an expert travel planner.

Destination: {destination}
Budget: {budget}
Days: {days}
Weather: {weather}

Generate:

SECTION 1:
DAY-BY-DAY ITINERARY

SECTION 2:
WEATHER APPROPRIATE PACKING LIST

SECTION 3:
POLITE HOTEL INQUIRY EMAIL

Format exactly:

===ITINERARY===
...

===PACKING===
...

===EMAIL===
...
"""

    try:

        response = requests.post(
            "http://localhost:11434/api/generate",
            json={
                "model": "llama3.2:latest",
                "prompt": prompt,
                "stream": False
            },
            timeout=180
        )

        result = response.json()

        text = result.get("response", "")

        itinerary = ""
        packing = ""
        email = ""

        if "===ITINERARY===" in text:
            parts = text.split("===ITINERARY===")[1]

            if "===PACKING===" in parts:
                itinerary, rest = parts.split(
                    "===PACKING===",
                    1
                )

                if "===EMAIL===" in rest:
                    packing, email = rest.split(
                        "===EMAIL===",
                        1
                    )

        return (
            itinerary.strip(),
            packing.strip(),
            email.strip()
        )

    except Exception as e:

        return (
            f"Unable to generate itinerary. {e}",
            "No packing list available.",
            "No hotel email available."
        )


# =========================
# ROUTES
# =========================

@app.route("/")
def home():

    conn = sqlite3.connect(DB_NAME)

    conn.row_factory = sqlite3.Row

    trips = conn.execute("""
        SELECT *
        FROM trips
        ORDER BY id DESC
    """).fetchall()

    conn.close()

    return render_template(
        "index.html",
        trips=trips
    )


@app.route("/plan", methods=["POST"])
def plan():

    destination = request.form["destination"]
    budget = request.form["budget"]
    days = request.form["days"]

    verified_destination = get_location_info(destination)

    weather_summary = get_weather(destination)

    itinerary, packing_list, hotel_email = generate_trip_plan(
        verified_destination,
        budget,
        days,
        weather_summary
    )

    conn = sqlite3.connect(DB_NAME)

    conn.execute("""
    INSERT INTO trips
    (
        destination,
        budget,
        days,
        weather_summary,
        itinerary,
        packing_list,
        hotel_email,
        created_at
    )
    VALUES (?,?,?,?,?,?,?,?)
    """,
    (
        destination,
        budget,
        days,
        weather_summary,
        itinerary,
        packing_list,
        hotel_email,
        datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    ))

    conn.commit()

    conn.row_factory = sqlite3.Row

    trips = conn.execute("""
    SELECT *
    FROM trips
    ORDER BY id DESC
    """).fetchall()

    conn.close()

    return render_template(
        "index.html",
        trips=trips,
        itinerary=itinerary,
        packing_list=packing_list,
        hotel_email=hotel_email,
        weather_summary=weather_summary,
        destination=destination,
        budget=budget,
        days=days
    )


if __name__ == "__main__":
    app.run(debug=True)