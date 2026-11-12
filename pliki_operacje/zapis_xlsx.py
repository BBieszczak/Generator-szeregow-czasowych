import pandas as pd
from pliki_operacje.bledy import wartosc_kolumny


def wybor_kolumn() -> None:
    print("Podaj nazwe pliku, który chcesz wprowadzić. Pamietaj o napisaniu jego roszerzena np. dane.xlsx")
    nazwa_pliku = input("Wprowadz nazwe").lower()
    try:
        czas = input("Pod litere kolumny z czasem").upper()
        wartosc_kolumny(czas)
        czas = pd.read_excel(nazwa_pliku,usecols= czas)
    except ValueError as e:
        print("Blad", e)
    wartosci = None
    regresory  = None

