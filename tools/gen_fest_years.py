"""One-time/annual: festival dates 2020-2030 (New Delhi) -> src/fest_years.json (used by the year-wise tables)."""
import json, os, sys, datetime as dt
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))
from festivals import find_dates
r = find_dates(dt.date(2020, 1, 1), dt.date(2030, 12, 31))
out = {k: sorted({x["date"].isoformat() for x in v if 2020 <= x["date"].year <= 2030}) for k, v in r.items()}
json.dump(out, open(os.path.join(os.path.dirname(__file__), "..", "src", "fest_years.json"), "w"), indent=0)
print(len(out), "festivals")
