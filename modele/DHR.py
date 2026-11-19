import pandas as pd
from statsmodels.tsa.deterministic import DeterministicProcess, Fourier
from statsmodels.tsa.arima.model import ARIMA


def prognozuj_dhr(df: pd.DataFrame, df_przyszle: pd.DataFrame | None, horyzont: int) -> pd.Series:
    y = df.iloc[:, 0]
    exog_user_hist = df.iloc[:, 1:] if df.shape[1] > 1 else None

    print("\n--- Trenowanie modelu DHR (Dynamic Harmonic Regression) ---")

    period = 12 if len(df) >= 24 else max(2, min(4, len(df) // 2))
    order = 1 if period <= 4 else 2

    dp = DeterministicProcess(index=df.index, period=period, additional_terms=[Fourier(period=period, order=order)])
    fourier_hist = dp.in_sample()
    fourier_fut = dp.out_of_sample(steps=horyzont)

    if exog_user_hist is not None:
        exog_hist = pd.concat([fourier_hist, exog_user_hist], axis=1)
        exog_fut = pd.concat([fourier_fut, df_przyszle], axis=1)
    else:
        exog_hist = fourier_hist
        exog_fut = fourier_fut

    model = ARIMA(endog=y, exog=exog_hist, order=(1, 1, 1))
    dopasowany_model = model.fit()

    prognoza_hist = dopasowany_model.predict(start=df.index[0], end=df.index[-1])
    prognoza_przyszlosc = dopasowany_model.forecast(steps=horyzont, exog=exog_fut)

    return pd.concat([prognoza_hist, prognoza_przyszlosc])
