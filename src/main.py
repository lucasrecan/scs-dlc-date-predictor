import matplotlib.pyplot as plt
import datetime as dt
import statistics
import json
nom_prochain_dlc = "Prochain DLC"
# --- Charger les données ---
def load_data(jeu):
    """Renvoie la liste des dlcs de maps sortis en fonction du jeu voulu.
    Args:
        jeu (String): le jeu choisi (ets2 ou ats)
    Returns:
        List: la liste des dlcs
    """
    with open(f"data/{jeu}_maps_dlc.json", "r", encoding="utf-8") as f:
        dlcs_data = json.load(f)
    # Convertir en liste 
    return [[d["name"], 0, d["reveal_delay"], d["release_delay"]] for d in dlcs_data]


# --- Calcul estimation des dates pour le prochain DLC ---

# Moyennes
def moyennes(dlcs):
    moyenne_succes_a_reveal = round(statistics.mean(d[2] for d in dlcs))
    moyenne_succes_a_release = round(statistics.mean(d[3] for d in dlcs))
    return moyenne_succes_a_reveal, moyenne_succes_a_release

def ajuster_au_jeudi(date_initiale):
    """
    Retourne la date du jeudi le plus proche de la date donnée.
    Si la date est à égale distance entre deux jeudis (ex : dimanche/lundi),
    la fonction choisit le jeudi suivant.
    """
    # Différence en jours entre le jeudi (3) et le jour actuel
    diff = 3 - date_initiale.weekday()
    # On ramène la différence dans l’intervalle [-3, +3] pour obtenir le plus proche jeudi
    if diff > 3:
        diff -= 7
    elif diff < -3:
        diff += 7
    # On renvoie la date ajustée
    return date_initiale + dt.timedelta(days=diff)

def predire_prochain_dlc(dlcs):
    # --- Demander à l'utilisateur le nom du DLC et la date d'ajout des succès ---
    nom_prochain_dlc = input("Nom du prochain DLC : ")
    date_ajout_succes_str = input("Date d'ajout des succès (format JJ/MM/AAAA) : ")
    date_ajout_succes = dt.datetime.strptime(date_ajout_succes_str, "%d/%m/%Y")
    # --- Trouver le dernier DLC sorti (dernière ligne de dlcs) ---
    dernier_dlc = dlcs[-1]
    delai_dernier_reveal = dernier_dlc[2]  # Délai entre succès et reveal
    delai_dernier_release = dernier_dlc[3]  # Délai entre succès et sortie
    # 1. Si les délais sont identiques au dernier DLC sorti
    estimation_date_reveal_dernier = date_ajout_succes + dt.timedelta(days=delai_dernier_reveal)
    estimation_date_release_dernier = date_ajout_succes + dt.timedelta(days=delai_dernier_release)

    # --- Afficher les résultats ---
    print(f"\n=== Estimation pour {nom_prochain_dlc} si les délais sont identiques à {dernier_dlc[0]} (dernière sortie) ===")
    print(f"Ajout des succès : {date_ajout_succes.strftime('%d %B %Y')}")
    print(f"Reveal de la date de sortie estimée : {estimation_date_reveal_dernier.strftime('%d %B %Y')}")
    print(f"Sortie estimée du DLC estimée : {estimation_date_release_dernier.strftime('%d %B %Y')}")
    print(f"Sortie estimée du DLC (jeudi le plus proche) : {ajuster_au_jeudi(estimation_date_release_dernier).strftime('%d %B %Y')}")

    # --- Calculer les estimations à partir des moyennes ---
    estimation_date_reveal = date_ajout_succes + dt.timedelta(days=round(moyennes(dlcs)[0]))
    estimation_date_release = date_ajout_succes + dt.timedelta(days=round(moyennes(dlcs)[1]))

    # --- Afficher les résultats ---
    print(f"\n=== Estimation pour {nom_prochain_dlc} avec les moyennes ===")
    print(f"Ajout des succès : {date_ajout_succes.strftime('%d %B %Y')}")
    print(f"Reveal de la date de sortie en moyenne : {estimation_date_reveal.strftime('%d %B %Y')}")
    print(f"Sortie estimée du DLC en moyenne : {estimation_date_release.strftime('%d %B %Y')}")
    print(f"Sortie estimée du DLC (jeudi le plus proche de la moyenne) : {ajuster_au_jeudi(estimation_date_release).strftime('%d %B %Y')}")

def historique(dlcs, jeu, prochain_dlc=True):
    dlcs_graphe = dlcs.copy()
    if prochain_dlc:
        # Ajout de l'estimation dans dlcs pour le graphe
        dlcs_graphe.append([f"{nom_prochain_dlc} (estimation)", 0, moyennes(dlcs)[0], moyennes(dlcs)[1]])

    # Trouver le jour le plus tardif
    jour_max = max(d[3] for d in dlcs_graphe)

    # Tracé
    fig, ax = plt.subplots(figsize=(9, 4))
    colors = ["tab:blue", "tab:orange", "tab:green"]
    labels = ["Ajout succès (J0)", "Reveal date de sortie", "Sortie"]

    for i, (name, j0, reveal, release) in enumerate(dlcs_graphe):
        y = len(dlcs_graphe) - i
        ax.plot([j0, reveal, release], [y]*3, marker='o', linestyle='-', color='gray', alpha=0.6)
        ax.scatter(j0, y, color=colors[0], label=labels[0] if i == 0 else "", zorder=3)
        ax.scatter(reveal, y, color=colors[1], label=labels[1] if i == 0 else "", zorder=3)
        ax.scatter(release, y, color=colors[2], label=labels[2] if i == 0 else "", zorder=3)
        ax.text(release + 1, y, name, va='center', fontsize=9)

    # Mise en forme
    ax.set_title(f"Chronologie relative des DLCs {jeu.upper()} (J0 = ajout des succès)", fontsize=11)
    ax.set_xlabel("Jours après ajout des succès")
    ax.set_xlim(-1, jour_max + 5)
    ax.set_yticks([])
    ax.legend()
    ax.grid(True, axis='x', linestyle='--', alpha=0.5)
    plt.tight_layout()
    plt.show()

# --- Deuxième graphe : Évolution des temps entre ajout des succès/reveal et reveal/sortie ---
def evolution(dlcs, jeu, prochain_dlc=True):
    dlcs_graphe = dlcs.copy()
    if prochain_dlc:
        # Ajout de l'estimation dans dlcs pour le graphe
        dlcs_graphe.append([f"{nom_prochain_dlc} (estimation)", 0, moyennes(dlcs)[0], moyennes(dlcs)[1]])

    fig2, ax2 = plt.subplots(figsize=(9,4))

    # Extraire les noms et les valeurs
    noms = [d[0] for d in dlcs_graphe]
    valeurs_reveal = [d[2] for d in dlcs_graphe]
    valeurs_release = [d[3] for d in dlcs_graphe]

    # Tracer les courbes
    ax2.plot(noms, valeurs_reveal, marker='o', label="Jours entre ajout succès et reveal", color="tab:blue")
    ax2.plot(noms, valeurs_release, marker='o', label="Jours entre ajout succès et sortie", color="tab:orange")

    # Mise en forme
    ax2.set_title(f"Évolution des délais entre étapes pour les DLCs {jeu.upper()}", fontsize=14, pad=20)
    ax2.set_ylabel("Nombre de jours", fontsize=12)
    ax2.set_ylim(0, max(max(valeurs_reveal), max(valeurs_release)) + 10)  # Marge en haut
    ax2.set_xticks(range(len(noms)))
    ax2.set_xticklabels(noms, rotation=45, ha='right', fontsize=10)  # Rotation et alignement
    ax2.legend(fontsize=12)
    ax2.grid(True, linestyle='--', alpha=0.6)
    plt.tight_layout()


    plt.show()

def afficher_accueil():
        print("Sélectionnez le jeu sur lequel vous voulez faire vos analyses.")
        print("1. Euro Truck Simulator 2")
        print("2. American Truck Simulator")
        print("Choisissez un numéro > ")
        return input()

def main():
    choix = ""
    jeu = ""
    print("écrire q pour quitter à tout moment")
    while choix != "q":
        choix = afficher_accueil()
        if choix == "1":
            jeu = "ets2"
        elif choix == "2":
            jeu = "ats"
        dlcs = load_data(jeu)
        while choix != "q" and choix != "5":
            print("1. Afficher les moyennes des délais entre l'ajout des succès du DLC et la date d'annonce/de sortie")
            print("2. Afficher l'historique des délais pour chaque DLC sorti dans un graphe")
            print("3. Afficher l'évolution des délais pour chaque DLC sorti dans un graphe différent")
            print("4. Prédire les dates du prochain dlc (si ses succès ont été ajoutés)")
            print("5. Revenir en arrière")
            choix = input()
            if choix == "1":
                moyenne_srev, moyenne_srel = moyennes(dlcs)
                print(f"Moyenne délai succès - reveal : {moyenne_srev}")
                print(f"Moyenne délai succès - sortie : {moyenne_srel}")
            elif choix == "2":
                historique(dlcs, jeu, prochain_dlc=False)
            elif choix == "3":
                evolution(dlcs, jeu, prochain_dlc=False)
            elif choix == "4":
                predire_prochain_dlc(dlcs)

if __name__ == "__main__":
    main()