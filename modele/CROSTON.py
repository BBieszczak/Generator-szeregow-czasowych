import pandas as pd
from croston import croston


def prognozuj_croston(df: pd.DataFrame, df_przyszle: pd.DataFrame | None, horyzont: int) -> pd.Series:
    print("\n--- Obliczanie prognozy modelem Crostona ---")
    y = df.iloc[:, 0].to_numpy(dtype=float)

    wynik = croston.fit_croston(y, horyzont, "original")

    przyszle_daty = pd.date_range(start=df.index[-1], periods=horyzont + 1, freq=df.index.freq)[1:]

    prognoza_hist = pd.Series(wynik["croston_fittedvalues"], index=df.index)
    prognoza_przyszlosc = pd.Series(wynik["croston_forecast"], index=przyszle_daty)

    return pd.concat([prognoza_hist, prognoza_przyszlosc])
