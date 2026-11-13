import pandas as pd
from pliki_operacje.bledy import wartosc_kolumny, poprawnosc_nazwy_pliku


def wybor_kolumn() -> None:
    print(
        "Podaj nazwe pliku, który chcesz wprowadzić. Pamietaj o napisaniu jego roszerzena np. dane.xlsx"
    )
    nazwa_pliku = input("Wprowadz nazwe: ").strip().lower()

    try:
        # Przypisujemy zwrócony Path z poprawnosc_nazwy_pliku do zmiennej plik
        plik = poprawnosc_nazwy_pliku(nazwa_pliku)
    except (ValueError, FileNotFoundError) as e:
        print("Blad: ", e)
        return

    try:
        czas = input("Pod litere kolumny z czasem: ").upper().strip()
        wartosc_kolumny(czas)
        czas_df = pd.read_excel(plik, usecols=czas)

        wartosci = input("Podaj pole z wartosciami dla szeregu: ").upper().strip()
        wartosc_kolumny(wartosci)
        wartosci_df = pd.read_excel(plik, usecols=wartosci)

        regresory: list[pd.DataFrame] = []
        ilosc_regresorow = int(input("Ile regresorow chcesz wprowadzic?: "))

        for i in range(ilosc_regresorow):
            kolumna = input(f"Podaj oznaczenie kolumny {i+1}: ").upper().strip()
            wartosc_kolumny(kolumna)
            regresory.append(pd.read_excel(plik, usecols=kolumna))

        print(czas_df, wartosci_df)
        for reg in regresory:
            print(reg)

    except ValueError as e:
        print("Blad: ", e)