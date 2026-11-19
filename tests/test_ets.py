import pandas as pd
import numpy as np
from modele.ETS import prognozuj_ets


def test_prognozuj_ets():
    daty = pd.date_range("2020-01-01", periods=24, freq="MS")
    df = pd.DataFrame({"Y": np.linspace(10, 20, 24)}, index=daty)

    wynik = prognozuj_ets(df, None, horyzont=3)
    assert isinstance(wynik, pd.Series)
    assert len(wynik) == 27
    assert isinstance(wynik.index, pd.DatetimeIndex)
