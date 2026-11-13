import pandas as pd
from statsmodels.tsa.arima.model import ARIMA


def prognozuj_arima(df: pd.DataFrame, df_przyszle: pd.DataFrame | None, horyzont: int) -> pd.Series:
    y = df.iloc[:, 0]
    exog_hist = df.iloc[:, 1:] if df.shape[1] > 1 else None

    print("\n--- Trenowanie modelu ARIMA(1,1,1) ---")
    model = ARIMA(endog=y, exog=exog_hist, order=(1, 1, 1))
    dopasowany_model = model.fit()

    # 1. Predykcja dla danych historycznych (od pierwszej do ostatniej znanej daty)
    prognoza_hist = dopasowany_model.predict(start=df.index[0], end=df.index[-1])

    # 2. Prognoza na przyszłość (dla dodanych horyzontów)
    prognoza_przyszlosc = dopasowany_model.forecast(steps=horyzont, exog=df_przyszle)

    # 3. Połączenie w jeden długi szereg (od początku historii do końca prognozy)
    pelna_prognoza = pd.concat([prognoza_hist, prognoza_przyszlosc])

    return pelna_prognoza