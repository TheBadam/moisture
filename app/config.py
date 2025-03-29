from dotenv import load_dotenv
import os
from dataclasses import dataclass

load_dotenv()  # take environment variables


DB_FILE = "/home/adamb/data/moisture.db"
URL = "http://192.168.1.119:8080"
CHART_FILE = "./moisture.svg"

class Config():
    def __init__(self):
        load_dotenv()
        self.DB_FILE = os.getenv("DB_FILE")
        self.CHART_FILE = os.getenv("CHART_FILE")
        self.INTERVAL = 60*60*1

        self.HOST = os.getenv("HOST", "http://localhost")
        self.PORT = os.getenv("PORT", 9000)
        self.MOISTURE_URL = os.getenv("MOISTURE_URL")

        self.INTERVAL = int(os.getenv("INTERVAL", 60*60*2))
        self.READINGS = 30

config =  Config()
