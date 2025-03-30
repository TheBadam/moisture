import sqlite3
from schema import Moisture, MoistureDto
from config import config


def initialize_db(path_to_db: str):
    """Create table if not exists."""
    conn = sqlite3.connect(path_to_db)
    try:
        cursor = conn.cursor()
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS moisture ( id INTEGER PRIMARY KEY AUTOINCREMENT, plant TEXT, moisture REAL, timestamp DATETIME DEFAULT CURRENT_TIMESTAMP)
        """
        )
        conn.commit()
    finally:
        conn.close()


def get_stored_moisture(last_n: int = 0) -> list[Moisture]:
    conn = sqlite3.connect(config.DB_FILE)
    results = []
    try:
        cursor = conn.cursor()
        cursor.execute(
            """
            SELECT
                timestamp,
                plant,
                moisture
            FROM
                moisture
            ORDER BY
                id DESC
            LIMIT (?)
        """,
            (last_n,),
        )
        results = cursor.fetchall()
    finally:
        conn.close()

    return [Moisture(plant, moisture, date) for [date, plant, moisture] in results]


def store(moisture: MoistureDto):
    try:
        conn = sqlite3.connect(config.DB_FILE)
        try:
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO moisture (plant,moisture) VALUES (?, ?)",
                (moisture.plant, moisture.moisture),
            )
            conn.commit()
        finally:
            conn.close()
    except Exception as e:
        print(f"Storage failed: {e}")
