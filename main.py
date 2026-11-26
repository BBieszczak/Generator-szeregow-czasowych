from pliki_operacje import wybor_kolumn



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

    # 3. Leniwy import i uruchomienie wybranego modelu
    match wybor:
        case "ARIMA":
            from modele.ARIMA import prognozuj_arima

            prognoza = prognozuj_arima(df, df_przyszle, horyzont)

        case "ARDL":
            from modele.ARDL import prognozuj_ardl

            prognoza = prognozuj_ardl(df, df_przyszle, horyzont)

        case "BTST":
            from modele.BTST import prognozuj_btst

            prognoza = prognozuj_btst(df, df_przyszle, horyzont)

        case "CROSTON":
            from modele.CROSTON import prognozuj_croston

            prognoza = prognozuj_croston(df, df_przyszle, horyzont)

        case "DHR":
            from modele.DHR import prognozuj_dhr

            prognoza = prognozuj_dhr(df, df_przyszle, horyzont)

        case "ETS":
            from modele.ETS import prognozuj_ets

            prognoza = prognozuj_ets(df, df_przyszle, horyzont)

        case "GAM":
            from modele.GAM import prognozuj_gam

            prognoza = prognozuj_gam(df, df_przyszle, horyzont)

        case "GAMLSS":
            from modele.GAMLSS import prognozuj_gamlss

            prognoza = prognozuj_gamlss(df, df_przyszle, horyzont)

        case "GRU":
            from modele.GRU import prognozuj_gru

            prognoza = prognozuj_gru(df, df_przyszle, horyzont)

        case "LSTM":
            from modele.LSTM import prognozuj_lstm

            prognoza = prognozuj_lstm(df, df_przyszle, horyzont)

        case "NNAR":
            from modele.NNAR import prognozuj_nnar

            prognoza = prognozuj_nnar(df, df_przyszle, horyzont)

        case "PROPHET":
            from modele.PROPHET import prognozuj_prophet

            prognoza = prognozuj_prophet(df, df_przyszle, horyzont)

        case "SARIMA":
            from modele.SARIMA import prognozuj_sarima

            prognoza = prognozuj_sarima(df, df_przyszle, horyzont)

        case "SARIMAX":
            from modele.SARIMAX import prognozuj_sarimax

            prognoza = prognozuj_sarimax(df, df_przyszle, horyzont)

        case "STLS":
            from modele.STLS import prognozuj_stls

            prognoza = prognozuj_stls(df, df_przyszle, horyzont)

        case "STS":
            from modele.STS import prognozuj_sts

            prognoza = prognozuj_sts(df, df_przyszle, horyzont)

        case "TFT":
            from modele.TFT import prognozuj_tft

            prognoza = prognozuj_tft(df, df_przyszle, horyzont)

        case "THETA":
            from modele.THETA import prognozuj_theta

            prognoza = prognozuj_theta(df, df_przyszle, horyzont)

        case "XG_BOOST":
            from modele.XG_Boost import prognozuj_xgboost

            prognoza = prognozuj_xgboost(df, df_przyszle, horyzont)

        case _:
            print(f"\nBłąd: Nie rozpoznano modelu '{wybor}'. Upewnij się, że nazwa została wpisana poprawnie.")

    # 4. Zapis wyników (Tabela .xlsx oraz Wykres .png)
    if prognoza is not None:
        from pliki_operacje.zapis_xlsx import zapisz_prognoze
        from pliki_operacje.generowanie_wykresu import zapisz_wykres

        zapisz_prognoze(df, prognoza, nazwa_modelu, horyzont)
        zapisz_wykres(df, prognoza, nazwa_modelu, horyzont)
        print(f"\nGenerowanie plików dla modelu {nazwa_modelu} zakończone pomyślnie.")
    else:
        if wybor in ["ARIMA", "ARDL", "BTST", "CROSTON", "DHR", "ETS", "GAM", "GAMLSS", "GRU", "LSTM", "NNAR", "PROPHET", "SARIMA", "SARIMAX", "STLS", "STS", "TFT", "THETA", "XG_BOOST"]:  # Lista gotowych modeli
            print("\nWystąpił problem z wygenerowaniem prognozy.")
        else:
            print(f"\nModel {wybor} nie wygenerował danych, ponieważ jego logika nie została jeszcze napisana.")

    print("\n--- Zakończono działanie programu ---")


if __name__ == "__main__":
    main()