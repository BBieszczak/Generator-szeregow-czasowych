import pytest
from pathlib import Path
from unittest.mock import patch

from pliki_operacje.wyjatki import wartosc_kolumny, poprawnosc_nazwy_pliku, FOLDER_Z_PLIKAMI


# ==================== TESTY DLA wartosc_kolumny ====================

class TestWartoscKolumny:
    """Testy dla funkcji walidującej oznaczenie kolumny."""

    # --- Poprawne dane ---
    def test_pojedyncza_litera_wielka(self):
        """Kolumna jednoliterowa (np. 'A') powinna przejść bez błędu."""
        wartosc_kolumny("A")  # brak wyjątku = OK

    def test_pojedyncza_litera_mala(self):
        """Kolumna jednoliterowa mała (np. 'b') powinna przejść bez błędu."""
        wartosc_kolumny("b")

    def test_dwie_litery(self):
        """Kolumna dwuliterowa (np. 'AA') powinna przejść bez błędu."""
        wartosc_kolumny("AA")

    def test_dwie_litery_male(self):
        """Kolumna dwuliterowa mała (np. 'ab') powinna przejść bez błędu."""
        wartosc_kolumny("ab")

    # --- Puste wejście ---
    def test_pusty_string(self):
        """Pusty string powinien rzucić ValueError."""
        with pytest.raises(ValueError, match="Oznaczenie kolumny nie może być puste"):
            wartosc_kolumny("")

    # --- Wejście z liczbami ---
    def test_string_z_cyfra(self):
        """Kolumna z cyfrą (np. 'A1') powinna rzucić ValueError."""
        with pytest.raises(ValueError, match="W kolumnach nie ma liczb"):
            wartosc_kolumny("A1")

    def test_sama_cyfra(self):
        """Sama cyfra (np. '1') powinna rzucić ValueError."""
        with pytest.raises(ValueError, match="W kolumnach nie ma liczb"):
            wartosc_kolumny("1")

    def test_cyfra_na_poczatku(self):
        """Cyfra na początku (np. '1A') powinna rzucić ValueError."""
        with pytest.raises(ValueError, match="W kolumnach nie ma liczb"):
            wartosc_kolumny("1A")

    # --- Zbyt długie lub nieprawidłowe oznaczenie ---
    def test_trzy_litery(self):
        """Trzy litery (np. 'ABC') powinny rzucić ValueError."""
        with pytest.raises(ValueError, match="Oznaczenie kolumny jest nieprawidlowe"):
            wartosc_kolumny("ABC")

    def test_cztery_litery(self):
        """Cztery litery powinny rzucić ValueError."""
        with pytest.raises(ValueError, match="Oznaczenie kolumny jest nieprawidlowe"):
            wartosc_kolumny("ABCD")

    def test_znaki_specjalne(self):
        """Znaki specjalne (np. '@#') powinny rzucić ValueError."""
        with pytest.raises(ValueError, match="Oznaczenie kolumny jest nieprawidlowe"):
            wartosc_kolumny("@#")

    def test_spacja(self):
        """Spacja powinna rzucić ValueError."""
        with pytest.raises(ValueError, match="Oznaczenie kolumny jest nieprawidlowe"):
            wartosc_kolumny("A B")


# ==================== TESTY DLA poprawnosc_nazwy_pliku ====================

class TestPoprawnoscNazwyPliku:
    """Testy dla funkcji walidującej nazwę pliku .xlsx."""

    # --- Złe rozszerzenie ---
    def test_plik_csv(self):
        """Plik .csv powinien rzucić ValueError."""
        with pytest.raises(ValueError, match="Plik musi mieć rozszerzenie .xlsx"):
            poprawnosc_nazwy_pliku("dane.csv")

    def test_plik_txt(self):
        """Plik .txt powinien rzucić ValueError."""
        with pytest.raises(ValueError, match="Plik musi mieć rozszerzenie .xlsx"):
            poprawnosc_nazwy_pliku("dane.txt")

    def test_plik_bez_rozszerzenia(self):
        """Plik bez rozszerzenia powinien rzucić ValueError."""
        with pytest.raises(ValueError, match="Plik musi mieć rozszerzenie .xlsx"):
            poprawnosc_nazwy_pliku("dane")

    def test_plik_xls(self):
        """Plik .xls (starszy format) powinien rzucić ValueError."""
        with pytest.raises(ValueError, match="Plik musi mieć rozszerzenie .xlsx"):
            poprawnosc_nazwy_pliku("dane.xls")

    # --- Plik nie istnieje ---
    def test_plik_nie_istnieje(self):
        """Plik .xlsx, który nie istnieje w folderze, powinien rzucić FileNotFoundError."""
        with pytest.raises(FileNotFoundError, match="Nie znaleziono pliku"):
            poprawnosc_nazwy_pliku("nieistniejacy_plik.xlsx")

    # --- Plik istnieje ---
    def test_plik_istnieje(self, tmp_path):
        """Plik .xlsx, który istnieje, powinien zwrócić poprawną ścieżkę."""
        # Podmiana FOLDER_Z_PLIKAMI na folder tymczasowy
        plik = tmp_path / "test_dane.xlsx"
        plik.touch()

        with patch("pliki_operacje.wyjatki.FOLDER_Z_PLIKAMI", tmp_path):
            wynik = poprawnosc_nazwy_pliku("test_dane.xlsx")
            assert wynik == plik
            assert isinstance(wynik, Path)


# ==================== TESTY DLA FOLDER_Z_PLIKAMI ====================

class TestFolderZPlikami:
    """Testy dla stałej FOLDER_Z_PLIKAMI."""

    def test_folder_konczy_sie_na_pliki_do_wczytania(self):
        """Ścieżka folderu powinna kończyć się na 'pliki_do_wczytania'."""
        assert FOLDER_Z_PLIKAMI.name == "pliki_do_wczytania"

    def test_folder_jest_absolutny(self):
        """Ścieżka folderu powinna być absolutna."""
        assert FOLDER_Z_PLIKAMI.is_absolute()
