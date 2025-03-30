from fastapi import FastAPI
import threading
import uvicorn
from datetime import datetime
from fastapi.responses import FileResponse
import pygal
from client import run_fetcher
from db import get_stored_moisture, initialize_db
from schema import Moisture
from config import config


def render_chart(plant_moisture: list[Moisture]):
    if not plant_moisture:
        return None

    plant_moisture.sort(key=lambda x: datetime.strptime(x.date, "%Y-%m-%d %H:%M:%S"))
    dates = [
        datetime.strptime(moisture.date, "%Y-%m-%d %H:%M:%S")
        for moisture in plant_moisture
    ]
    moisture_values = [moisture.moisture for moisture in plant_moisture]

    line_chart = pygal.Line(
        x_label_rotation=35,
        truncate_label=-1,
        x_value_formatter=lambda dt: dt.strftime("%Y-%m-%d @ %H:%M:%S"),
    )
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
    def get_moisture(n_readings: int = config.DEFAULT_READINGS):
        """Retrieve the latest moisture data from the database."""
        results = get_stored_moisture(n_readings)

        if results:
            return results
        else:
            return {"message": "No data available"}

    @app.get("/chart", response_class=FileResponse)
    def get_moisture(n_readings: int = config.DEFAULT_READINGS):
        """Retrieve the latest moisture data from the database."""
        results = get_stored_moisture(n_readings)
        render_chart(results)
        return FileResponse(config.CHART_FILE)

    uvicorn.run(app, host=config.HOST, port=config.PORT)
