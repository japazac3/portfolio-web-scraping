
from pathlib import Path

import pandas as pd
import pytest

from generate_report import generate_report


@pytest.fixture
def sample_csv(tmp_path):
    """Crea un CSV temporal con datos validos."""

    df = pd.DataFrame({
        "title": [
            "Libro de prueba A",
            "Libro de prueba B",
            "Libro de prueba C"
        ],
        "rating": [4, 5, 3],
        "price_gbp_numeric": [15.50, 25.00, 35.75],
        "is_available": [True, True, False]
    })

    csv_file = tmp_path / "books_test.csv"
    df.to_csv(csv_file, index=False, encoding="utf-8-sig")

    return csv_file


def test_generates_valid_pdf(sample_csv, tmp_path):
    """Comprueba que se genere un PDF valido."""

    report_dir = tmp_path / "reports"
    pdf_file = report_dir / "test_report.pdf"

    generate_report(
        data_file=sample_csv,
        report_dir=report_dir,
        pdf_file=pdf_file
    )

    assert pdf_file.exists()
    assert pdf_file.stat().st_size > 1000

    with open(pdf_file, "rb") as file:
        assert file.read(5) == b"%PDF-"


def test_rejects_missing_csv(tmp_path):
    """Comprueba el manejo de archivos inexistentes."""

    with pytest.raises(FileNotFoundError):
        generate_report(
            data_file=tmp_path / "inexistente.csv",
            report_dir=tmp_path / "reports",
            pdf_file=tmp_path / "reports" / "test.pdf"
        )


def test_rejects_missing_columns(tmp_path):
    """Comprueba la validacion de columnas requeridas."""

    csv_file = tmp_path / "incomplete.csv"

    pd.DataFrame({
        "title": ["Libro de prueba"]
    }).to_csv(csv_file, index=False)

    with pytest.raises(ValueError, match="Faltan columnas"):
        generate_report(
            data_file=csv_file,
            report_dir=tmp_path / "reports",
            pdf_file=tmp_path / "reports" / "test.pdf"
        )


def test_rejects_invalid_prices(tmp_path):
    """Comprueba que se rechacen precios no numericos."""

    csv_file = tmp_path / "invalid_prices.csv"

    pd.DataFrame({
        "title": ["Libro de prueba"],
        "rating": [4],
        "price_gbp_numeric": ["precio invalido"],
        "is_available": [True]
    }).to_csv(csv_file, index=False)

    with pytest.raises(
        ValueError,
        match="No existen precios numericos validos"
    ):
        generate_report(
            data_file=csv_file,
            report_dir=tmp_path / "reports",
            pdf_file=tmp_path / "reports" / "test.pdf"
        )
