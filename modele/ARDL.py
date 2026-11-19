import pandas as pd
from statsmodels.tsa.ardl import ARDL


def prognozuj_ardl(df: pd.DataFrame, df_przyszle: pd.DataFrame | None, horyzont: int) -> pd.Series:
    y = df.iloc[:, 0]
    exog_hist = df.iloc[:, 1:] if df.shape[1] > 1 else None

    print("\n--- Trenowanie modelu ARDL ---")
    order = 1 if exog_hist is not None else 0
    model = ARDL(endog=y, lags=1, exog=exog_hist, order=order)
    dopasowany_model = model.fit()

    # 1. Predykcja dla danych historycznych
    prognoza_hist = dopasowany_model.predict(start=df.index[0], end=df.index[-1])

    # 2. Prognoza na przyszłość
    prognoza_przyszlosc = dopasowany_model.forecast(steps=horyzont, exog=df_przyszle)

    # 3. Połączenie w jeden długi szereg
    pelna_prognoza = pd.concat([prognoza_hist, prognoza_przyszlosc])

    return pelna_prognoza
