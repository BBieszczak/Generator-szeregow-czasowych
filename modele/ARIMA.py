import pandas as pd
from statsmodels.tsa.arima.model import ARIMA


def prognozuj_arima(df: pd.DataFrame, df_przyszle: pd.DataFrame | None, horyzont: int) -> None:
    # Zakładamy, że pierwsza kolumna to zmienna główna Y, a reszta to regresory
    y = df.iloc[:, 0]
    exog_hist = df.iloc[:, 1:] if df.shape[1] > 1 else None

    print("\n--- Trenowanie modelu ARIMA(1,1,1) ---")

    # Tworzenie i dopasowanie modelu
    # order=(1,1,1) to standardowe, podstawowe parametry (AR, I, MA)
    model = ARIMA(endog=y, exog=exog_hist, order=(1, 1, 1))
    dopasowany_model = model.fit()

    # Wyświetlanie samej prognozy
    print(f"\n--- Prognoza na {horyzont} okresów w przód ---")
    prognoza = dopasowany_model.forecast(steps=horyzont, exog=df_przyszle)

    print(prognoza)