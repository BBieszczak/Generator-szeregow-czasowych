import pandas as pd
import numpy as np
from modele.DHR import prognozuj_dhr


def test_prognozuj_dhr_bez_regresorow():
    daty = pd.date_range("2020-01-01", periods=24, freq="MS")
    df = pd.DataFrame({"Y": np.linspace(10, 20, 24)}, index=daty)

    wynik = prognozuj_dhr(df, None, horyzont=3)
    assert isinstance(wynik, pd.Series)
    assert len(wynik) == 27
    assert isinstance(wynik.index, pd.DatetimeIndex)


def test_prognozuj_dhr_z_regresorami():
    daty = pd.date_range("2020-01-01", periods=24, freq="MS")
    df = pd.DataFrame({"Y": np.linspace(10, 20, 24), "X": np.linspace(1, 2, 24)}, index=daty)

    przyszle_daty = pd.date_range("2022-01-01", periods=2, freq="MS")
    df_przyszle = pd.DataFrame({"X": [2.1, 2.2]}, index=przyszle_daty)

    wynik = prognozuj_dhr(df, df_przyszle, horyzont=2)
    assert isinstance(wynik, pd.Series)
    assert len(wynik) == 26
