import pandas as pd
from statsmodels.tsa.arima.model import ARIMA
from statsmodels.tsa.forecasting.stl import STLForecast


def prognozuj_stls(df: pd.DataFrame, df_przyszle: pd.DataFrame | None, horyzont: int) -> pd.Series:
    y = df.iloc[:, 0]
    exog_hist = df.iloc[:, 1:] if df.shape[1] > 1 else None

    print("\n--- Trenowanie modelu STLS ---")
    period = 12 if len(df) >= 24 else (4 if len(df) >= 8 else 2)

    model_kwargs = {"order": (1, 1, 0)}
    if exog_hist is not None:
        model_kwargs["exog"] = exog_hist

    stlf = STLForecast(y, ARIMA, model_kwargs=model_kwargs, period=period)
    dopasowany_model = stlf.fit()

    if exog_hist is not None:
        prognoza_hist = dopasowany_model.get_prediction(start=0, end=len(df) - 1, exog=exog_hist).predicted_mean
        prognoza_przyszlosc = dopasowany_model.forecast(steps=horyzont, exog=df_przyszle)
    else:
        prognoza_hist = dopasowany_model.get_prediction(start=0, end=len(df) - 1).predicted_mean
        prognoza_przyszlosc = dopasowany_model.forecast(steps=horyzont)

    return pd.concat([prognoza_hist, prognoza_przyszlosc])
