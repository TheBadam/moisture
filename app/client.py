import requests
import time
from db import store
from schema import MoistureDto
from config import config


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
