import json
import datetime as dt
from pathlib import Path

jeu = input("Nom du jeu (ets2/ats) : ").strip()
JSON_FILE = Path(f"{jeu}_maps_dlc.json")

def recuperer_date(prompt):
    """
    Demande une date à l'utilisateur et la convertit en datetime.
    Accepte plusieurs formats (ex : 2024-11-01 ou 1/11/2024).
    """
    while True:
        date_str = input(prompt + " (format JJ/MM/AAAA) : ").strip()
        try:
            return dt.datetime.strptime(date_str, "%d/%m/%Y")
        except ValueError:
            print("Format invalide. Exemple attendu : 01/11/2025")

def recuperer_json():
    """
    Charge le JSON existant s'il est présent, sinon retourne une liste vide.
    """
    if JSON_FILE.exists():
        try:
            with open(JSON_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)
                print(f"{len(data)} DLC(s) déjà présent(s) dans {JSON_FILE.name}")
                return data
        except json.JSONDecodeError:
            print("Fichier JSON corrompu ou vide. Un nouveau sera créé.")
            return []
    return []

def main():
    dlcs = recuperer_json()

    print("=== Création d'une base de données JSON de DLCs ===\n")

    while True:
        name = input("Nom du DLC : ").strip()
        if not name:
            print("Le nom ne peut pas être vide.")
            continue

        date_succes = recuperer_date(f"Date d'ajout des succès pour {name}")
        date_reveal = recuperer_date(f"Date du reveal de la date de sortie pour {name}")
        date_release = recuperer_date(f"Date de sortie de {name}")

        # Calcul des écarts
        reveal_delay = (date_reveal - date_succes).days
        release_delay = (date_release - date_succes).days

        dlcs.append({
            "name": name,
            "reveal_delay": reveal_delay,
            "release_delay": release_delay
        })

        again = input("Ajouter un autre DLC ? (o/n) : ").strip().lower()
        if again != "o":
            break

    # Sauvegarde dans un fichier JSON
    with open(f"{jeu}_maps_dlc.json", "w", encoding="utf-8") as f:
        json.dump(dlcs, f, ensure_ascii=False, indent=2)

    print(f"\n{len(dlcs)} DLC(s) enregistré(s) dans {jeu}_dlcs.json")
    print("Fichier créé avec succès !")

if __name__ == "__main__":
    main()