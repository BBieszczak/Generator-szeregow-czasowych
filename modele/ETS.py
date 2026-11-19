import pandas as pd
from statsmodels.tsa.exponential_smoothing.ets import ETSModel


def prognozuj_ets(df: pd.DataFrame, df_przyszle: pd.DataFrame | None, horyzont: int) -> pd.Series:
    y = df.iloc[:, 0]

    print("\n--- Trenowanie modelu ETS ---")
    model = ETSModel(y, error="add", trend="add")
    dopasowany_model = model.fit(disp=False)

    prognoza_hist = dopasowany_model.predict(start=df.index[0], end=df.index[-1])
    prognoza_przyszlosc = dopasowany_model.forecast(steps=horyzont)

    return pd.concat([prognoza_hist, prognoza_przyszlosc])
