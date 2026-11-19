import pandas as pd
from unittest.mock import patch
from pliki_operacje.zapis_xlsx import zapisz_prognoze


def test_zapisz_prognoze(tmp_path):
    daty_hist = pd.date_range("2020-01-01", periods=3, freq="MS")
    daty_pelne = pd.date_range("2020-01-01", periods=5, freq="MS")

    df = pd.DataFrame({"Y": [10.0, 11.0, 12.0]}, index=daty_hist)
    prognoza = pd.Series([10.1, 11.2, 12.1, 13.0, 14.0], index=daty_pelne)

    with patch("pliki_operacje.zapis_xlsx.FOLDER_ZAPISU", tmp_path):
        zapisz_prognoze(df, prognoza, "ARIMA", 2)

    plik = tmp_path / "ARIMA_2.xlsx"
    assert plik.exists()

    zapisany = pd.read_excel(plik, index_col=0)
    assert list(zapisany.columns) == ["Wartość rzeczywista", "Predykcja"]
    assert len(zapisany) == 5
