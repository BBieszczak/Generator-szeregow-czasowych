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

### Zapisanie wyników do Excela

### Generowanie wizualizacji