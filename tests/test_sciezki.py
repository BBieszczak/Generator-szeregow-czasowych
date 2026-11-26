import sys
from pathlib import Path
from unittest.mock import patch
from pliki_operacje.sciezki import katalog_bazowy


def test_katalog_bazowy_skrypt():
    with patch.object(sys, "frozen", False, create=True):
        wynik = katalog_bazowy()
        assert wynik == Path(__file__).resolve().parent.parent


def test_katalog_bazowy_exe(tmp_path):
    fake_exe = tmp_path / "Generator.exe"
    with patch.object(sys, "frozen", True, create=True):
        with patch.object(sys, "executable", str(fake_exe)):
            wynik = katalog_bazowy()
            assert wynik == tmp_path.resolve()
