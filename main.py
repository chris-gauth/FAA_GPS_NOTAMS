import json
import requests
import feedparser
import re
from bs4 import BeautifulSoup

from GeoPlot import plot_faa_notices


def clean_html(raw_html):
    return BeautifulSoup(raw_html, "html.parser").get_text(separator=" ", strip=True)

def save_to_json(entries, filename="faa_notices.json"):
    cleaned_entries = []
    for entry in entries:
        description = clean_html(entry.get("description", ""))
        latitude, longitude = extract_coordinates(description)

        cleaned_entries.append({
            "title": clean_html(entry.get("title", "")),
            "description": description,
            "latitude": latitude,
            "longitude": longitude,
            "link": entry.get("link", ""),
        })

    with open(filename, "w", encoding="utf-8") as f:
        json.dump(cleaned_entries, f, indent=2, ensure_ascii=False)
    print(f"\n Saved {len(cleaned_entries)} entries to {filename} in JSON format")

def extract_coordinates(text):
    match = re.search(r"Centered at (\d{6,8}[NS])(\d{6,8}[EW])", text)
    if match:
        return match.group(1), match.group(2)
    return None, None

def fetch_faa_notices(feed_url, max_items=50):
    response = requests.get(feed_url)
    feed = feedparser.parse(response.content)

    matching_entries = []

    for entry in feed.entries[:max_items]:
        title = clean_html(entry.get("title", "")) + " "
        description = clean_html(entry.get("description", ""))
        link = entry.get("link", "")

        if "GPS INTERFERENCE" in description.upper():
        #    print(f"{title}")
        #    print(f"{description}")
        #    print(f"{link}")
            matching_entries.append(entry)

    return matching_entries

if __name__ == "__main__":
    URL = "https://www.faasafety.gov/RSS/NoticesRSS.aspx"
    results = fetch_faa_notices(URL)
    if results:
        save_to_json(results)
        plot_faa_notices()
