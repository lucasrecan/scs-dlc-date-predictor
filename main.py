import matplotlib.pyplot as plt
import datetime as dt
import statistics

# Données
dlcs = [
    ["Scandinavia", 0, 9, 42],
    ["Vive la France!", 0, 11, 18],
    ["Italia", 0, 44, 50],
    ["Beyond the Baltic Sea", 0, 22, 28],
    ["Road to the Black Sea", 0, 36, 43],
    ["Iberia", 0, 15, 21],
    ["West Balkans", 0, 10, 34],
    ["Greece", 0, 18, 33],
]



# # --- Charger les données ---
# with open("ets2_maps_dlc.json", "r", encoding="utf-8") as f:
#     dlcs_data = json.load(f)
# # Convertir en liste 
# dlcs = [[d["name"], 0, d["reveal_delay"], d["release_delay"]] for d in dlcs_data]

# road_bs = next(d for d in dlcs if "Black Sea" in d[0])
# dlcs = [d for d in dlcs if d != road_bs]

# --- Demander à l'utilisateur le nom du DLC et la date d'ajout des succès ---
nom_prochain_dlc = input("Nom du prochain DLC : ")
date_ajout_succes_str = input("Date d'ajout des succès (format JJ/MM/AAAA) : ")
date_ajout_succes = dt.datetime.strptime(date_ajout_succes_str, "%d/%m/%Y")

# --- Trouver le dernier DLC sorti (dernière ligne de dlcs) ---
dernier_dlc = dlcs[-1]
delai_dernier_reveal = dernier_dlc[2]  # Délai entre succès et reveal
delai_dernier_release = dernier_dlc[3]  # Délai entre succès et sortie


# --- Calcul estimation des dates pour le prochain DLC ---

# Moyennes
moyenne_succes_a_reveal = round(statistics.mean(d[2] for d in dlcs))
moyenne_succes_a_release = round(statistics.mean(d[3] for d in dlcs))
print(f"Moyenne délai succès - reveal : {moyenne_succes_a_reveal}")
print(f"Moyenne délai succès - sortie : {moyenne_succes_a_release}")


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

# 1. Si les délais sont identiques au dernier DLC sorti
estimation_date_reveal_dernier = date_ajout_succes + dt.timedelta(days=delai_dernier_reveal)
estimation_date_release_dernier = date_ajout_succes + dt.timedelta(days=delai_dernier_release)

# --- Afficher les résultats ---
print(f"\n=== Estimation pour {nom_prochain_dlc} si les délais sont identiques à {dernier_dlc[0]} ===")
print(f"Ajout des succès : {date_ajout_succes.strftime('%d %B %Y')}")
print(f"Reveal de la date de sortie estimée : {estimation_date_reveal_dernier.strftime('%d %B %Y')}")
print(f"Sortie estimée du DLC estimée : {estimation_date_release_dernier.strftime('%d %B %Y')}")
print(f"Sortie estimée du DLC (jeudi le plus proche) : {ajuster_au_jeudi(estimation_date_release_dernier).strftime('%d %B %Y')}")

# --- Calculer les estimations à partir des moyennes ---
estimation_date_reveal = date_ajout_succes + dt.timedelta(days=round(moyenne_succes_a_reveal))
estimation_date_release = date_ajout_succes + dt.timedelta(days=round(moyenne_succes_a_release))

# --- Afficher les résultats ---
print(f"\n=== Estimation pour {nom_prochain_dlc} ===")
print(f"Ajout des succès : {date_ajout_succes.strftime('%d %B %Y')}")
print(f"Reveal de la date de sortie en moyenne : {estimation_date_reveal.strftime('%d %B %Y')}")
print(f"Sortie estimée du DLC en moyenne : {estimation_date_release.strftime('%d %B %Y')}")
print(f"Sortie estimée du DLC (jeudi le plus proche de la moyenne) : {ajuster_au_jeudi(estimation_date_release).strftime('%d %B %Y')}")

# Ajout de l'estimation dans dlcs pour le graphe
dlcs_graphe = dlcs.copy()
dlcs_graphe.append([f"{nom_prochain_dlc} (estimation)", 0, moyenne_succes_a_reveal, moyenne_succes_a_release])

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
ax.set_title("Chronologie relative des DLCs ETS2 (J0 = ajout des succès)", fontsize=11)
ax.set_xlabel("Jours après ajout des succès")
ax.set_xlim(-1, jour_max + 5)
ax.set_yticks([])
ax.legend()
ax.grid(True, axis='x', linestyle='--', alpha=0.5)
plt.tight_layout()



# --- Deuxième graphe : Évolution des temps entre ajout des succès/reveal et reveal/sortie ---
fig2, ax2 = plt.subplots(figsize=(9,4))

# Extraire les noms et les valeurs
noms = [d[0] for d in dlcs]
valeurs_reveal = [d[2] for d in dlcs]
valeurs_release = [d[3] for d in dlcs]

# Tracer les courbes
ax2.plot(noms, valeurs_reveal, marker='o', label="Jours entre ajout succès et reveal", color="tab:blue")
ax2.plot(noms, valeurs_release, marker='o', label="Jours entre ajout succès et sortie", color="tab:orange")

# Mise en forme
ax2.set_title("Évolution des délais entre étapes pour les DLCs ETS2", fontsize=14, pad=20)
ax2.set_ylabel("Nombre de jours", fontsize=12)
ax2.set_ylim(0, max(max(valeurs_reveal), max(valeurs_release)) + 10)  # Marge en haut
ax2.set_xticks(range(len(noms)))
ax2.set_xticklabels(noms, rotation=45, ha='right', fontsize=10)  # Rotation et alignement
ax2.legend(fontsize=12)
ax2.grid(True, linestyle='--', alpha=0.6)
plt.tight_layout()


plt.show()
