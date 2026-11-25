# Generator szeregow czasowych

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
* Ostalanie ogległości między okresami

### Wybór algorytmu i przekierowanie strumienia
* Wskazanie przez użytkownika jedno z dostępnych modeli
* Match case uruchamia odpowiednią funkcje

### Trenowanie modelu i generowanie predykcji
* Przejście do modułu z modelami i uruchmoienie odpowiedniego pliku
* Generowanie wyniku za pośrednictwem zewnętrznych bibliotek
* LSTM, GRU i TFT - korzystają z Deep Learningu
* Przesłanie danych dalej

### Zapisanie wyników do Excela
* Utworzenie pliku .xlsx zawierającego wartości date, wartości rzeczywsite oraz predykcje
* Zapisanie pliku .xlsx pod nazwą: model_liczba okresów.xlsx (np. LSTM_5.xlsx, ARIMA_3.xlsx) w folderze szeregi_czasowe
* Uwaga regresory nie są zapisywane w pliku!
### Generowanie wizualizacji
* Utworzenie pliku .png zawierającego wizualizację wykresu rzeczywsitego oraz predykcji
* Zapisanie pliku .png pod nazwą: model_liczba okresów.png (np. LSTM_5.png, ARIMA_3.png) w folderze wykresy