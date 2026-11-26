__all__ = [
    "wybor_kolumn",
    "zapisz_prognoze",
    "zapisz_wykres",
    "oblicz_przedzial_ufnosci",
]


def __getattr__(name: str):
    """Leniwe ładowanie funkcji pakietu, aby uniknąć wczytywania ciężkich bibliotek przy starcie."""
    if name == "wybor_kolumn":
        from .wczytanie_xlsx import wybor_kolumn

        return wybor_kolumn
    if name == "zapisz_prognoze":
        from .zapis_xlsx import zapisz_prognoze

        return zapisz_prognoze
    if name == "zapisz_wykres":
        from .generowanie_wykresu import zapisz_wykres

        return zapisz_wykres
    if name == "oblicz_przedzial_ufnosci":
        from .przedzial_ufnosci import oblicz_przedzial_ufnosci

        return oblicz_przedzial_ufnosci
    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")
