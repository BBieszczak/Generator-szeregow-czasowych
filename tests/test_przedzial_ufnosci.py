import numpy as np
import pandas as pd
from pliki_operacje.przedzial_ufnosci import oblicz_przedzial_ufnosci


def test_oblicz_przedzial_ufnosci_poprawne_wymiary():
    idx_hist = pd.date_range("2020-01-01", periods=10, freq="MS")
    df = pd.DataFrame({"Y": np.linspace(10, 20, 10)}, index=idx_hist)
    idx_pelny = pd.date_range("2020-01-01", periods=13, freq="MS")
    prognoza = pd.Series(np.linspace(10, 23, 13), index=idx_pelny)

    dolna, gorna = oblicz_przedzial_ufnosci(df, prognoza, horyzont=3, poziom=0.95)
    assert len(dolna) == 3
    assert len(gorna) == 3
    assert (dolna < gorna).all()
    assert (dolna < prognoza.iloc[-3:]).all()
    assert (gorna > prognoza.iloc[-3:]).all()


def test_oblicz_przedzial_ufnosci_zerowy_horyzont():
    idx = pd.date_range("2020-01-01", periods=5, freq="MS")
    df = pd.DataFrame({"Y": [1, 2, 3, 4, 5]}, index=idx)
    prognoza = pd.Series([1, 2, 3, 4, 5], index=idx)

    dolna, gorna = oblicz_przedzial_ufnosci(df, prognoza, horyzont=0)
    assert dolna.empty
    assert gorna.empty
