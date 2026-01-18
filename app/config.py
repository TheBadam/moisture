import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    def __init__(self):
        # required
        if (moisture_url:=os.getenv("MOISTURE_URL")) is None:
            raise Exception("Undefined moisture service. Please define env variable: 'MOISTURE_URL'")
        self.MOISTURE_URL = moisture_url
        
        # required
        if (chart_file:=os.getenv("CHART_FILE")) is None:
            raise Exception("Undefined moisture chart file. Please define env variable: 'CHART_FILE'")
        self.CHART_FILE = chart_file

        self.DB_FILE = os.getenv("DB_FILE", "moisture.db")
        self.INTERVAL = 60 * 60 * 1

        self.HOST = os.getenv("HOST", "0.0.0.0")
        self.PORT = os.getenv("PORT", 9000)
        

        self.INTERVAL = int(os.getenv("INTERVAL", 60 * 60 * 2)) # 2h
        self.DEFAULT_READINGS = 30


config = Config()
