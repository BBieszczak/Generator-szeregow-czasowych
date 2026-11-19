from pathlib import Path


def wartosc_kolumny(kolumna: str) -> None:
    if not kolumna:
        raise ValueError("Oznaczenie kolumny nie może być puste!")

    if any(znak.isdigit() for znak in kolumna):
        raise ValueError("W kolumnach nie ma liczb! Powinienes wpisac np. C, AA lub E")

    if not kolumna.isalpha() or len(kolumna) > 2:
        raise ValueError("Oznaczenie kolumny jest nieprawidlowe! Powinienes wpisac np. C, AA lub E")

# Ścieżka do folderu pliki_do_wczytania
FOLDER_Z_PLIKAMI = Path(__file__).resolve().parent.parent / "pliki_do_wczytania"


def poprawnosc_nazwy_pliku(nazwa_pliku: str) -> Path:
    if not nazwa_pliku.endswith(".xlsx"):
        raise ValueError("Plik musi mieć rozszerzenie .xlsx")

    sciezka = FOLDER_Z_PLIKAMI / nazwa_pliku

    if not sciezka.is_file():
        raise FileNotFoundError(f"Nie znaleziono pliku '{nazwa_pliku}' w folderze '{FOLDER_Z_PLIKAMI.name}'")

    return sciezka
