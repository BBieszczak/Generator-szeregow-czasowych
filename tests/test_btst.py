import pandas as pd
import numpy as np
from modele.BTST import prognozuj_btst


def test_prognozuj_btst():
    daty = pd.date_range("2020-01-01", periods=20, freq="MS")
    df = pd.DataFrame({"Y": np.linspace(10, 20, 20)}, index=daty)

    wynik = prognozuj_btst(df, None, horyzont=3)
    assert isinstance(wynik, pd.Series)
    assert len(wynik) == 23
    assert isinstance(wynik.index, pd.DatetimeIndex)
