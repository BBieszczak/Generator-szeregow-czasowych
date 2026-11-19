import pytest
from pathlib import Path
from unittest.mock import patch
from pliki_operacje.wyjatki import wartosc_kolumny, poprawnosc_nazwy_pliku


@pytest.mark.parametrize("kolumna", ["A", "b", "AA", "ab"])
def test_wartosc_kolumny_poprawna(kolumna):
    wartosc_kolumny(kolumna)


@pytest.mark.parametrize("kolumna", ["", "1", "A1", "ABC", "@#", "A B"])
def test_wartosc_kolumny_niepoprawna(kolumna):
    with pytest.raises(ValueError):
        wartosc_kolumny(kolumna)


@pytest.mark.parametrize("nazwa", ["plik.csv", "plik.txt", "plik", "plik.xls"])
def test_poprawnosc_nazwy_pliku_zle_rozszerzenie(nazwa):
    with pytest.raises(ValueError, match="Plik musi mieć rozszerzenie .xlsx"):
        poprawnosc_nazwy_pliku(nazwa)


def test_poprawnosc_nazwy_pliku_nie_istnieje():
    with pytest.raises(FileNotFoundError):
        poprawnosc_nazwy_pliku("brak.xlsx")


def test_poprawnosc_nazwy_pliku_istnieje(tmp_path):
    (tmp_path / "dane.xlsx").touch()
    with patch("pliki_operacje.wyjatki.FOLDER_Z_PLIKAMI", tmp_path):
        sciezka = poprawnosc_nazwy_pliku("dane.xlsx")
        assert sciezka.is_file()
