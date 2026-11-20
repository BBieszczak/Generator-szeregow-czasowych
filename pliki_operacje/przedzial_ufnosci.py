import numpy as np
import pandas as pd
from scipy import stats


def oblicz_przedzial_ufnosci(
    df: pd.DataFrame, prognoza: pd.Series, horyzont: int, poziom: float = 0.95
) -> tuple[pd.Series, pd.Series]:
    """Oblicza dolną i górną granicę przedziału ufności dla prognozy na horyzont przyszły.

    Wykorzystuje odchylenie standardowe błędów resztowych (residuals) na danych historycznych
    oraz standardowe rozszerzanie niepewności w czasie (sqrt(h)).
    """
    if horyzont <= 0 or len(prognoza) <= len(df):
        puste = pd.Series(dtype=float)
        return puste, puste

    y_hist = df.iloc[:, 0].to_numpy(dtype=float)
    daty_hist = df.index
    prog_hist = prognoza.loc[daty_hist].to_numpy(dtype=float)

    reszty = y_hist - prog_hist
    se = float(np.std(reszty, ddof=1)) if len(reszty) > 1 else float(np.std(reszty))
    if np.isnan(se) or se == 0:
        se = float(np.std(y_hist)) * 0.05 if np.std(y_hist) > 0 else 1.0

    z = float(stats.norm.ppf(1 - (1 - poziom) / 2))

    fut_daty = prognoza.index[-horyzont:]
    prog_fut = prognoza.loc[fut_daty].to_numpy(dtype=float)

    kroki = np.arange(1, horyzont + 1)
    margines = z * se * np.sqrt(kroki)

    etykieta_proc = f"{int(poziom * 100)}%"
    dolna = pd.Series(prog_fut - margines, index=fut_daty, name=f"Dolna granica ({etykieta_proc})")
    gorna = pd.Series(prog_fut + margines, index=fut_daty, name=f"Górna granica ({etykieta_proc})")

    return dolna, gorna
