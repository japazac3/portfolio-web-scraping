
import pandas as pd
import pytest

from analyze_data import clean_data, validate_columns


@pytest.fixture
def sample_data():
    return pd.DataFrame({
        "title": [
            "Book A",
            "Book A Duplicate",
            "Book B",
            "Book C",
            "Book D"
        ],
        "price_gbp": [
            "£12.34",
            "£15.00",
            "£0.00",
            "invalid",
            "£9.99"
        ],
        "availability": [
            "In stock",
            "In stock",
            "Out of stock",
            None,
            "In stock"
        ],
        "rating": [
            "3",
            "4",
            "6",
            "3.5",
            "invalid"
        ],
        "product_url": [
            "book-a",
            "book-a",
            "book-b",
            "book-c",
            "book-d"
        ],
        "source_page": [
            1, 1, 1, 1, 1
        ]
    })


def test_removes_duplicate_urls(sample_data):
    result = clean_data(sample_data)

    assert len(result) == 4
    assert result["product_url"].is_unique


def test_converts_prices_and_rejects_invalid_values(sample_data):
    result = clean_data(sample_data)

    assert result.loc[
        result["product_url"] == "book-a",
        "price_gbp_numeric"
    ].iloc[0] == 12.34

    assert pd.isna(
        result.loc[
            result["product_url"] == "book-b",
            "price_gbp_numeric"
        ].iloc[0]
    )

    assert pd.isna(
        result.loc[
            result["product_url"] == "book-c",
            "price_gbp_numeric"
        ].iloc[0]
    )

    assert result.loc[
        result["product_url"] == "book-d",
        "price_gbp_numeric"
    ].iloc[0] == 9.99


def test_validates_ratings(sample_data):
    result = clean_data(sample_data)

    assert result.loc[
        result["product_url"] == "book-a",
        "rating"
    ].iloc[0] == 3

    assert pd.isna(
        result.loc[
            result["product_url"] == "book-b",
            "rating"
        ].iloc[0]
    )

    assert pd.isna(
        result.loc[
            result["product_url"] == "book-c",
            "rating"
        ].iloc[0]
    )

    assert pd.isna(
        result.loc[
            result["product_url"] == "book-d",
            "rating"
        ].iloc[0]
    )


def test_identifies_availability(sample_data):
    result = clean_data(sample_data)

    assert result["is_available"].tolist() == [
        True,
        False,
        False,
        True
    ]


def test_rejects_missing_required_columns():
    incomplete_data = pd.DataFrame({
        "title": ["Book A"],
        "price_gbp": ["£12.34"]
    })

    with pytest.raises(ValueError, match="Faltan columnas"):
        validate_columns(incomplete_data)
