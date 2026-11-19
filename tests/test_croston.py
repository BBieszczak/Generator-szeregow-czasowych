import pandas as pd
from modele.CROSTON import prognozuj_croston


def test_prognozuj_croston():
    daty = pd.date_range("2020-01-01", periods=10, freq="MS")
    df = pd.DataFrame({"Y": [0, 2, 0, 0, 3, 0, 1, 0, 0, 2]}, index=daty)

    wynik = prognozuj_croston(df, None, horyzont=3)
    assert isinstance(wynik, pd.Series)
    assert len(wynik) == 13
    assert isinstance(wynik.index, pd.DatetimeIndex)
    assert wynik.iloc[-1] > 0
