from modele.ARIMA import prognozuj_arima
from pliki_operacje.wczytanie_xlsx import wybor_kolumn
from pliki_operacje.zapis_xlsx import zapisz_prognoze



def main() -> None:
    print("--- Start programu: Generator Szeregów Czasowych ---")

    # 1. Wczytanie i przygotowanie danych
    df, df_przyszle, horyzont = wybor_kolumn()

    if df is not None:
        # 2. Generowanie prognozy
        prognoza = prognozuj_arima(df, df_przyszle, horyzont)

        # 3. Zapis do pliku Excel
        zapisz_prognoze(df, prognoza, nazwa_modelu="ARIMA", horyzont=horyzont)

    print("\n--- Zakończono działanie programu ---")


# TEN FRAGMENT JEST NIEZBĘDNY DO URUCHOMIENIA:
if __name__ == "__main__":
    main()