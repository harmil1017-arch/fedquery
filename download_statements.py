"""Download six official FOMC statements as clean paragraph text files."""
from pathlib import Path
import re
import requests
from bs4 import BeautifulSoup

STATEMENTS = {
    # 2024
    "2024-01-31": "https://www.federalreserve.gov/newsevents/pressreleases/monetary20240131a.htm",
    "2024-03-20": "https://www.federalreserve.gov/newsevents/pressreleases/monetary20240320a.htm",
    "2024-05-01": "https://www.federalreserve.gov/newsevents/pressreleases/monetary20240501a.htm",
    "2024-06-12": "https://www.federalreserve.gov/newsevents/pressreleases/monetary20240612a.htm",
    "2024-07-31": "https://www.federalreserve.gov/newsevents/pressreleases/monetary20240731a.htm",
    "2024-09-18": "https://www.federalreserve.gov/newsevents/pressreleases/monetary20240918a.htm",
    "2024-11-07": "https://www.federalreserve.gov/newsevents/pressreleases/monetary20241107a.htm",
    "2024-12-18": "https://www.federalreserve.gov/newsevents/pressreleases/monetary20241218a.htm",

    # 2025
    "2025-01-29": "https://www.federalreserve.gov/newsevents/pressreleases/monetary20250129a.htm",
    "2025-03-19": "https://www.federalreserve.gov/newsevents/pressreleases/monetary20250319a.htm",
    "2025-05-07": "https://www.federalreserve.gov/newsevents/pressreleases/monetary20250507a.htm",
    "2025-06-18": "https://www.federalreserve.gov/newsevents/pressreleases/monetary20250618a.htm",
    "2025-07-30": "https://www.federalreserve.gov/newsevents/pressreleases/monetary20250730a.htm",
    "2025-09-17": "https://www.federalreserve.gov/newsevents/pressreleases/monetary20250917a.htm",
    "2025-10-29": "https://www.federalreserve.gov/newsevents/pressreleases/monetary20251029a.htm",
    "2025-12-10": "https://www.federalreserve.gov/newsevents/pressreleases/monetary20251210a.htm",

    # 2026 (available so far)
    "2026-01-28": "https://www.federalreserve.gov/newsevents/pressreleases/monetary20260128a.htm",
    "2026-03-18": "https://www.federalreserve.gov/newsevents/pressreleases/monetary20260318a.htm",
    "2026-04-29": "https://www.federalreserve.gov/newsevents/pressreleases/monetary20260429a.htm",
    "2026-06-17": "https://www.federalreserve.gov/newsevents/pressreleases/monetary20260617a.htm",
    "2026-07-29": "https://www.federalreserve.gov/newsevents/pressreleases/monetary20260729a.htm",
    "2026-09-16": "https://www.federalreserve.gov/newsevents/pressreleases/monetary20260916a.htm",
}

OUT = Path("data/statements")
OUT.mkdir(parents=True, exist_ok=True)

def clean(text: str) -> str:
    return re.sub(r"\\s+", " ", text).strip()

for date, url in STATEMENTS.items():
    response = requests.get(url, timeout=30, headers={"User-Agent": "FedQuery educational project"})
    response.raise_for_status()
    soup = BeautifulSoup(response.text, "html.parser")
    article = soup.find("div", id="article") or soup.find("main") or soup
    paragraphs = [clean(p.get_text(" ", strip=True)) for p in article.find_all("p")]
    # Keep statement content only; drop media/footer boilerplate.
    paragraphs = [p for p in paragraphs if p and "For media inquiries" not in p and "Last Update" not in p]
    (OUT / f"{date}.txt").write_text(
        f"Source: {url}\\nMeeting date: {date}\\n\\n" + "\\n\\n".join(paragraphs) + "\\n",
        encoding="utf-8",
    )
    print(f"Saved {date}.txt ({len(paragraphs)} paragraphs)")

