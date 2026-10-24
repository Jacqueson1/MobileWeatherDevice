import json
from collections import Counter
from pathlib import Path

rows = json.loads(Path("samples/forecast_all.json").read_text(encoding="utf-8"))
print("rows loaded:", len(rows))

counter = Counter()
for row in rows:
    for key in ("morning_forecast", "afternoon_forecast", "night_forecast", "summary_forecast"):
        counter[row[key].strip().lower()] +=1

print("\n unique phrases (lowercased):", len(counter))
for phrase, count in counter.most_common():
    print(f"{count:6} {phrase}")