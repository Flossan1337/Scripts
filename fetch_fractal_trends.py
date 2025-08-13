# fetch_fractal_trends.py

import os
from datetime import datetime
import pandas as pd
from pytrends.request import TrendReq

# ── DEFINE YOUR GROUPS ──
GROUPS = [
    ["Fractal North", "Fractal Define", "Fractal Core",   "Fractal Node",    "Fractal Meshify"],
    ["Fractal North", "Fractal Focus",  "Fractal Vector", "Fractal Era",     "Fractal Torrent"],
    ["Fractal North", "Fractal Pop",    "Fractal Ridge",  "Fractal Terra",   "Fractal Mood"],
    ["Fractal North", "Fractal Epoch",  "Fractal Refine", "Fractal Scape"]
]

OUTPUT_CSV = "fractal_trends_monthly.csv"

def fetch_group(keywords):
    """
    Fetch monthly Google Trends for up to 5 keywords
    from Jan 1 2016 until today.
    Returns a DataFrame indexed by month.
    """
    py = TrendReq(hl="en-US", tz=120)  # tz=Stockholm = +2h
    tf = f"2016-01-01 {datetime.now():%Y-%m-%d}"
    py.build_payload(keywords, timeframe=tf)
    df = py.interest_over_time().drop(columns=["isPartial"], errors="ignore")
    # resample to month-end
    return df.resample("M").mean()

def main():
    master = None

    for grp in GROUPS:
        df = fetch_group(grp)
        # on the first group, keep all columns; afterwards drop the duplicate "Fractal North"
        if master is None:
            master = df
        else:
            df = df.drop(columns=["Fractal North"], errors="ignore")
            master = master.join(df, how="outer")

    # reset index into a "Date" column
    out = master.sort_index().reset_index().rename(columns={"date": "Date"})
    out.to_csv(OUTPUT_CSV, index=False)
    print(f"Wrote {len(out)} months to {OUTPUT_CSV}")

if __name__ == "__main__":
    main()
