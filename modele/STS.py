import pandas as pd
from statsmodels.tsa.statespace.structural import UnobservedComponents


def prognozuj_sts(df: pd.DataFrame, df_przyszle: pd.DataFrame | None, horyzont: int) -> pd.Series:
    y = df.iloc[:, 0]
    exog_hist = df.iloc[:, 1:] if df.shape[1] > 1 else None

    print("\n--- Trenowanie modelu STS ---")
    model = UnobservedComponents(
        endog=y,
        level="local linear trend",
        exog=exog_hist,
    )
    dopasowany_model = model.fit(disp=False)

    prognoza_hist = dopasowany_model.predict(start=df.index[0], end=df.index[-1])
    prognoza_przyszlosc = dopasowany_model.forecast(steps=horyzont, exog=df_przyszle)

    return pd.concat([prognoza_hist, prognoza_przyszlosc])
