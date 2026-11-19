import pandas as pd
from statsmodels.tsa.holtwinters import ExponentialSmoothing


def prognozuj_ets(df: pd.DataFrame, df_przyszle: pd.DataFrame | None, horyzont: int) -> pd.Series:
    print("\n--- Trenowanie modelu ETS (Holt-Winters) ---")
    y = df.iloc[:, 0]

    model = ExponentialSmoothing(y, trend="add")
    dopasowany_model = model.fit()

    prognoza_hist = dopasowany_model.fittedvalues
    prognoza_przyszlosc = dopasowany_model.forecast(steps=horyzont)

    return pd.concat([prognoza_hist, prognoza_przyszlosc])
