import openpyxl  # noqa: F401 - wymagane dla PyInstaller przy dynamicznym imporcie w pandas
import pandas as pd
from .przedzial_ufnosci import oblicz_przedzial_ufnosci
from .sciezki import katalog_bazowy

FOLDER_ZAPISU = katalog_bazowy() / "szeregi_czasowe"


def zapisz_prognoze(
    df: pd.DataFrame,
    prognoza: pd.Series,
    nazwa_modelu: str,
    horyzont: int,
    przedzial_ufnosci: tuple[pd.Series, pd.Series] | None = None,
) -> None:
    nazwa_y = df.columns[0]

    # 1. Wyciągnięcie danych historycznych
    df_hist = df[[nazwa_y]].copy()
    df_hist.columns = ["Wartość rzeczywista"]

    # 2. Przygotowanie pełnej prognozy jako kolumny
    df_prog = prognoza.to_frame(name="Predykcja")

    # 3. Dodanie przedziałów ufności dla przyszłych obserwacji
    if przedzial_ufnosci is None and horyzont > 0:
        przedzial_ufnosci = oblicz_przedzial_ufnosci(df, prognoza, horyzont)

    if przedzial_ufnosci is not None:
        dolna, gorna = przedzial_ufnosci
        if not dolna.empty and not gorna.empty:
            df_prog[dolna.name] = dolna
            df_prog[gorna.name] = gorna

    # 4. Złączenie po datach
    wynik = df_hist.join(df_prog, how="outer")

    # 5. Tworzenie nazwy pliku i zapis
    nazwa_pliku = f"{nazwa_modelu}_{horyzont}.xlsx"
    sciezka = FOLDER_ZAPISU / nazwa_pliku

    FOLDER_ZAPISU.mkdir(parents=True, exist_ok=True)
    wynik.to_excel(sciezka, index_label="Data", engine="openpyxl")

    print(f"\n[Zapis] Pomyślnie utworzono plik z pełną predykcją: {sciezka}")
