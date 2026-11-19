import numpy as np
import pandas as pd
from tbats import TBATS


def prognozuj_btst(df: pd.DataFrame, df_przyszle: pd.DataFrame | None, horyzont: int) -> pd.Series:
    print("\n--- Trenowanie modelu BATS/TBATS ---")
    y = df.iloc[:, 0].to_numpy(dtype=float)

    estimator = TBATS(use_arma_errors=False, use_box_cox=False)
    fitted = estimator.fit(y)

    przyszle_daty = pd.date_range(start=df.index[-1], periods=horyzont + 1, freq=df.index.freq)[1:]

    prognoza_hist = pd.Series(fitted.y_hat, index=df.index)
    prognoza_przyszlosc = pd.Series(fitted.forecast(steps=horyzont), index=przyszle_daty)

    pelna_prognoza = pd.concat([prognoza_hist, prognoza_przyszlosc])
    return pelna_prognoza
