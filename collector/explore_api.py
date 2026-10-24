import json
from pathlib import Path

import httpx

URL = "https://api.data.gov.my/weather/forecast/"

SAMPLES = Path("samples")
SAMPLES.mkdir(exist_ok=True)

def fetch(params=None):
    """Call the API once and return the parsed JSON."""
    r = httpx.get(URL, params=params, timeout=30, follow_redirects=True)
    print(f"GET {r.url} -> {r.status_code}")

    for name, value in r.headers.items():
        if "rate" in name.lower() or "retry" in name.lower():
            print(f" header {name} = {value}")

    r.raise_for_status()
    return r.json()


# --- Experiment 1: Ask for Everything ---
all_rows = fetch()
print("rows:", len(all_rows))
print("districts:", len({row["location"]["location_id"] for row in all_rows}))
print("dates:", sorted({row["date"] for row in all_rows}))

(SAMPLES / "forecast_all.json").write_text(
    json.dumps(all_rows, ensure_ascii=False, indent=2), encoding="utf-8"
)


# ---Ex-periment 2: Only langkawi, filtered by id ---
langkawi = fetch({"contains": "Ds001@location__location_id"})
print("langkawi rows:", len(langkawi))
for row in langkawi:
    print(row["date"], "|", row["summary_forecast"], "|", row["min_temp"], "-", row["max_temp"])


# --- Experiment 3: which phrases exist in the real data ---
phrases = set()
for now in all_rows:
    for key in ("morning_forecast", "afternoon_forecast", "night_forecast", "summary_forecast"):
        phrases.add(row[key])
print("\n unique phrases:")
for p in sorted(phrases):
    print(" -", p)