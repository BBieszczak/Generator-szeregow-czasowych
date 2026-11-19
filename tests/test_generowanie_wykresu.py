import matplotlib
matplotlib.use("Agg")
import pandas as pd
from unittest.mock import patch
from pliki_operacje.generowanie_wykresu import zapisz_wykres


def test_zapisz_wykres(tmp_path):
    daty = pd.date_range("2020-01-01", periods=3, freq="MS")
    df = pd.DataFrame({"Y": [10.0, 11.0, 12.0]}, index=daty)
    prognoza = pd.Series([10.1, 11.2, 12.1], index=daty)

    with patch("pliki_operacje.generowanie_wykresu.FOLDER_ZAPISU", tmp_path):
        zapisz_wykres(df, prognoza, "ARIMA", 1)

    plik = tmp_path / "ARIMA_1.png"
    assert plik.exists()
    assert plik.stat().st_size > 0
    with open(plik, "rb") as f:
        assert f.read(4) == b"\x89PNG"
