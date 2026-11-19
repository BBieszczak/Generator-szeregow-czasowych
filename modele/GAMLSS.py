import numpy as np
import pandas as pd
from pygam import ExpectileGAM, s


def prognozuj_gamlss(df: pd.DataFrame, df_przyszle: pd.DataFrame | None, horyzont: int) -> pd.Series:
    print("\n--- Trenowanie modelu GAMLSS (ExpectileGAM) ---")
    y = df.iloc[:, 0].to_numpy(dtype=float)
    n = len(y)
    exog_user_hist = df.iloc[:, 1:].to_numpy(dtype=float) if df.shape[1] > 1 else None

    t_hist = np.arange(n).reshape(-1, 1)

    if exog_user_hist is not None:
        X_hist = np.column_stack([t_hist, exog_user_hist])
        t_fut = np.arange(n, n + horyzont).reshape(-1, 1)
        exog_user_fut = df_przyszle.to_numpy(dtype=float)
        X_fut = np.column_stack([t_fut, exog_user_fut])
        X_all = np.vstack([X_hist, X_fut])

        formula = s(0)
        for col_idx in range(1, X_hist.shape[1]):
            formula += s(col_idx)
        gam = ExpectileGAM(formula, expectile=0.5).fit(X_hist, y)
    else:
        X_hist = t_hist
        X_all = np.arange(n + horyzont).reshape(-1, 1)
        gam = ExpectileGAM(s(0), expectile=0.5).fit(X_hist, y)

    przyszle_daty = pd.date_range(start=df.index[-1], periods=horyzont + 1, freq=df.index.freq)[1:]
    pelen_indeks = df.index.append(przyszle_daty)

    pred_all = gam.predict(X_all)
    return pd.Series(pred_all, index=pelen_indeks)
