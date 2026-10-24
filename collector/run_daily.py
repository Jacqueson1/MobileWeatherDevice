import time
from datetime import date, datetime, timedelta, timezone

import httpx

from core.db import get_connection, init_db

URL = "https://api.data.gov.my/weather/forecast/"
MYT = timezone(timedelta(hours=8))  # Malaysia time, UTC+8 (works on Python 3.10)

TYPE_BY_PREFIX = {
    "St": "state",
    "Ds": "district",
    "Tn": "town",
    "Rc": "recreation",
    "Dv": "division",
}


def fetch_forecast(retries=3):
    """Download all forecasts. If we hit the rate limit (429), wait and retry."""
    for attempt in range(1, retries + 1):
        r = httpx.get(URL, timeout=60, follow_redirects=True)
        if r.status_code == 429:
            wait = 60 * attempt
            print(f"Rate limited (429). Waiting {wait}s before retry {attempt}/{retries}...")
            time.sleep(wait)
            continue
        r.raise_for_status()
        return r.json()
    raise RuntimeError("Still rate-limited after all retries")


def save_snapshot(rows):
    """Flatten each nested row and insert it. Returns how many NEW rows were added."""
    now = datetime.now(MYT)
    fetched_date = now.date()
    fetched_at = now.isoformat(timespec="seconds")

    conn = get_connection()
    new_rows = 0
    try:
        with conn:  # one transaction: commits at the end, rolls back if anything fails
            for row in rows:
                loc = row["location"]
                loc_id = loc["location_id"]

                conn.execute(
                    "INSERT OR IGNORE INTO locations (location_id, name, type) VALUES (?, ?, ?)",
                    (loc_id, loc["location_name"], TYPE_BY_PREFIX.get(loc_id[:2], "unknown")),
                )

                forecast_date = date.fromisoformat(row["date"])
                lead_days = (forecast_date - fetched_date).days

                cur = conn.execute(
                    """
                    INSERT OR IGNORE INTO forecast_snapshots
                    (location_id, forecast_date, fetched_date, fetched_at, lead_days,
                     morning_forecast, afternoon_forecast, night_forecast,
                     summary_forecast, summary_when, min_temp, max_temp)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                    """,
                    (
                        loc_id,
                        row["date"],
                        fetched_date.isoformat(),
                        fetched_at,
                        lead_days,
                        row.get("morning_forecast"),
                        row.get("afternoon_forecast"),
                        row.get("night_forecast"),
                        row.get("summary_forecast"),
                        row.get("summary_when"),
                        row.get("min_temp"),
                        row.get("max_temp"),
                    ),
                )
                new_rows += cur.rowcount  # 1 if inserted, 0 if it was a duplicate
    finally:
        conn.close()
    return new_rows


def main():
    init_db()
    rows = fetch_forecast()
    inserted = save_snapshot(rows)
    print(f"Fetched {len(rows)} rows: {inserted} new, {len(rows) - inserted} duplicates skipped")


if __name__ == "__main__":
    main()