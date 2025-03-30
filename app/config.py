from dotenv import load_dotenv
import os


class Config:
    def __init__(self):
        load_dotenv()
        self.DB_FILE = os.getenv("DB_FILE")
        self.CHART_FILE = os.getenv("CHART_FILE")
        self.INTERVAL = 60 * 60 * 1

        self.HOST = os.getenv("HOST", "0.0.0.0")
        self.PORT = os.getenv("PORT", 9000)
        self.MOISTURE_URL = os.getenv("MOISTURE_URL")

        self.INTERVAL = int(os.getenv("INTERVAL", 60 * 60 * 2))
        self.DEFAULT_READINGS = 30


config = Config()
