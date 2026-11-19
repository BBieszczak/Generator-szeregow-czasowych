import pytest
import pandas as pd
from pathlib import Path
from unittest.mock import patch
import matplotlib
matplotlib.use("Agg")  # Backend bez GUI — niezbędny w środowisku testowym

from pliki_operacje.generowanie_wykresu import zapisz_wykres, FOLDER_ZAPISU


# ==================== DANE TESTOWE ====================

@pytest.fixture
def dane_historyczne():
    """DataFrame z danymi historycznymi (indeks DatetimeIndex)."""
    daty = pd.date_range("2020-01-01", periods=12, freq="MS")
    df = pd.DataFrame(
        {"Wartosc": [10, 12, 11, 13, 14, 15, 16, 17, 18, 19, 20, 21]},
        index=daty,
    )
    df.index.name = "Data"
    return df


@pytest.fixture
def prognoza(dane_historyczne):
    """Prognoza jako pd.Series (historyczna + przyszła)."""
    daty_hist = dane_historyczne.index
    daty_przyszle = pd.date_range("2021-01-01", periods=3, freq="MS")
    pelen_indeks = daty_hist.append(daty_przyszle)
    return pd.Series(
        [10.5, 12.0, 11.5, 13.2, 14.1, 15.3, 16.1, 17.2, 18.4, 19.1, 20.0, 21.5, 22.0, 23.0, 24.0],
        index=pelen_indeks,
    )


# ==================== TESTY DLA zapisz_wykres ====================

class TestZapiszWykres:
    """Testy dla funkcji zapisującej wykres do pliku .png."""

    def test_tworzy_plik_png(self, tmp_path, dane_historyczne, prognoza):
        """Powinien utworzyć plik .png w podanym folderze."""
        with patch("pliki_operacje.generowanie_wykresu.FOLDER_ZAPISU", tmp_path):
            zapisz_wykres(dane_historyczne, prognoza, "ARIMA", 3)

        plik = tmp_path / "ARIMA_3.png"
        assert plik.exists()

    def test_plik_ma_poprawna_nazwe(self, tmp_path, dane_historyczne, prognoza):
        """Nazwa pliku powinna mieć format '{model}_{horyzont}.png'."""
        with patch("pliki_operacje.generowanie_wykresu.FOLDER_ZAPISU", tmp_path):
            zapisz_wykres(dane_historyczne, prognoza, "TEST_MODEL", 5)

        plik = tmp_path / "TEST_MODEL_5.png"
        assert plik.exists()

    def test_plik_nie_jest_pusty(self, tmp_path, dane_historyczne, prognoza):
        """Wygenerowany plik .png powinien mieć rozmiar > 0."""
        with patch("pliki_operacje.generowanie_wykresu.FOLDER_ZAPISU", tmp_path):
            zapisz_wykres(dane_historyczne, prognoza, "ARIMA", 3)

        plik = tmp_path / "ARIMA_3.png"
        assert plik.stat().st_size > 0

    def test_tworzy_folder_jesli_nie_istnieje(self, tmp_path, dane_historyczne, prognoza):
        """Powinien automatycznie utworzyć folder 'wykresy', jeśli nie istnieje."""
        nowy_folder = tmp_path / "nowy_folder_wykresow"
        with patch("pliki_operacje.generowanie_wykresu.FOLDER_ZAPISU", nowy_folder):
            zapisz_wykres(dane_historyczne, prognoza, "ARIMA", 3)

        assert nowy_folder.exists()
        assert (nowy_folder / "ARIMA_3.png").exists()

    def test_plik_to_poprawny_png(self, tmp_path, dane_historyczne, prognoza):
        """Plik powinien zaczynać się od nagłówka PNG (magic bytes)."""
        with patch("pliki_operacje.generowanie_wykresu.FOLDER_ZAPISU", tmp_path):
            zapisz_wykres(dane_historyczne, prognoza, "ARIMA", 3)

        plik = tmp_path / "ARIMA_3.png"
        with open(plik, "rb") as f:
            naglowek = f.read(8)
        # Standardowy nagłówek pliku PNG
        assert naglowek[:4] == b"\x89PNG"


# ==================== TESTY DLA FOLDER_ZAPISU ====================

class TestFolderZapisuWykresow:
    """Testy dla stałej FOLDER_ZAPISU w module generowanie_wykresu."""

    def test_folder_konczy_sie_na_wykresy(self):
        """Ścieżka folderu powinna kończyć się na 'wykresy'."""
        assert FOLDER_ZAPISU.name == "wykresy"

    def test_folder_jest_absolutny(self):
        """Ścieżka folderu powinna być absolutna."""
        assert FOLDER_ZAPISU.is_absolute()
