import pytest
import pandas as pd
from unittest.mock import patch

from pliki_operacje.wczytanie_xlsx import (
    buduj_szereg_historyczny,
    wprowadz_przyszle_regresory,
    wybor_kolumn,
)


# ==================== DANE TESTOWE ====================

@pytest.fixture
def przykladowy_excel(tmp_path):
    """Tworzy tymczasowy plik .xlsx z prostymi danymi do testów."""
    dane = {
        "Data": pd.date_range("2020-01-01", periods=12, freq="MS"),
        "Wartosc": [10.0, 12.5, 11.0, 13.0, 14.5, 15.0, 16.0, 17.5, 18.0, 19.0, 20.5, 21.0],
    }
    df = pd.DataFrame(dane)
    sciezka = tmp_path / "test.xlsx"
    df.to_excel(sciezka, index=False)
    return sciezka


@pytest.fixture
def przykladowy_excel_z_regresorem(tmp_path):
    """Tworzy tymczasowy plik .xlsx z danymi + regresorem."""
    dane = {
        "Data": pd.date_range("2020-01-01", periods=12, freq="MS"),
        "Wartosc": [10.0, 12.5, 11.0, 13.0, 14.5, 15.0, 16.0, 17.5, 18.0, 19.0, 20.5, 21.0],
        "Regresor": [1.0, 1.1, 1.2, 1.3, 1.4, 1.5, 1.6, 1.7, 1.8, 1.9, 2.0, 2.1],
    }
    df = pd.DataFrame(dane)
    sciezka = tmp_path / "test_reg.xlsx"
    df.to_excel(sciezka, index=False)
    return sciezka


@pytest.fixture
def przykladowy_df():
    """Gotowy DataFrame z indeksem DatetimeIndex (jak po buduj_szereg_historyczny)."""
    daty = pd.date_range("2020-01-01", periods=12, freq="MS")
    df = pd.DataFrame(
        {"Wartosc": [10, 12, 11, 13, 14, 15, 16, 17, 18, 19, 20, 21]},
        index=daty,
    )
    df.index.name = "Data"
    return df


@pytest.fixture
def przykladowy_df_z_regresorem():
    """Gotowy DataFrame z Y + regresorem."""
    daty = pd.date_range("2020-01-01", periods=12, freq="MS")
    df = pd.DataFrame(
        {
            "Wartosc": [10, 12, 11, 13, 14, 15, 16, 17, 18, 19, 20, 21],
            "Regresor": [1.0, 1.1, 1.2, 1.3, 1.4, 1.5, 1.6, 1.7, 1.8, 1.9, 2.0, 2.1],
        },
        index=pd.date_range("2020-01-01", periods=12, freq="MS"),
    )
    df.index.name = "Data"
    return df


# ==================== TESTY DLA buduj_szereg_historyczny ====================

class TestBudujSzeregHistoryczny:
    """Testy dla funkcji budującej DataFrame z pliku .xlsx."""

    def test_buduje_z_jednej_kolumny(self, przykladowy_excel):
        """Powinien zbudować szereg z kolumną Y i indeksem typu DatetimeIndex."""
        df = buduj_szereg_historyczny(przykladowy_excel, "A", "B", [], "M")

        assert isinstance(df.index, pd.DatetimeIndex)
        assert len(df) == 12
        assert df.shape[1] == 1  # tylko kolumna Y

    def test_buduje_z_regresorem(self, przykladowy_excel_z_regresorem):
        """Powinien zbudować szereg z kolumną Y + regresor."""
        df = buduj_szereg_historyczny(przykladowy_excel_z_regresorem, "A", "B", ["C"], "M")

        assert isinstance(df.index, pd.DatetimeIndex)
        assert len(df) == 12
        assert df.shape[1] == 2  # Y + 1 regresor

    def test_indeks_posortowany(self, przykladowy_excel):
        """Indeks powinien być posortowany rosnąco."""
        df = buduj_szereg_historyczny(przykladowy_excel, "A", "B", [], "M")
        assert df.index.is_monotonic_increasing

    def test_wartosci_numeryczne(self, przykladowy_excel):
        """Wszystkie wartości w kolumnach powinny być numeryczne."""
        df = buduj_szereg_historyczny(przykladowy_excel, "A", "B", [], "M")
        for kol in df.columns:
            assert pd.api.types.is_numeric_dtype(df[kol])

    def test_czestotliwosc_miesieczna(self, przykladowy_excel):
        """Przy jednostce 'M' indeks powinien mieć częstotliwość 'MS'."""
        df = buduj_szereg_historyczny(przykladowy_excel, "A", "B", [], "M")
        assert df.index.freq is not None
        assert df.index.freq.name == "MS"


# ==================== TESTY DLA wprowadz_przyszle_regresory ====================

class TestWprowadzPrzyszleRegresory:
    """Testy dla funkcji pobierającej przyszłe wartości regresorów."""

    def test_brak_regresorow_zwraca_none(self, przykladowy_df):
        """Gdy brak regresorów (ile=0), powinien zwrócić None."""
        wynik = wprowadz_przyszle_regresory(przykladowy_df, horyzont=3, liczba_regresorow=0)
        assert wynik is None

    def test_z_regresorem_zwraca_dataframe(self, przykladowy_df_z_regresorem):
        """Powinien zwrócić DataFrame z odpowiednią liczbą wierszy."""
        # Mockowanie input() — podajemy wartości regresora na 3 przyszłe okresy
        odpowiedzi = iter(["2.2", "2.3", "2.4"])
        with patch("builtins.input", lambda prompt: next(odpowiedzi)):
            wynik = wprowadz_przyszle_regresory(
                przykladowy_df_z_regresorem, horyzont=3, liczba_regresorow=1
            )

        assert isinstance(wynik, pd.DataFrame)
        assert len(wynik) == 3
        assert wynik.index[0] > przykladowy_df_z_regresorem.index[-1]

    def test_przyszle_daty_sa_ciagloscia(self, przykladowy_df_z_regresorem):
        """Przyszłe daty powinny być ciągłością istniejącego indeksu."""
        odpowiedzi = iter(["1.0", "2.0"])
        with patch("builtins.input", lambda prompt: next(odpowiedzi)):
            wynik = wprowadz_przyszle_regresory(
                przykladowy_df_z_regresorem, horyzont=2, liczba_regresorow=1
            )

        ostatnia_data_hist = przykladowy_df_z_regresorem.index[-1]
        assert wynik.index[0] > ostatnia_data_hist


# ==================== TESTY DLA wybor_kolumn ====================

class TestWyborKolumn:
    """Testy dla głównej funkcji orkiestrującej wczytywanie danych."""

    def test_zwraca_none_przy_bledzie(self):
        """Przy błędzie wejścia powinien zwrócić (None, None, 0)."""
        # Symulacja błędu — podajemy plik .csv, co rzuci ValueError
        with patch("builtins.input", side_effect=["dane.csv"]):
            wynik = wybor_kolumn()

        assert wynik[0] is None
        assert wynik[1] is None
        assert wynik[2] == 0

    def test_poprawne_wczytanie(self, przykladowy_excel):
        """Powinien zwrócić (df, None, horyzont) przy poprawnych danych bez regresorów."""
        odpowiedzi = iter([
            przykladowy_excel.name,  # nazwa pliku
            "A",                      # kolumna czasu
            "B",                      # kolumna Y
            "0",                      # 0 regresorów
            "M",                      # miesięcznie
            "3",                      # horyzont
        ])

        with patch("builtins.input", lambda prompt: next(odpowiedzi)):
            with patch(
                    "pliki_operacje.wyjatki.FOLDER_Z_PLIKAMI",
                przykladowy_excel.parent,
            ):
                df, df_przyszle, horyzont = wybor_kolumn()

        assert df is not None
        assert isinstance(df, pd.DataFrame)
        assert df_przyszle is None
        assert horyzont == 3
