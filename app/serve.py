from fastapi import FastAPI
from dataclasses import dataclass
import sqlite3
import requests
import time
import threading
import uvicorn
from datetime import datetime
from xml.sax.saxutils import escape
from fastapi.responses import FileResponse
import pygal
from dotenv import load_dotenv
import os

from config import config

@dataclass
class MoistureDto():
    plant: str
    moisture: float

@dataclass
class Moisture():
    plant: str
    moisture: float
    date: str

def initialize_db(path_to_db: str):
    """Create table if not exists."""
    conn = sqlite3.connect(path_to_db)
    try:
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS moisture ( id INTEGER PRIMARY KEY AUTOINCREMENT, plant TEXT, moisture REAL, timestamp DATETIME DEFAULT CURRENT_TIMESTAMP)
        ''')
        conn.commit()
    finally:
        conn.close()

def get_stored_moisture(last_n: int = 0) -> list[Moisture]:
    conn = sqlite3.connect(config.DB_FILE)
    results = []
    try:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT
                timestamp,
                plant,
                moisture
            FROM
                moisture
            ORDER BY
                id DESC
            LIMIT (?)
        """, (last_n,))
        results = cursor.fetchall()
    finally:
        conn.close()

    return [Moisture(plant, moisture, date) for [date, plant, moisture] in results]

def store(moisture: MoistureDto):
    try:
        conn = sqlite3.connect(config.DB_FILE)
        try:
            cursor = conn.cursor()
            cursor.execute("INSERT INTO moisture (plant,moisture) VALUES (?, ?)", (moisture.plant,moisture.moisture))
            conn.commit()
        finally:
            conn.close()
        # print(f"Data stored at {time.strftime('%Y-%m-%d %H:%M:%S')} {moisture.plant, moisture.moisture}")
    except Exception as e:
        print(f"Storage failed: {e}")

def fetch_moisture_reading() -> MoistureDto:
    moisture = None
    try:
        response = requests.get(config.MOISTURE_URL)
        response.raise_for_status()
        data = response.json()
        moisture = MoistureDto("Monstera", data["moisture"])
    except requests.RequestException as e:
        print(f"Request failed: {e}")
    return moisture
    

def run_fetcher():
    while True:
        moisture = fetch_moisture_reading()
        if moisture is not None:
            store(moisture)
        time.sleep(config.INTERVAL)


def render_chart(plant_moisture: list[Moisture]):
    if not plant_moisture:
        return None

    plant_moisture.sort(key=lambda x: datetime.strptime(x.date, "%Y-%m-%d %H:%M:%S"))
    dates = [datetime.strptime(moisture.date, "%Y-%m-%d %H:%M:%S") for moisture in plant_moisture]
    moisture_values = [moisture.moisture for moisture in plant_moisture]
    
    line_chart = pygal.Line(
        x_label_rotation=35,
        truncate_label=-1,
        x_value_formatter=lambda dt: dt.strftime("%Y-%m-%d @ %H:%M:%S"))
    line_chart.range = [0, 100]
    line_chart.title = f"Plant moisture"
    line_chart.x_labels = dates
    line_chart.add(plant_moisture[0].plant, moisture_values)

    line_chart.render_to_file(config.CHART_FILE)


if __name__ == "__main__":
    initialize_db(config.DB_FILE)

    thread = threading.Thread(target=run_fetcher, daemon=True)
    thread.start()

    app = FastAPI()

    @app.get("/moisture")
    def get_moisture():
        """Retrieve the latest moisture data from the database."""
        results = get_stored_moisture(config.READINGS)

        if results:
            return results
        else:
            return {"message": "No data available"}
    
    @app.get("/chart", response_class=FileResponse)
    def get_moisture():
        """Retrieve the latest moisture data from the database."""
        results = get_stored_moisture(config.READINGS)
        render_chart(results)
        return FileResponse(config.CHART_FILE)

    uvicorn.run(app, port=config.PORT)