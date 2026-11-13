import pandas as pd
from pathlib import Path

FOLDER_ZAPISU = Path(__file__).resolve().parent.parent / "szeregi_czasowe"


def zapisz_prognoze(df: pd.DataFrame, prognoza: pd.Series, nazwa_modelu: str, horyzont: int) -> None:
    nazwa_y = df.columns[0]

    # 1. Wyciągnięcie danych historycznych z odpowiednią nazwą z wykresu
    df_hist = df[[nazwa_y]].copy()
    df_hist.columns = ['Wartość rzeczywista']

    # 2. Przygotowanie pełnej prognozy jako kolumny
    df_prog = prognoza.to_frame(name='Predykcja')

    # 3. Złączenie po datach (outer join zapewni, że daty przyszłe też wejdą do tabeli)
    wynik = df_hist.join(df_prog, how='outer')

    # 4. Tworzenie nazwy pliku i zapis
    nazwa_pliku = f"{nazwa_modelu}_{horyzont}.xlsx"
    sciezka = FOLDER_ZAPISU / nazwa_pliku

    FOLDER_ZAPISU.mkdir(exist_ok=True)
    wynik.to_excel(sciezka, index_label="Data")

    print(f"\n[Zapis] Pomyślnie utworzono plik z pełną predykcją: {sciezka}")