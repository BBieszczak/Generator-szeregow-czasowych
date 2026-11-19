import pytest
import pandas as pd
from unittest.mock import patch
from pliki_operacje.wczytanie_xlsx import (
    buduj_szereg_historyczny,
    wprowadz_przyszle_regresory,
    wybor_kolumn,
)


@pytest.fixture
def mock_excel(tmp_path):
    sciezka = tmp_path / "test.xlsx"
    pd.DataFrame({
        "Data": ["2020M01", "2020M02", "2020M03"],
        "Y": ["1 000,50", "1 200,00", "1 150,75"],
        "X": [1.0, 2.0, 3.0],
    }).to_excel(sciezka, index=False)
    return sciezka


def test_buduj_szereg_historyczny(mock_excel):
    df = buduj_szereg_historyczny(mock_excel, "A", "B", ["C"], "M")
    assert isinstance(df.index, pd.DatetimeIndex)
    assert len(df) == 3
    assert df["Y"].iloc[0] == 1000.50
    assert df.index.freqstr == "MS"


def test_wprowadz_przyszle_regresory():
    daty = pd.date_range("2020-01-01", periods=3, freq="MS")
    df = pd.DataFrame({"Y": [1, 2, 3], "X": [10, 20, 30]}, index=daty)

    assert wprowadz_przyszle_regresory(df, horyzont=2, liczba_regresorow=0) is None

    with patch("builtins.input", side_effect=["40.5", "50.5"]):
        przyszle = wprowadz_przyszle_regresory(df, horyzont=2, liczba_regresorow=1)
        assert isinstance(przyszle, pd.DataFrame)
        assert len(przyszle) == 2
        assert przyszle["X"].tolist() == [40.5, 50.5]


def test_wybor_kolumn_blad():
    with patch("builtins.input", side_effect=["brak.xlsx"]):
        df, przyszle, horyzont = wybor_kolumn()
        assert df is None and przyszle is None and horyzont == 0


def test_wybor_kolumn_sukces(mock_excel):
    odpowiedzi = [mock_excel.name, "A", "B", "0", "M", "3"]
    with patch("builtins.input", side_effect=odpowiedzi):
        with patch("pliki_operacje.wyjatki.FOLDER_Z_PLIKAMI", mock_excel.parent):
            df, przyszle, horyzont = wybor_kolumn()
            assert isinstance(df, pd.DataFrame)
            assert przyszle is None
            assert horyzont == 3
