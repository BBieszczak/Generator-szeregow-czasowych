from modele.ARIMA import prognozuj_arima
from pliki_operacje.wczytanie_xlsx import wybor_kolumn



def main() -> None:
    print("--- Start programu: Generator Szeregów Czasowych ---")

    # 1. Pobieranie i formatowanie danych
    df, df_przyszle, horyzont = wybor_kolumn()

    # 2. Jeśli dane wczytały się poprawnie, uruchom model ARIMA
    if df is not None:
        prognozuj_arima(df, df_przyszle, horyzont)

    print("\n--- Zakończono działanie programu ---")


if __name__ == "__main__":
    main()