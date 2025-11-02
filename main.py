import matplotlib.pyplot as plt
import datetime as dt
import statistics

# Données
dlcs = [
    ["Vive la France!", 0, 11, 18],
    ["Italia", 0, 13, 19],
    ["Beyond the Baltic Sea", 0, 22, 28],
    ["Iberia", 0, 15, 21],
    ["West Balkans", 0, 10, 24],
    ["Greece", 0, 18, 33],
]
road_bs = ["Road to the Black Sea", 0, 36, 43]

# --- Calcul estimation des dates pour le prochain DLC ---

# Moyennes sans Road to the Black Sea puisque l'écart est très grand
moyenne_succes_a_reveal_sans_RBS = round(statistics.mean(d[2] for d in dlcs))
moyenne_reveal_a_release_sans_RBS = round(statistics.mean(d[3] for d in dlcs))


# Moyennes avec Road to the Black Sea
dlcs.insert(3, road_bs)
moyenne_succes_a_reveal_avec_RBS = round(statistics.mean(d[2] for d in dlcs))
moyenne_reveal_a_release_avec_RBS = round(statistics.mean(d[3] for d in dlcs))

# Ajout des estimations dans dlcs pour le graphe
dlcs.append(["Nordic Horizons (estimation avec moyennes sans RBS)", 0, moyenne_succes_a_reveal_sans_RBS, moyenne_reveal_a_release_sans_RBS])
dlcs.append(["Nordic Horizons (estimation avec moyennes)", 0, moyenne_succes_a_reveal_avec_RBS, moyenne_reveal_a_release_avec_RBS])

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

# --- Définir la date d'ajout des succès du prochain DLC ---
date_ajout_succes = dt.datetime(2025, 10, 23)

# --- Calculer les estimations à partir des moyennes sans RBS ---
estimation_date_reveal = date_ajout_succes + dt.timedelta(days=round(moyenne_succes_a_reveal_sans_RBS))
estimation_date_release = estimation_date_reveal + dt.timedelta(days=round(moyenne_reveal_a_release_sans_RBS))

# --- Afficher les résultats ---
print("\n=== Estimation pour le DLC Nordic Horizons sans RBS ===")
print(f"Ajout des succès : {date_ajout_succes.strftime('%d %B %Y')}")
print(f"Reveal de la date de sortie en moyenne : {estimation_date_reveal.strftime('%d %B %Y')}")
print(f"Sortie estimée du DLC en moyenne : {estimation_date_release.strftime('%d %B %Y')}")
print(f"Sortie estimée du DLC (jeudi le plus proche de la moyenne) : {ajuster_au_jeudi(estimation_date_release).strftime('%d %B %Y')}")

# --- Calculer les estimations à partir des moyennes avec RBS ---
estimation_date_reveal = date_ajout_succes + dt.timedelta(days=round(moyenne_succes_a_reveal_avec_RBS))
estimation_date_release = estimation_date_reveal + dt.timedelta(days=round(moyenne_reveal_a_release_avec_RBS))

# --- Afficher les résultats ---
print("\n=== Estimation pour le DLC Nordic Horizons avec RBS ===")
print(f"Ajout des succès : {date_ajout_succes.strftime('%d %B %Y')}")
print(f"Reveal de la date de sortie en moyenne : {estimation_date_reveal.strftime('%d %B %Y')}")
print(f"Sortie estimée du DLC en moyenne : {estimation_date_release.strftime('%d %B %Y')}")
print(f"Sortie estimée du DLC (jeudi le plus proche de la moyenne) : {ajuster_au_jeudi(estimation_date_release).strftime('%d %B %Y')}")

# Trouver le jour le plus tardif
max_day = max(d[3] for d in dlcs)

# Tracé
fig, ax = plt.subplots(figsize=(9, 4))
colors = ["tab:blue", "tab:orange", "tab:green"]
labels = ["Ajout succès (J0)", "Reveal date de sortie", "Sortie"]

for i, (name, j0, reveal, release) in enumerate(dlcs):
    y = len(dlcs) - i
    ax.plot([j0, reveal, release], [y]*3, marker='o', linestyle='-', color='gray', alpha=0.6)
    ax.scatter(j0, y, color=colors[0], label=labels[0] if i == 0 else "", zorder=3)
    ax.scatter(reveal, y, color=colors[1], label=labels[1] if i == 0 else "", zorder=3)
    ax.scatter(release, y, color=colors[2], label=labels[2] if i == 0 else "", zorder=3)
    ax.text(release + 1, y, name, va='center', fontsize=9)

# Mise en forme
ax.set_title("Chronologie relative des DLCs ETS2 (J0 = ajout des succès)", fontsize=11)
ax.set_xlabel("Jours après ajout des succès")
ax.set_xlim(-1, max_day + 5)
ax.set_yticks([])
ax.legend()
ax.grid(True, axis='x', linestyle='--', alpha=0.5)

plt.tight_layout()
plt.show()