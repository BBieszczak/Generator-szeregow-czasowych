# Generator szeregów czasowych

## Wymagania i instalacja (PyCharm / terminal)

* **Python:** wersja `3.10` lub nowsza (zalecana `3.13`).
* Umieść plik wejściowy `.xlsx` w folderze `pliki_do_wczytania` (w projekcie znajduje się przykładowy plik `dane.xlsx`).

### Uruchomienie w PyCharmie
1. Pobierz lub sklonuj repozytorium i otwórz folder projektu w PyCharmie.
2. Utwórz lokalne środowisko wirtualne (`.venv`) z posiadanego Pythona (`>= 3.10`): **Settings → Project → Python Interpreter → Add Interpreter → Add Local Interpreter → Virtualenv Environment**.
3. PyCharm zaproponuje instalację zależności z `requirements.txt` (albo uruchom w terminalu PyCharma):
   ```bash
   pip install -r requirements.txt
   ```
4. Uruchom plik `main.py`.

### Uruchomienie testów
```bash
pytest
```

### Budowanie pliku `.exe` (opcjonalnie)
```bash
pip install pyinstaller
pyinstaller --onedir --name GeneratorSzeregowCzasowych main.py
```
Po zbudowaniu w trybie `--onedir` (zalecany dla szybszego uruchamiania) w folderze `dist/GeneratorSzeregowCzasowych/` powstanie plik `.exe`. Przed wysłaniem programu na inne urządzenie umieść obok pliku `.exe` folder `pliki_do_wczytania` z danymi `.xlsx`. Foldery `szeregi_czasowe` i `wykresy` utworzą się automatycznie.

---

## Przebieg programu

### Inicjalizacja i pobranie ustawień
* Uruchomienie pliku main
* Pobieranie od użytkownika danych:
  * Nazwa pliku
  * Odpowiednie kolumny
  * Występowanie regresorów
  * Ilość okresów prognozy (miesięcy/kwartałów/lat)
  
### Oczyszczenie i budowa struktury
* Łączenie wskazanych danych w jedną tabelę
* Przystosowanie dat pod działanie biblioteki pandas
* Ustawienie daty jako indeks tabeli
* Ustalanie odległości między okresami

### Wybór algorytmu i przekierowanie strumienia
* Wskazanie przez użytkownika jednego z dostępnych modeli
* `match case` uruchamia odpowiednią funkcję (z leniwym importem wybranego modelu)

### Trenowanie modelu i generowanie predykcji
* Przejście do modułu z modelami i uruchomienie odpowiedniego pliku
* Generowanie wyniku za pośrednictwem zewnętrznych bibliotek
* LSTM, GRU i TFT - korzystają z Deep Learningu
* Do otrzymanego wyniku generowany jest przedział ufności 

### Zapisanie wyników do Excela
* Utworzenie pliku `.xlsx` zawierającego daty, wartości rzeczywiste oraz predykcję
* Zapisanie pliku `.xlsx` pod nazwą: `model_liczba_okresow.xlsx` (np. `LSTM_5.xlsx`, `ARIMA_3.xlsx`) w folderze `szeregi_czasowe`
* Uwaga: regresory nie są zapisywane w pliku!

### Generowanie wizualizacji
* Utworzenie pliku `.png` zawierającego wizualizację wykresu rzeczywistego oraz predykcji
* Zapisanie pliku `.png` pod nazwą: `model_liczba_okresow.png` (np. `LSTM_5.png`, `ARIMA_3.png`) w folderze `wykresy`
