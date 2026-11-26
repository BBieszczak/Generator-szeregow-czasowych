import pandas as pd
from unittest.mock import patch
from main import main


def test_main_blad_wczytania():
    with patch("main.wybor_kolumn", return_value=(None, None, 0)):
        with patch("builtins.input") as mock_input:
            main()
            mock_input.assert_not_called()


def test_main_arima_sukces():
    df = pd.DataFrame({"Y": [1, 2, 3]}, index=pd.date_range("2020-01-01", periods=3, freq="MS"))
    prognoza = pd.Series([1, 2, 3, 4], index=pd.date_range("2020-01-01", periods=4, freq="MS"))

    with patch("main.wybor_kolumn", return_value=(df, None, 1)):
        with patch("builtins.input", return_value="arima"):
            with patch("modele.ARIMA.prognozuj_arima", return_value=prognoza) as mock_arima:
                with patch("pliki_operacje.zapis_xlsx.zapisz_prognoze") as mock_zapis_prog:
                    with patch("pliki_operacje.generowanie_wykresu.zapisz_wykres") as mock_zapis_wyk:
                        main()
                        mock_arima.assert_called_once()
                        mock_zapis_prog.assert_called_once()
                        mock_zapis_wyk.assert_called_once()


def test_main_wybor_numerem():
    df = pd.DataFrame({"Y": [1, 2, 3]}, index=pd.date_range("2020-01-01", periods=3, freq="MS"))
    prognoza = pd.Series([1, 2, 3, 4], index=pd.date_range("2020-01-01", periods=4, freq="MS"))

    with patch("main.wybor_kolumn", return_value=(df, None, 1)):
        with patch("builtins.input", return_value="2"):  # 2 = ARDL
            with patch("modele.ARDL.prognozuj_ardl", return_value=prognoza) as mock_ardl:
                with patch("pliki_operacje.zapis_xlsx.zapisz_prognoze") as mock_zapis:
                    with patch("pliki_operacje.generowanie_wykresu.zapisz_wykres"):
                        main()
                        mock_ardl.assert_called_once()
                        mock_zapis.assert_called_once_with(df, prognoza, "ARDL", 1)
