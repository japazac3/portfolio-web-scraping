
import pandas as pd
import pytest

from visualize_data import (
    generate_charts,
    prepare_data,
    CHART_FILES
)


@pytest.fixture
def sample_data():
    """Datos de ejemplo para probar la generacion de graficos."""

    return pd.DataFrame({
        "title": [
            f"Libro de prueba {i}" for i in range(12)
        ],
        "rating": [
            1, 2, 3, 4, 5, 1,
            2, 3, 4, 5, 3, 4
        ],
        "price_gbp_numeric": [
            10.5, 15.0, 20.0, 25.5,
            30.0, 35.0, 40.0, 45.0,
            50.0, 55.0, 12.0, 18.0
        ],
        "is_available": [
            True, True, False, True,
            False, True, True, False,
            True, True, False, True
        ]
    })


def test_generates_six_charts(sample_data, tmp_path):
    """Comprueba que se generen los seis archivos PNG."""

    generated_files = generate_charts(
        sample_data,
        report_dir=tmp_path
    )

    assert len(generated_files) == 6

    for file in generated_files:
        assert file.exists()
        assert file.stat().st_size > 0
        assert file.suffix == ".png"

    generated_names = {
        file.name for file in generated_files
    }

    assert generated_names == set(CHART_FILES)


def test_prepare_data_rejects_missing_columns(sample_data):
    """Comprueba que se detecten columnas faltantes."""

    incomplete_data = sample_data.drop(
        columns=["rating"]
    )

    with pytest.raises(ValueError, match="Faltan columnas"):
        prepare_data(incomplete_data)


def test_prepare_data_rejects_empty_data(sample_data):
    """Comprueba que se rechacen datos sin registros validos."""

    invalid_data = sample_data.copy()

    invalid_data["price_gbp_numeric"] = "invalido"
    invalid_data["rating"] = "invalido"

    with pytest.raises(ValueError, match="No existen registros validos"):
        prepare_data(invalid_data)
