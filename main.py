from pliki_operacje import wybor_kolumn, zapisz_prognoze, zapisz_wykres
from modele.ARIMA import prognozuj_arima
from modele.ARDL import prognozuj_ardl
from modele.BTST import prognozuj_btst
from modele.CROSTON import prognozuj_croston



def main() -> None:
    print("--- Start programu: Generator Szeregów Czasowych ---")

    # 1. Wczytanie i przygotowanie danych
    wyniki = wybor_kolumn()

    # Zabezpieczenie na wypadek, gdyby wybor_kolumn() zwróciło błąd
    if wyniki[0] is None:
        print("\nBłąd podczas wczytywania danych. Zatrzymuję program.")
        return

    df, df_przyszle, horyzont = wyniki

    # 2. Wybór modelu przez użytkownika
    print("\nDostępne modele:")
    print(" 1. ARIMA       6. ETS         11. NNAR       16. STS")
    print(" 2. ARDL        7. GAM         12. PROPHET    17. TFT")
    print(" 3. BTST        8. GAMLSS      13. SARIMA     18. THETA")
    print(" 4. CROSTON     9. GRU         14. SARIMAX    19. XG_BOOST")
    print(" 5. DHR        10. LSTM        15. STLS")

    modele_mapa = {
        "1": "ARIMA", "2": "ARDL", "3": "BTST", "4": "CROSTON", "5": "DHR",
        "6": "ETS", "7": "GAM", "8": "GAMLSS", "9": "GRU", "10": "LSTM",
        "11": "NNAR", "12": "PROPHET", "13": "SARIMA", "14": "SARIMAX",
        "15": "STLS", "16": "STS", "17": "TFT", "18": "THETA", "19": "XG_BOOST",
    }

    wybor = input("\nWpisz nazwę lub numer modelu (np. ARIMA lub 1): ").strip().upper()
    wybor = modele_mapa.get(wybor.rstrip("."), wybor)

    prognoza = None
    nazwa_modelu = wybor

    # 3. match case do obsługi wyboru każdego z plików
    match wybor:
        case "ARIMA":
            prognoza = prognozuj_arima(df, df_przyszle, horyzont)

        case "ARDL":
            prognoza = prognozuj_ardl(df, df_przyszle, horyzont)

        case "BTST":
            prognoza = prognozuj_btst(df, df_przyszle, horyzont)

        case "CROSTON":
            prognoza = prognozuj_croston(df, df_przyszle, horyzont)

        case "DHR":
            print(f"\nUruchamianie modelu {wybor}... (Wymaga uzupełnienia pliku {wybor}.py)")

        case "ETS":
            print(f"\nUruchamianie modelu {wybor}... (Wymaga uzupełnienia pliku {wybor}.py)")

        case "GAM":
            print(f"\nUruchamianie modelu {wybor}... (Wymaga uzupełnienia pliku {wybor}.py)")

        case "GAMLSS":
            print(f"\nUruchamianie modelu {wybor}... (Wymaga uzupełnienia pliku {wybor}.py)")

        case "GRU":
            print(f"\nUruchamianie modelu {wybor}... (Wymaga uzupełnienia pliku {wybor}.py)")

        case "LSTM":
            print(f"\nUruchamianie modelu {wybor}... (Wymaga uzupełnienia pliku {wybor}.py)")

        case "NNAR":
            print(f"\nUruchamianie modelu {wybor}... (Wymaga uzupełnienia pliku {wybor}.py)")

        case "PROPHET":
            print(f"\nUruchamianie modelu {wybor}... (Wymaga uzupełnienia pliku {wybor}.py)")

        case "SARIMA":
            print(f"\nUruchamianie modelu {wybor}... (Wymaga uzupełnienia pliku {wybor}.py)")

        case "SARIMAX":
            print(f"\nUruchamianie modelu {wybor}... (Wymaga uzupełnienia pliku {wybor}.py)")

        case "STLS":
            print(f"\nUruchamianie modelu {wybor}... (Wymaga uzupełnienia pliku {wybor}.py)")

        case "STS":
            print(f"\nUruchamianie modelu {wybor}... (Wymaga uzupełnienia pliku {wybor}.py)")

        case "TFT":
            print(f"\nUruchamianie modelu {wybor}... (Wymaga uzupełnienia pliku {wybor}.py)")

        case "THETA":
            print(f"\nUruchamianie modelu {wybor}... (Wymaga uzupełnienia pliku {wybor}.py)")

        case "XG_BOOST":
            print(f"\nUruchamianie modelu {wybor}... (Wymaga uzupełnienia pliku {wybor}.py)")

        case _:
            print(f"\nBłąd: Nie rozpoznano modelu '{wybor}'. Upewnij się, że nazwa została wpisana poprawnie.")

    # 4. Zapis wyników (Tabela .xlsx oraz Wykres .png)
    if prognoza is not None:
        zapisz_prognoze(df, prognoza, nazwa_modelu, horyzont)
        zapisz_wykres(df, prognoza, nazwa_modelu, horyzont)
        print(f"\nGenerowanie plików dla modelu {nazwa_modelu} zakończone pomyślnie.")
    else:
        if wybor in ["ARIMA", "ARDL", "BTST", "CROSTON"]:  # Lista gotowych modeli
            print("\nWystąpił problem z wygenerowaniem prognozy.")
        else:
            print(f"\nModel {wybor} nie wygenerował danych, ponieważ jego logika nie została jeszcze napisana.")

    print("\n--- Zakończono działanie programu ---")


if __name__ == "__main__":
    main()