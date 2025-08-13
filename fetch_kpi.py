import requests
from bs4 import BeautifulSoup
import re
import csv
import os
from datetime import datetime

URL = "https://adtraction.com/se/om-adtraction/"
CSV_FILE = "kpi-history.csv"

def fetch_stats():
    resp = requests.get(URL, timeout=10)
    resp.raise_for_status()
    soup = BeautifulSoup(resp.text, "html.parser")
    strings = list(soup.stripped_strings)
    try:
        start = strings.index("Vår plattform")
    except ValueError:
        raise RuntimeError("Couldn't locate the 'Vår plattform' section.")
    stats = {}
    i = start + 1
    while i < len(strings) - 1:
        label = strings[i].strip()
        value = strings[i+1].strip()
        if re.fullmatch(r"[\d\s]+", value):
            stats[label] = int(value.replace(" ", ""))
            i += 2
        else:
            i += 1
    return stats

if __name__ == "__main__":
    stats = fetch_stats()
    conv   = stats.get("Konverteringar:", 0)
    brands = stats.get("Varumärken",    0)

    # 1) Print to console
    print(f"Konverteringar: {conv:,}")
    print(f"Varumärken:     {brands:,}")

    # 2) Append to CSV
    header = ["Date","Konverteringar","Varumärken"]
    row    = [ datetime.now().strftime("%Y-%m-%d"), conv, brands ]

    write_header = not os.path.exists(CSV_FILE)
    with open(CSV_FILE, "a", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        if write_header:
            writer.writerow(header)
        writer.writerow(row)

    print(f"Appended to {CSV_FILE}")
