import httpx
from bs4 import BeautifulSoup
import json
import os

SEEN_FILE = "data/seen_updates.json"

CCI_URLS = {
    "Antitrust Orders": "https://www.cci.gov.in/antitrust/orders/",
    "Combinations - Sec 31": "https://www.cci.gov.in/combination/orders-section31",
    "Combinations - Sec 43A/44": "https://www.cci.gov.in/combination/orders-section43a_44",
    "Combinations - Modified": "https://www.cci.gov.in/combination/cases-approved-with-modification"
}

def fetch_pdfs(url):
    try:
        response = httpx.get(url, timeout=10)
        soup = BeautifulSoup(response.text, "html.parser")
        links = soup.find_all("a", href=True)
        pdfs = []
        for link in links:
            href = link["href"]
            if href.endswith(".pdf"):
                text = link.text.strip() or "PDF Link"
                full_url = href if href.startswith("http") else f"https://www.cci.gov.in{href}"
                pdfs.append({"title": text, "url": full_url})
        return pdfs
    except Exception as e:
        print(f"Error fetching {url}: {e}")
        return []

def check_for_updates():
    if not os.path.exists(SEEN_FILE):
        with open(SEEN_FILE, "w") as f:
            json.dump({}, f)

    with open(SEEN_FILE, "r") as f:
        seen = json.load(f)

    all_updates = []

    for name, url in CCI_URLS.items():
        current = fetch_pdfs(url)
        prev = seen.get(name, [])
        new_links = [item for item in current if item not in prev]

        if new_links:
            seen[name] = current
            for item in new_links:
                all_updates.append({
                    "section": name,
                    "title": item["title"],
                    "url": item["url"]
                })

    with open(SEEN_FILE, "w") as f:
        json.dump(seen, f, indent=2)

    return all_updates
