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
        })

    return templates.TemplateResponse(request, "index.html", {
        "locations": locations,
        "location": current,
        "days": days,
        "fetched_date": fetched_date,
    })