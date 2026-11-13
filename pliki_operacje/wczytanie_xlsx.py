import pandas as pd
from pliki_operacje.bledy import poprawnosc_nazwy_pliku, wartosc_kolumny


# --- 1. POBIERANIE DANYCH OD UŻYTKOWNIKA ---
def zapytaj_o_dane():
    sciezka = poprawnosc_nazwy_pliku(input("Nazwa pliku (np. dane.xlsx): ").strip())

    czas = input("Kolumna z czasem (np. A): ").strip().upper()
    wartosc_kolumny(czas)

    y = input("Kolumna z wartościami Y (np. B): ").strip().upper()
    wartosc_kolumny(y)

    ile_reg = int(input("Ile regresorów? (0 jeśli brak): "))
    regresory = []
    for i in range(ile_reg):
        kol = input(f"Kolumna regresora {i + 1}: ").strip().upper()
        wartosc_kolumny(kol)
        regresory.append(kol)

    jednostka = input("Częstotliwość [M]iesiące, [K]wartały, [R]oki: ").strip().upper()
    horyzont = int(input("Na ile okresów w przód prognoza?: "))

    return sciezka, czas, y, regresory, jednostka, horyzont


# --- 2. BUDOWANIE I CZYSZCZENIE SZEREGU ---
def buduj_szereg_historyczny(sciezka, czas, y, regresory, jednostka):
    kolumny = [czas, y] + regresory
    df = pd.concat([pd.read_excel(sciezka, usecols=k) for k in kolumny], axis=1)
    nazwa_czasu = df.columns[0]

    # Parsowanie daty
    try:
        df[nazwa_czasu] = pd.to_datetime(df[nazwa_czasu])
    except ValueError:
        df[nazwa_czasu] = pd.to_datetime(df[nazwa_czasu].astype(str).str.strip(), format="%YM%m")

    # Ustawianie indeksu
    df = df.sort_values(by=nazwa_czasu).set_index(nazwa_czasu)
    df = df.asfreq({"M": "MS", "K": "QS", "R": "YS"}.get(jednostka, "MS"))

    # Zamiana przecinków na kropki (jeśli dane pobrały się jako tekst)
    for kol in df.columns:
        if df[kol].dtype == object:
            df[kol] = df[kol].astype(str).str.replace(" ", "").str.replace(",", ".")
        df[kol] = pd.to_numeric(df[kol])

    return df


# --- 3. WPROWADZANIE PRZYSZŁYCH REGRESORÓW ---
def wprowadz_przyszle_regresory(df, horyzont, liczba_regresorow):
    if liczba_regresorow == 0:
        return None

    nazwy_reg = df.columns[1:]  # Wszystkie kolumny poza zmienną główną (Y)
    przyszle_daty = pd.date_range(start=df.index[-1], periods=horyzont + 1, freq=df.index.freq)[1:]

    print("\n--- Wprowadzanie wartości regresorów na przyszłość ---")
    dane = {reg: [] for reg in nazwy_reg}

    for data in przyszle_daty:
        print(f"\nData prognozy: {data.date()}")
        for reg in nazwy_reg:
            wartosc = input(f"Podaj wartość dla '{reg}': ").replace(",", ".")
            dane[reg].append(float(wartosc))

    df_przyszle = pd.DataFrame(dane, index=przyszle_daty)
    df_przyszle.index.name = df.index.name

    return df_przyszle


# === GŁÓWNA FUNKCJA ===
def wybor_kolumn():
    try:
        sciezka, czas, y, reg, jedn, horyzont = zapytaj_o_dane()

        df = buduj_szereg_historyczny(sciezka, czas, y, reg, jedn)

        df_przyszle = wprowadz_przyszle_regresory(df, horyzont, len(reg))

        print("\n[Sukces] Dane wczytane poprawnie.")
        return df, df_przyszle, horyzont

    except Exception as e:
        print(f"\nBłąd programu: {e}")
        return None, None, 0