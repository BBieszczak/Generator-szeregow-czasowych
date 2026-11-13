import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path

# Zmieniono folder docelowy na "wykresy"
FOLDER_ZAPISU = Path(__file__).resolve().parent.parent / "wykresy"


def zapisz_wykres(df: pd.DataFrame, prognoza: pd.Series, nazwa_modelu: str, horyzont: int) -> None:
    nazwa_y = df.columns[0]

    plt.figure(figsize=(12, 6))

    # Rysowanie linii
    plt.plot(df.index, df[nazwa_y], label='Wartość rzeczywista', color='#8B5FBF', linewidth=2.5)
    plt.plot(prognoza.index, prognoza, label='Predykcja', color='#2E8B57', linestyle='--', linewidth=2.5)

    # Formatowanie wykresu
    plt.title(f"Porównanie: {nazwa_modelu} (Prognoza na {horyzont} okresów)")
    plt.xlabel("Data")
    plt.ylabel(nazwa_y)
    plt.legend()
    plt.grid(True, linestyle=':', alpha=0.7)

    plt.xticks(rotation=45)
    plt.tight_layout()

    # Zapis do pliku
    nazwa_pliku = f"{nazwa_modelu}_{horyzont}.png"
    sciezka = FOLDER_ZAPISU / nazwa_pliku

    FOLDER_ZAPISU.mkdir(exist_ok=True)  # Tworzy folder "wykresy", jeśli nie istnieje
    plt.savefig(sciezka, dpi=300)
    plt.close()

    print(f"[Zapis] Pomyślnie utworzono wykres: {sciezka}")