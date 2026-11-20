import pandas as pd
import numpy as np
from modele.STS import prognozuj_sts


def test_prognozuj_sts_bez_regresorow():
    daty = pd.date_range("2020-01-01", periods=15, freq="MS")
    df = pd.DataFrame({"Y": np.linspace(10, 20, 15)}, index=daty)

    wynik = prognozuj_sts(df, None, horyzont=3)
    assert isinstance(wynik, pd.Series)
    assert len(wynik) == 18
    assert isinstance(wynik.index, pd.DatetimeIndex)


def test_prognozuj_sts_z_regresorami():
    daty = pd.date_range("2020-01-01", periods=15, freq="MS")
    df = pd.DataFrame({"Y": np.linspace(10, 20, 15), "X": np.linspace(1, 2, 15)}, index=daty)

    przyszle_daty = pd.date_range("2021-04-01", periods=2, freq="MS")
    df_przyszle = pd.DataFrame({"X": [2.1, 2.2]}, index=przyszle_daty)

    wynik = prognozuj_sts(df, df_przyszle, horyzont=2)
    assert isinstance(wynik, pd.Series)
    assert len(wynik) == 17
