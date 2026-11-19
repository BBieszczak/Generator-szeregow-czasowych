import pytest
import pandas as pd
import numpy as np

from modele.ARIMA import prognozuj_arima


# ==================== DANE TESTOWE ====================

@pytest.fixture
def dane_bez_regresorow():
    """DataFrame z samą kolumną Y (bez regresorów), indeks DatetimeIndex."""
    daty = pd.date_range("2020-01-01", periods=36, freq="MS")
    np.random.seed(42)
    wartosci = np.cumsum(np.random.randn(36)) + 100  # symulacja szeregu z trendem
    df = pd.DataFrame({"Wartosc": wartosci}, index=daty)
    df.index.name = "Data"
    return df


@pytest.fixture
def dane_z_regresorem():
    """DataFrame z Y + regresor, indeks DatetimeIndex."""
    daty = pd.date_range("2020-01-01", periods=36, freq="MS")
    np.random.seed(42)
    wartosci = np.cumsum(np.random.randn(36)) + 100
    regresor = np.linspace(1, 5, 36)
    df = pd.DataFrame({"Wartosc": wartosci, "Regresor": regresor}, index=daty)
    df.index.name = "Data"
    return df


@pytest.fixture
def przyszle_regresory(dane_z_regresorem):
    """DataFrame z przyszłymi wartościami regresora."""
    horyzont = 6
    przyszle_daty = pd.date_range(
        start=dane_z_regresorem.index[-1],
        periods=horyzont + 1,
        freq="MS",
    )[1:]
    df_przyszle = pd.DataFrame(
        {"Regresor": np.linspace(5, 6, horyzont)},
        index=przyszle_daty,
    )
    df_przyszle.index.name = "Data"
    return df_przyszle


# ==================== TESTY DLA prognozuj_arima ====================

class TestPrognozujArima:
    """Testy dla funkcji prognozującej modelem ARIMA(1,1,1)."""

    # --- Dane bez regresorów ---
    def test_zwraca_series(self, dane_bez_regresorow):
        """Wynik powinien być typu pd.Series."""
        wynik = prognozuj_arima(dane_bez_regresorow, None, horyzont=6)
        assert isinstance(wynik, pd.Series)

    def test_dlugosc_wyniku_bez_regresorow(self, dane_bez_regresorow):
        """Długość prognozy = dane historyczne (36) + horyzont (6) = 42."""
        horyzont = 6
        wynik = prognozuj_arima(dane_bez_regresorow, None, horyzont=horyzont)
        assert len(wynik) == len(dane_bez_regresorow) + horyzont

    def test_wartosci_numeryczne(self, dane_bez_regresorow):
        """Wszystkie wartości prognozy powinny być liczbowe (brak NaN)."""
        wynik = prognozuj_arima(dane_bez_regresorow, None, horyzont=6)
        # Pierwszy punkt predykcji (start=index[0]) może mieć NaN (artefakt ARIMA),
        # ale reszta nie powinna
        assert wynik.iloc[1:].notna().all()

    def test_indeks_to_datetime(self, dane_bez_regresorow):
        """Indeks prognozy powinien być typu DatetimeIndex."""
        wynik = prognozuj_arima(dane_bez_regresorow, None, horyzont=6)
        assert isinstance(wynik.index, pd.DatetimeIndex)

    def test_prognoza_zawiera_daty_przyszle(self, dane_bez_regresorow):
        """Prognoza powinna zawierać daty wykraczające poza dane historyczne."""
        horyzont = 6
        wynik = prognozuj_arima(dane_bez_regresorow, None, horyzont=horyzont)
        ostatnia_data_hist = dane_bez_regresorow.index[-1]
        assert wynik.index[-1] > ostatnia_data_hist

    def test_horyzont_1(self, dane_bez_regresorow):
        """Prognoza z horyzontem 1 — powinien mieć dokładnie 37 punktów."""
        wynik = prognozuj_arima(dane_bez_regresorow, None, horyzont=1)
        assert len(wynik) == len(dane_bez_regresorow) + 1

    # --- Dane z regresorem ---
    def test_z_regresorem(self, dane_z_regresorem, przyszle_regresory):
        """Powinien działać poprawnie z regresorami."""
        horyzont = len(przyszle_regresory)
        wynik = prognozuj_arima(dane_z_regresorem, przyszle_regresory, horyzont=horyzont)
        assert isinstance(wynik, pd.Series)
        assert len(wynik) == len(dane_z_regresorem) + horyzont

    def test_dlugosc_z_regresorem(self, dane_z_regresorem, przyszle_regresory):
        """Długość prognozy z regresorem = 36 + 6 = 42."""
        horyzont = len(przyszle_regresory)
        wynik = prognozuj_arima(dane_z_regresorem, przyszle_regresory, horyzont=horyzont)
        assert len(wynik) == 36 + 6

    # --- Powtarzalność ---
    def test_determinizm(self, dane_bez_regresorow):
        """Dwa wywołania z tymi samymi danymi powinny dać identyczny wynik."""
        wynik_1 = prognozuj_arima(dane_bez_regresorow, None, horyzont=6)
        wynik_2 = prognozuj_arima(dane_bez_regresorow, None, horyzont=6)
        pd.testing.assert_series_equal(wynik_1, wynik_2)
