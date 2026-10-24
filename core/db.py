import sqlite3
from pathlib import Path

DB_PATH = Path("data/weather.db")

SCHEMA = """
CREATE TABLE IF NOT EXISTS locations (
    location_id TEXT PRIMARY KEY,
    name        TEXT NOT NULL,
    type        TEXT NOT NULL,
    lat         REAL,
    lon         REAL
);

CREATE TABLE IF NOT EXISTS forecast_snapshots (
    id                 INTEGER PRIMARY KEY AUTOINCREMENT,
    location_id        TEXT NOT NULL REFERENCES locations(location_id),
    forecast_date      TEXT NOT NULL,
    fetched_date       TEXT NOT NULL,
    fetched_at         TEXT NOT NULL,
    lead_days          INTEGER NOT NULL,
    morning_forecast   TEXT,
    afternoon_forecast TEXT,
    night_forecast     TEXT,
    summary_forecast   TEXT,
    summary_when       TEXT,
    min_temp           INTEGER,
    max_temp           INTEGER,
    UNIQUE (location_id, forecast_date, fetched_date)
);
"""

def get_connection():
    DB_PATH.parent.mkdir(exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    return conn

def init_db():
    conn = get_connection()
    conn.executescript(SCHEMA)
    conn.commit()
    conn.close()

if __name__ == "__main__":
    init_db()
    conn = get_connection()
    tables = conn.execute(
        "SELECT name FROM sqlite_master WHERE type = 'table' ORDER BY name"
    ).fetchall()
    print("tables:", [t["name"] for t in tables])
    conn.close()