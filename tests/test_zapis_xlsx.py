import pytest
import pandas as pd
from pathlib import Path
from unittest.mock import patch

from pliki_operacje.zapis_xlsx import zapisz_prognoze, FOLDER_ZAPISU


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


# ==================== TESTY DLA zapisz_prognoze ====================

class TestZapiszPrognoze:
    """Testy dla funkcji zapisującej prognozę do pliku .xlsx."""

    def test_tworzy_plik_xlsx(self, tmp_path, dane_historyczne, prognoza):
        """Powinien utworzyć plik .xlsx w podanym folderze."""
        with patch("pliki_operacje.zapis_xlsx.FOLDER_ZAPISU", tmp_path):
            zapisz_prognoze(dane_historyczne, prognoza, "ARIMA", 3)

        plik = tmp_path / "ARIMA_3.xlsx"
        assert plik.exists()

    def test_plik_ma_poprawna_nazwe(self, tmp_path, dane_historyczne, prognoza):
        """Nazwa pliku powinna mieć format '{model}_{horyzont}.xlsx'."""
        with patch("pliki_operacje.zapis_xlsx.FOLDER_ZAPISU", tmp_path):
            zapisz_prognoze(dane_historyczne, prognoza, "TEST_MODEL", 5)

        plik = tmp_path / "TEST_MODEL_5.xlsx"
        assert plik.exists()

    def test_plik_zawiera_poprawne_kolumny(self, tmp_path, dane_historyczne, prognoza):
        """Plik powinien zawierać kolumny 'Wartość rzeczywista' i 'Predykcja'."""
        with patch("pliki_operacje.zapis_xlsx.FOLDER_ZAPISU", tmp_path):
            zapisz_prognoze(dane_historyczne, prognoza, "ARIMA", 3)

        plik = tmp_path / "ARIMA_3.xlsx"
        wynik = pd.read_excel(plik, index_col=0)

        assert "Wartość rzeczywista" in wynik.columns
        assert "Predykcja" in wynik.columns

    def test_plik_zawiera_dane_historyczne(self, tmp_path, dane_historyczne, prognoza):
        """Kolumna 'Wartość rzeczywista' powinna mieć 12 niepustych wierszy."""
        with patch("pliki_operacje.zapis_xlsx.FOLDER_ZAPISU", tmp_path):
            zapisz_prognoze(dane_historyczne, prognoza, "ARIMA", 3)

        plik = tmp_path / "ARIMA_3.xlsx"
        wynik = pd.read_excel(plik, index_col=0)

        assert wynik["Wartość rzeczywista"].notna().sum() == 12

    def test_plik_zawiera_prognoze_przyszla(self, tmp_path, dane_historyczne, prognoza):
        """Kolumna 'Predykcja' powinna mieć 15 wierszy (12 hist + 3 przyszłe)."""
        with patch("pliki_operacje.zapis_xlsx.FOLDER_ZAPISU", tmp_path):
            zapisz_prognoze(dane_historyczne, prognoza, "ARIMA", 3)

        plik = tmp_path / "ARIMA_3.xlsx"
        wynik = pd.read_excel(plik, index_col=0)

        assert wynik["Predykcja"].notna().sum() == 15

    def test_tworzy_folder_jesli_nie_istnieje(self, tmp_path, dane_historyczne, prognoza):
        """Powinien automatycznie utworzyć folder docelowy."""
        nowy_folder = tmp_path / "nowy_folder_zapisu"
        with patch("pliki_operacje.zapis_xlsx.FOLDER_ZAPISU", nowy_folder):
            zapisz_prognoze(dane_historyczne, prognoza, "ARIMA", 3)

        assert nowy_folder.exists()
        assert (nowy_folder / "ARIMA_3.xlsx").exists()


# ==================== TESTY DLA FOLDER_ZAPISU ====================

class TestFolderZapisu:
    """Testy dla stałej FOLDER_ZAPISU."""

    def test_folder_konczy_sie_na_szeregi_czasowe(self):
        """Ścieżka folderu powinna kończyć się na 'szeregi_czasowe'."""
        assert FOLDER_ZAPISU.name == "szeregi_czasowe"

    def test_folder_jest_absolutny(self):
        """Ścieżka folderu powinna być absolutna."""
        assert FOLDER_ZAPISU.is_absolute()
