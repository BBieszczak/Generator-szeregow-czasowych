import pandas as pd
from statsmodels.tsa.forecasting.theta import ThetaModel


def prognozuj_theta(df: pd.DataFrame, df_przyszle: pd.DataFrame | None, horyzont: int) -> pd.Series:
    print("\n--- Trenowanie modelu Theta ---")
    y = df.iloc[:, 0]

    period = 12 if len(df) >= 24 else (4 if len(df) >= 8 else None)
    model = ThetaModel(y, period=period)
    dopasowany_model = model.fit()

    prognoza_hist = y.copy()
    prognoza_przyszlosc = dopasowany_model.forecast(steps=horyzont)

    return pd.concat([prognoza_hist, prognoza_przyszlosc])
