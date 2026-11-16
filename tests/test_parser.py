"""Manual parser test; run with: python -m unittest discover -s tests"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import unittest
from scraper import parse_listing_page

HTML = """
<article class="product_pod">
 <p class="star-rating Three"></p>
 <h3><a href="catalogue/demo_1/index.html" title="Demo Book">Demo</a></h3>
 <p class="price_color">£12.34</p>
 <p class="availability"> In stock </p>
</article>
<ul><li class="next"><a href="page-2.html">next</a></li></ul>
"""

class ParserTest(unittest.TestCase):
    def test_extracts_fields_and_pagination(self):
        books, next_url = parse_listing_page(HTML, "https://books.toscrape.com/")
        self.assertEqual(len(books), 1)
        self.assertEqual(books[0].title, "Demo Book")
        self.assertEqual(books[0].rating, 3)
        self.assertEqual(next_url, "https://books.toscrape.com/page-2.html")

if __name__ == "__main__":
    unittest.main()
