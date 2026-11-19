import pandas as pd
import numpy as np
from modele.GAM import prognozuj_gam


def test_prognozuj_gam_bez_regresorow():
    daty = pd.date_range("2020-01-01", periods=20, freq="MS")
    df = pd.DataFrame({"Y": np.linspace(10, 20, 20)}, index=daty)

    wynik = prognozuj_gam(df, None, horyzont=3)
    assert isinstance(wynik, pd.Series)
    assert len(wynik) == 23
    assert isinstance(wynik.index, pd.DatetimeIndex)


def test_prognozuj_gam_z_regresorami():
    daty = pd.date_range("2020-01-01", periods=20, freq="MS")
    df = pd.DataFrame({"Y": np.linspace(10, 20, 20), "X": np.linspace(1, 2, 20)}, index=daty)

    przyszle_daty = pd.date_range("2021-09-01", periods=2, freq="MS")
    df_przyszle = pd.DataFrame({"X": [2.1, 2.2]}, index=przyszle_daty)

    wynik = prognozuj_gam(df, df_przyszle, horyzont=2)
    assert isinstance(wynik, pd.Series)
    assert len(wynik) == 22
