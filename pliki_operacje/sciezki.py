import sys
from pathlib import Path


def katalog_bazowy() -> Path:
    """Zwraca katalog główny programu (obok pliku .exe lub katalog projektu)."""
    if getattr(sys, "frozen", False):
        return Path(sys.executable).resolve().parent
    return Path(__file__).resolve().parent.parent
