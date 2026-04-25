from urllib.parse import urljoin, urlparse
import requests
from bs4 import BeautifulSoup

DEFAULT_HEADERS = {
    "User-Agent": "Mozilla/5.0 (compatible; PortfolioScraper/1.0; +https://example.com/bot)"
}

BLOCKED_SCHEMES = {"file", "ftp", "mailto", "tel", "javascript", "data"}

def normalize_url(url):
    parsed = urlparse(url)
    if parsed.scheme.lower() in BLOCKED_SCHEMES:
        raise ValueError("Unsupported URL scheme.")
    if parsed.scheme not in ("http", "https"):
        raise ValueError("Only http and https URLs are supported.")
    return url

def scrape_page(url):
    url = normalize_url(url)

    try:
        response = requests.get(url, headers=DEFAULT_HEADERS, timeout=12, allow_redirects=True)
        response.raise_for_status()
    except requests.RequestException as exc:
        raise ValueError(f"Could not fetch page: {exc}") from exc

    content_type = response.headers.get("Content-Type", "")
    if "text/html" not in content_type and content_type:
        raise ValueError("This URL does not look like an HTML page.")

    soup = BeautifulSoup(response.text, "html.parser")

    title = ""
    if soup.title and soup.title.string:
        title = soup.title.string.strip()[:500]

    meta_description = ""
    meta = soup.find("meta", attrs={"name": "description"})
    if meta and meta.get("content"):
        meta_description = meta.get("content", "").strip()

    headings = []
    for tag_name in ["h1", "h2"]:
        for tag in soup.find_all(tag_name):
            text = tag.get_text(" ", strip=True)
            if text:
                headings.append({"tag": tag_name.upper(), "text": text[:500]})

    links = []
    seen = set()
    for a in soup.find_all("a", href=True):
        href = a.get("href", "").strip()
        if not href:
            continue
        absolute = urljoin(response.url, href)
        parsed = urlparse(absolute)
        if parsed.scheme not in ("http", "https"):
            continue
        text = a.get_text(" ", strip=True)[:500]
        if absolute in seen:
            continue
        seen.add(absolute)
        links.append({"text": text, "href": absolute})
        if len(links) >= 100:
            break

    return {
        "final_url": response.url,
        "title": title,
        "meta_description": meta_description,
        "headings": headings[:100],
        "links": links,
        "h1_count": sum(1 for h in headings if h["tag"] == "H1"),
        "h2_count": sum(1 for h in headings if h["tag"] == "H2"),
        "link_count": len(links),
    }
