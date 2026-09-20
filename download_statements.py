"""Download six official FOMC statements as clean paragraph text files."""
from pathlib import Path
import re
import requests
from bs4 import BeautifulSoup

STATEMENTS = {
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

