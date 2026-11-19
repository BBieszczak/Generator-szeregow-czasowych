import numpy as np
import pandas as pd
from pygam import LinearGAM, s


def prognozuj_gam(df: pd.DataFrame, df_przyszle: pd.DataFrame | None, horyzont: int) -> pd.Series:
    print("\n--- Trenowanie modelu GAM (Generalized Additive Model) ---")
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
        gam = LinearGAM(formula).fit(X_hist, y)
    else:
        X_hist = t_hist
        X_all = np.arange(n + horyzont).reshape(-1, 1)
        gam = LinearGAM(s(0)).fit(X_hist, y)

    przyszle_daty = pd.date_range(start=df.index[-1], periods=horyzont + 1, freq=df.index.freq)[1:]
    pelen_indeks = df.index.append(przyszle_daty)

    pred_all = gam.predict(X_all)
    return pd.Series(pred_all, index=pelen_indeks)
