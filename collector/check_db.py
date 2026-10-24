from core.db import get_connection

conn = get_connection()

print("snapshots:", conn.execute("SELECT COUNT(*) FROM forecast_snapshots").fetchone()[0])
print("locations:", conn.execute("SELECT COUNT(*) FROM locations").fetchone()[0])

print("\nrows per lead_days:")
for r in conn.execute(
    "SELECT lead_days, COUNT(*) AS n FROM forecast_snapshots GROUP BY lead_days ORDER BY lead_days"
):
    print(f"  lead {r['lead_days']:>3}: {r['n']}")

print("\nLangkawi (Ds001):")
for r in conn.execute(
    """SELECT forecast_date, lead_days, summary_forecast, min_temp, max_temp
       FROM forecast_snapshots WHERE location_id = 'Ds001' ORDER BY forecast_date"""
):
    print(f"  {r['forecast_date']} lead={r['lead_days']} | {r['summary_forecast']} | {r['min_temp']}-{r['max_temp']}")

conn.close()