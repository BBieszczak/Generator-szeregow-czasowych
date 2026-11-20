import pandas as pd
from statsmodels.tsa.statespace.sarimax import SARIMAX


def prognozuj_sarima(df: pd.DataFrame, df_przyszle: pd.DataFrame | None, horyzont: int) -> pd.Series:
    y = df.iloc[:, 0]
    exog_hist = df.iloc[:, 1:] if df.shape[1] > 1 else None

    print("\n--- Trenowanie modelu SARIMA ---")
    s = 12 if len(df) >= 24 else (4 if len(df) >= 8 else 1)
    seasonal_order = (1, 1, 0, s) if s > 1 else (0, 0, 0, 0)

    model = SARIMAX(
        endog=y,
        exog=exog_hist,
        order=(1, 1, 1),
        seasonal_order=seasonal_order,
        enforce_stationarity=False,
        enforce_invertibility=False,
    )
    dopasowany_model = model.fit(disp=False)

    prognoza_hist = dopasowany_model.predict(start=df.index[0], end=df.index[-1])
    prognoza_przyszlosc = dopasowany_model.forecast(steps=horyzont, exog=df_przyszle)

    return pd.concat([prognoza_hist, prognoza_przyszlosc])
