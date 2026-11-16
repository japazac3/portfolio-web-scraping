
from scraper import parse_listing_page


HTML = """
<article class="product_pod">
    <p class="star-rating Three"></p>
    <h3>
        <a href="catalogue/demo_1/index.html" title="Demo Book">
            Demo
        </a>
    </h3>
    <p class="price_color">£12.34</p>
    <p class="availability"> In stock </p>
</article>

<ul>
    <li class="next">
        <a href="page-2.html">next</a>
    </li>
</ul>
"""


def test_extracts_fields_and_pagination():
    books, next_url = parse_listing_page(
        HTML,
        "https://books.toscrape.com/"
    )

    assert len(books) == 1
    assert books[0].title == "Demo Book"
    assert books[0].rating == 3
    assert next_url == "https://books.toscrape.com/page-2.html"


def test_extracts_book_price():
    books, _ = parse_listing_page(
        HTML,
        "https://books.toscrape.com/"
    )

    assert books[0].price_gbp == "£12.34"


def test_extracts_availability():
    books, _ = parse_listing_page(
        HTML,
        "https://books.toscrape.com/"
    )

    assert "In stock" in books[0].availability
