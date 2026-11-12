from pathlib import Path


def wartosc_kolumny(kolumna: str) -> None:

    zawiera_liczbe = any(znak.isdigit() for znak in kolumna)
    if zawiera_liczbe:
        raise ValueError("W kolumach nie ma liczb! Powinienes wpisac np. C, AA lub E")

    if len(kolumna) > 2:
        raise ValueError("Oznaczenie kolumny jest nie prawidlowe! Powinienes wpisac np. C, AA lub E")

def poprawnosc_nazwy_pliku(nazwa_pliku: str) -> None:
    if not nazwa_pliku.lower().endswith(".xlsx"):
        raise ValueError("Wskazany plik musi mieć rozszerzenie .xlsx!")

    FOLDER_Z_PLIKAMI = (
        Path(__file__).resolve().parent.parent / "pliki_do_wczytania"
    )

    if not nazwa_pliku.endswith(".xlsx"):
        nazwa_pliku += ".xlsx"

    sciezka = FOLDER_Z_PLIKAMI / nazwa_pliku

    # Sprawdzenie czy plik istnieje
    if not sciezka.is_file():
        raise FileNotFoundError(
            f"Plik '{nazwa_pliku}' nie istnieje w folderze 'pliki_do_wczytania'!"
        )
