import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import pandas as pd
from .przedzial_ufnosci import oblicz_przedzial_ufnosci
from .sciezki import katalog_bazowy

# Folder docelowy na wykresy
FOLDER_ZAPISU = katalog_bazowy() / "wykresy"


def zapisz_wykres(
    df: pd.DataFrame,
    prognoza: pd.Series,
    nazwa_modelu: str,
    horyzont: int,
    przedzial_ufnosci: tuple[pd.Series, pd.Series] | None = None,
) -> None:
    nazwa_y = df.columns[0]

    plt.figure(figsize=(12, 6))

    # Rysowanie linii rzeczywistej i prognozy
    plt.plot(df.index, df[nazwa_y], label="Wartość rzeczywista", color="#8B5FBF", linewidth=2.5)
    plt.plot(prognoza.index, prognoza, label="Predykcja", color="#2E8B57", linestyle="--", linewidth=2.5)

    # Przedział ufności dla horyzontu przyszłego
    if przedzial_ufnosci is None and horyzont > 0:
        przedzial_ufnosci = oblicz_przedzial_ufnosci(df, prognoza, horyzont)

    if przedzial_ufnosci is not None:
        dolna, gorna = przedzial_ufnosci
        if not dolna.empty and not gorna.empty:
            proc = dolna.name.split("(")[-1].rstrip(")") if "(" in dolna.name else "95%"
            plt.fill_between(
                dolna.index,
                dolna,
                gorna,
                color="#2E8B57",
                alpha=0.2,
                label=f"Przedział ufności ({proc})",
            )
            plt.plot(dolna.index, dolna, color="#2E8B57", linestyle=":", linewidth=1.2, alpha=0.6)
            plt.plot(gorna.index, gorna, color="#2E8B57", linestyle=":", linewidth=1.2, alpha=0.6)

    # Formatowanie wykresu
    plt.title(f"Porównanie: {nazwa_modelu} (Prognoza na {horyzont} okresów)")
    plt.xlabel("Data")
    plt.ylabel(nazwa_y)
    plt.legend()
    plt.grid(True, linestyle=":", alpha=0.7)

    plt.xticks(rotation=45)
    plt.tight_layout()

    # Zapis do pliku
    nazwa_pliku = f"{nazwa_modelu}_{horyzont}.png"
    sciezka = FOLDER_ZAPISU / nazwa_pliku

    FOLDER_ZAPISU.mkdir(parents=True, exist_ok=True)
    plt.savefig(sciezka, dpi=300)
    plt.close()

    print(f"[Zapis] Pomyślnie utworzono wykres: {sciezka}")
