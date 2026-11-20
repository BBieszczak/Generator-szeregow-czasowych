import logging
import pandas as pd
from prophet import Prophet

# Wyciszenie logów informacyjnych biblioteki Prophet i cmdstanpy
logging.getLogger("cmdstanpy").setLevel(logging.WARNING)


def prognozuj_prophet(df: pd.DataFrame, df_przyszle: pd.DataFrame | None, horyzont: int) -> pd.Series:
    print("\n--- Trenowanie modelu Prophet ---")

    df_p = pd.DataFrame({"ds": df.index, "y": df.iloc[:, 0].values})

    has_exog = df.shape[1] > 1
    m = Prophet()

    if has_exog:
        for col in df.columns[1:]:
            df_p[col] = df[col].values
            m.add_regressor(col)

    m.fit(df_p)

    future = m.make_future_dataframe(periods=horyzont, freq=df.index.freq)

    if has_exog and df_przyszle is not None:
        for col in df.columns[1:]:
            future[col] = list(df[col].values) + list(df_przyszle[col].values)

    forecast = m.predict(future)

    przyszle_daty = pd.date_range(start=df.index[-1], periods=horyzont + 1, freq=df.index.freq)[1:]
    pelen_indeks = df.index.append(przyszle_daty)

    return pd.Series(forecast["yhat"].values, index=pelen_indeks)
