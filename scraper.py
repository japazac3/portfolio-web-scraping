"""Educational scraper for https://books.toscrape.com/."""
import argparse
import csv
import logging
import random
import time
from dataclasses import dataclass, asdict
from pathlib import Path
from typing import Optional
from urllib.parse import urljoin

import requests
from bs4 import BeautifulSoup
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

BASE_URL = "https://books.toscrape.com/"
RATINGS = {"One": 1, "Two": 2, "Three": 3, "Four": 4, "Five": 5}

@dataclass
class Book:
    title: str
    price_gbp: str
    availability: str
    rating: Optional[int]
    product_url: str
    source_page: str

def build_session():
    session = requests.Session()
    session.headers.update({"User-Agent": "EducationalPortfolioScraper/1.0 (Python learning project)"})
    retry = Retry(total=3, connect=3, read=3, backoff_factor=1,
                  status_forcelist=(429, 500, 502, 503, 504),
                  allowed_methods=frozenset(["GET"]))
    adapter = HTTPAdapter(max_retries=retry)
    session.mount("https://", adapter)
    session.mount("http://", adapter)
    return session

def fetch_html(session, url, timeout=20):
    response = session.get(url, timeout=timeout)
    response.raise_for_status()
    return response.text

def parse_listing_page(html, page_url):
    soup = BeautifulSoup(html, "html.parser")
    books = []
    for article in soup.select("article.product_pod"):
        title_tag = article.select_one("h3 a")
        price_tag = article.select_one(".price_color")
        availability_tag = article.select_one(".availability")
        if not all([title_tag, price_tag, availability_tag]):
            logging.warning("Skipping incomplete product card on %s", page_url)
            continue
        rating_tag = article.select_one(".star-rating")
        rating = None
        if rating_tag:
            rating = next((RATINGS[c] for c in rating_tag.get("class", []) if c in RATINGS), None)
        books.append(Book(
            title=title_tag.get("title") or title_tag.get_text(strip=True),
            price_gbp=price_tag.get_text(strip=True),
            availability=" ".join(availability_tag.stripped_strings),
            rating=rating,
            product_url=urljoin(page_url, title_tag.get("href", "")),
            source_page=page_url,
        ))
    next_tag = soup.select_one("li.next a")
    next_url = urljoin(page_url, next_tag.get("href")) if next_tag else None
    return books, next_url

def scrape_books(max_pages, delay):
    session = build_session()
    url = BASE_URL
    results = []
    page = 0
    while url and (max_pages is None or page < max_pages):
        page += 1
        logging.info("Reading page %d: %s", page, url)
        try:
            html = fetch_html(session, url)
        except requests.RequestException:
            logging.exception("Could not retrieve %s", url)
            break
        books, next_url = parse_listing_page(html, url)
        logging.info("Found %d records", len(books))
        results.extend(books)
        url = next_url
        if url and (max_pages is None or page < max_pages):
            time.sleep(delay + random.uniform(0, 0.3))
    return results

def save_csv(books, output):
    output = Path(output)
    output.parent.mkdir(parents=True, exist_ok=True)
    fields = list(Book.__dataclass_fields__)
    with output.open("w", newline="", encoding="utf-8-sig") as f:
        writer = csv.DictWriter(f, fieldnames=fields)
        writer.writeheader()
        writer.writerows(asdict(book) for book in books)

def main():
    parser = argparse.ArgumentParser(description="Books to Scrape educational crawler")
    parser.add_argument("--max-pages", type=int, default=50)
    parser.add_argument("--delay", type=float, default=1.0)
    parser.add_argument("--output", default="data/books.csv")
    args = parser.parse_args()
    if args.max_pages < 1:
        parser.error("--max-pages must be >= 1")
    if args.delay < 0.5:
        parser.error("--delay should be >= 0.5 seconds")
    Path("logs").mkdir(exist_ok=True)
    logging.basicConfig(level=logging.INFO,
        format="%(asctime)s | %(levelname)s | %(message)s",
        handlers=[logging.StreamHandler(),
                  logging.FileHandler("logs/scraper.log", encoding="utf-8")])
    books = scrape_books(args.max_pages, args.delay)
    save_csv(books, args.output)
    logging.info("Saved %d records to %s", len(books), args.output)

if __name__ == "__main__":
    main()
