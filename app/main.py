from datetime import date, datetime, timedelta, timezone
from pathlib import Path

from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from core.db import get_connection
from core.translate import translate

BASE_DIR = Path(__file__).parent
MYT = timezone(timedelta(hours=8))   # Malaysia time
DEFAULT_LOCATION = "Ds001"           # Langkawi

app = FastAPI(title="Weather Device")
app.mount("/static", StaticFiles(directory=BASE_DIR / "static"), name="static")
templates = Jinja2Templates(directory=str(BASE_DIR / "templates"))


def day_title(d, today):
    if d == today:
        return "Today"
    if d == today + timedelta(days=1):
        return "Tomorrow"
    return d.strftime("%A")

def temp_bar(min_t, max_t, lo=20, hi=40):
    """Where the range bar sits, as % of a 20-40°C scale."""
    if min_t is None or max_t is None:
        return None, None
    left = max(0, min(100, (min_t - lo) / (hi - lo) * 100))
    right = max(0, min(100, (max_t - lo) / (hi - lo) * 100))
    return round(left, 1), round(max(right - left, 4), 1)


@app.get("/", response_class=HTMLResponse)
def home(request: Request, location: str = DEFAULT_LOCATION):
    conn = get_connection()
    try:
        locations = conn.execute(
            "SELECT location_id, name, type FROM locations ORDER BY name, type"
        ).fetchall()

        current = conn.execute(
            "SELECT location_id, name, type FROM locations WHERE location_id = ?",
            (location,),
        ).fetchone()
        if current is None:
            raise HTTPException(status_code=404, detail="Unknown location")

        # Use the most recent snapshot we saved for this location
        fetched_date = conn.execute(
            "SELECT MAX(fetched_date) FROM forecast_snapshots WHERE location_id = ?",
            (location,),
        ).fetchone()[0]

        rows = []
        if fetched_date:
            rows = conn.execute(
                """SELECT forecast_date, morning_forecast, afternoon_forecast,
                          night_forecast, summary_forecast, min_temp, max_temp
                   FROM forecast_snapshots
                   WHERE location_id = ? AND fetched_date = ?
                   ORDER BY forecast_date""",
                (location, fetched_date),
            ).fetchall()
    finally:
        conn.close()

        today = datetime.now(MYT).date()
    days = []
    for r in rows:
        d = date.fromisoformat(r["forecast_date"])
        bar_left, bar_width = temp_bar(r["min_temp"], r["max_temp"])   # <-- NEW line
        days.append({
            "title": day_title(d, today),
            "label": d.strftime("%d %b"),
            "summary": translate(r["summary_forecast"]),
            "summary_raw": r["summary_forecast"],
            "morning": translate(r["morning_forecast"]),
            "afternoon": translate(r["afternoon_forecast"]),
            "night": translate(r["night_forecast"]),
            "min_temp": r["min_temp"],
            "max_temp": r["max_temp"],
            "bar_left": bar_left,                                      # <-- NEW
            "bar_width": bar_width,                                    # <-- NEW
        })

    return templates.TemplateResponse(request, "index.html", {
        "locations": locations,
        "location": current,
        "days": days,
        "fetched_date": fetched_date,
    })