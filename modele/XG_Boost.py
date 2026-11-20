import numpy as np
import pandas as pd
from xgboost import XGBRegressor


def prognozuj_xgboost(df: pd.DataFrame, df_przyszle: pd.DataFrame | None, horyzont: int) -> pd.Series:
    print("\n--- Trenowanie modelu XGBoost ---")
    y = df.iloc[:, 0].to_numpy(dtype=float)
    n = len(y)
    has_exog = df.shape[1] > 1
    exog = df.iloc[:, 1:].to_numpy(dtype=float) if has_exog else None
    exog_fut = df_przyszle.to_numpy(dtype=float) if (has_exog and df_przyszle is not None) else None

    p = max(1, min(3, n // 3))
    X, Y = [], []
    for i in range(p, n):
        row = list(y[i - p : i])
        if has_exog:
            row.extend(exog[i])
        X.append(row)
        Y.append(y[i])

    model = XGBRegressor(n_estimators=50, max_depth=3, random_state=42, verbosity=0)
    model.fit(np.array(X), np.array(Y))

    prog_hist = np.concatenate([y[:p], model.predict(np.array(X))])
    curr_y = list(y[-p:])
    prog_fut = []
    for h in range(horyzont):
        row = list(curr_y[-p:])
        if has_exog and exog_fut is not None:
            row.extend(exog_fut[h])
        pred = float(model.predict(np.array([row]))[0])
        prog_fut.append(pred)
        curr_y.append(pred)

    przyszle_daty = pd.date_range(start=df.index[-1], periods=horyzont + 1, freq=df.index.freq)[1:]
    return pd.concat([pd.Series(prog_hist, index=df.index), pd.Series(prog_fut, index=przyszle_daty)])
