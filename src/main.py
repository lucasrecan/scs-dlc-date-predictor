from time import sleep
import matplotlib.pyplot as plt
import datetime as dt
import statistics
import json

# --- Load data ---
def load_data(game):
    """Returns the list of map DLCs released for the chosen game.
    Args:
        game (String): chosen game (ets2 or ats)
    Returns:
        List: the list of DLCs
    """
    with open(f"data/{game}_maps_dlc.json", "r", encoding="utf-8") as f:
        dlcs_data = json.load(f)
    # Convert to list 
    return [[d["name"], 0, d["reveal_delay"], d["release_delay"]] for d in dlcs_data]


# --- Estimate the dates for the next DLC ---

# Averages
def averages(dlcs):
    """Computes the average time between achievements addition and reveal/release.

    Args:
        dlcs (list): list of dlcs to compute the averages for

    Returns:
        (int, int): (average time between achievements addition and reveal,
                     average time between achievements addition and release)
    """
    avg_achievements_to_reveal = round(statistics.mean(d[2] for d in dlcs))
    avg_achievements_to_release = round(statistics.mean(d[3] for d in dlcs))
    return avg_achievements_to_reveal, avg_achievements_to_release

def adjust_to_thursday(initial_date):
    """Returns the date of the Thursday closest to the given date.
    If the date is equally distant between two Thursdays (e.g. Sunday/Monday),
    the function chooses the next Thursday.

    Args:
        initial_date (datetime): the calculated date

    Returns:
        datetime: the closest Thursday to the calculated date
    """
    diff = 3 - initial_date.weekday()
    if diff > 3:
        diff -= 7
    elif diff < -3:
        diff += 7
    return initial_date + dt.timedelta(days=diff)

def predict_next_dlc(dlcs):
    """Asks the user for the name of the next DLC (for console coherence)
    and the achievements addition date, then:
    Based on averages, prints the estimated reveal date and release date,
    and the release date adjusted to the closest Thursday.
    Using the same delays as the last DLC, it also prints the same estimates.

    Args:
        dlcs (list): list of dlcs and their delays
    """
    print("--------------------------------------------------------------------")
    next_dlc_name = input("Next DLC name: ")
    achievements_date_str = input("Date of achievements addition (format DD/MM/YYYY): ")
    achievements_date = dt.datetime.strptime(achievements_date_str, "%d/%m/%Y")

    last_dlc = dlcs[-1]
    last_reveal_delay = last_dlc[2]
    last_release_delay = last_dlc[3]

    estimated_reveal_last = achievements_date + dt.timedelta(days=last_reveal_delay)
    estimated_release_last = achievements_date + dt.timedelta(days=last_release_delay)

    print(f"\n=== Estimate for {next_dlc_name} if delays are the same as {last_dlc[0]} (last release) ===")
    print(f"achievements addition: {achievements_date.strftime('%d %B %Y')}")
    print(f"Estimated reveal date: {estimated_reveal_last.strftime('%d %B %Y')}")
    print(f"Estimated release date: {estimated_release_last.strftime('%d %B %Y')}")
    print(f"Estimated release (closest Thursday): {adjust_to_thursday(estimated_release_last).strftime('%d %B %Y')}")

    estimated_reveal_avg = achievements_date + dt.timedelta(days=round(averages(dlcs)[0]))
    estimated_release_avg = achievements_date + dt.timedelta(days=round(averages(dlcs)[1]))

    print(f"\n=== Estimate for {next_dlc_name} based on averages ===")
    print(f"achievements addition: {achievements_date.strftime('%d %B %Y')}")
    print(f"Average reveal date: {estimated_reveal_avg.strftime('%d %B %Y')}")
    print(f"Average release date: {estimated_release_avg.strftime('%d %B %Y')}")
    print(f"Average release (closest Thursday): {adjust_to_thursday(estimated_release_avg).strftime('%d %B %Y')}")

def history(dlcs, game):
    dlcs_graph = dlcs.copy()
    print("--------------------------------------------------------------------")
    print("Add an entry for averages?")
    print("1. Yes")
    print("2. No")
    print("3. Go back")
    choice = "4"
    while not(choice == "1" or choice == "2" or choice == "3"):
        choice = input("Choose a number > ")
    if choice != "3":
        if choice == "1":
            dlcs_graph.append(["Averages", 0, averages(dlcs)[0], averages(dlcs)[1]])

        max_day = max(d[3] for d in dlcs_graph)

        fig, ax = plt.subplots(figsize=(9, 4))
        colors = ["tab:blue", "tab:orange", "tab:green"]
        labels = ["achievements addition (Day 0)", "Release date reveal", "Release"]

        for i, (name, j0, reveal, release) in enumerate(dlcs_graph):
            y = len(dlcs_graph) - i
            ax.plot([j0, reveal, release], [y]*3, marker='o', linestyle='-', color='gray', alpha=0.6)
            ax.scatter(j0, y, color=colors[0], label=labels[0] if i == 0 else "", zorder=3)
            ax.scatter(reveal, y, color=colors[1], label=labels[1] if i == 0 else "", zorder=3)
            ax.scatter(release, y, color=colors[2], label=labels[2] if i == 0 else "", zorder=3)
            ax.text(release + 1, y, name, va='center', fontsize=9)

        ax.set_title(f"Relative timeline of {game.upper()} DLCs (Day 0 = achievements addition)", fontsize=11)
        ax.set_xlabel("Days after achievements addition")
        ax.set_xlim(-1, max_day + 5)
        ax.set_yticks([])
        ax.legend()
        ax.grid(True, axis='x', linestyle='--', alpha=0.5)
        plt.tight_layout()
        plt.show()

# --- Second graph: evolution of delays between achievements/reveal/release ---
def evolution(dlcs, game):
    dlcs_graph = dlcs.copy()
    print("--------------------------------------------------------------------")
    print("Add an entry for averages?")
    print("1. Yes")
    print("2. No")
    print("3. Go back")
    choice = "4"
    while not(choice == "1" or choice == "2" or choice == "3"):
        choice = input("Choose a number > ")
    if choice != "3":
        if choice == "1":
            dlcs_graph.append(["Averages", 0, averages(dlcs)[0], averages(dlcs)[1]])

        fig2, ax2 = plt.subplots(figsize=(9,4))

        names = [d[0] for d in dlcs_graph]
        reveal_values = [d[2] for d in dlcs_graph]
        release_values = [d[3] for d in dlcs_graph]

        ax2.plot(names, reveal_values, marker='o', label="Days between achievements addition and reveal", color="tab:blue")
        ax2.plot(names, release_values, marker='o', label="Days between achievements addition and release", color="tab:orange")

        ax2.set_title(f"Evolution of delays between stages for {game.upper()} DLCs", fontsize=14, pad=20)
        ax2.set_ylabel("Number of days", fontsize=12)
        ax2.set_ylim(0, max(max(reveal_values), max(release_values)) + 10)
        ax2.set_xticks(range(len(names)))
        ax2.set_xticklabels(names, rotation=45, ha='right', fontsize=10)
        ax2.legend(fontsize=12)
        ax2.grid(True, linestyle='--', alpha=0.6)
        plt.tight_layout()

    plt.show()

def show_home():
    print("--------------------------------------------------------------------")
    print("Select the game you want to analyze.")
    print("1. Euro Truck Simulator 2")
    print("2. American Truck Simulator")
    return input("Choose a number > ")

def main():
    choice = ""
    game = ""
    print("Type q to quit at any time.")
    sleep(0.25)
    while choice != "q":
        choice = show_home()
        if choice == "1":
            game = "ets2"
        elif choice == "2":
            game = "ats"
        dlcs = load_data(game)
        while choice != "q" and choice != "5":
            print("--------------------------------------------------------------------")
            print("1. Show average delays between achievements addition and reveal/release")
            print("2. Show historical delays for each released DLC in a timeline graph")
            print("3. Show evolution of delays between steps in a different graph")
            print("4. Predict dates for the next DLC (if its achievements were added)")
            print("5. Go back")
            choice = input("Choose a number > ")
            if choice == "1":
                avg_srev, avg_srel = averages(dlcs)
                print(f"Average delay achievements → reveal: {avg_srev} days")
                print(f"Average delay achievements → release: {avg_srel} days")
                input("\nPress Enter to continue...")
            elif choice == "2":
                history(dlcs, game)
            elif choice == "3":
                evolution(dlcs, game)
            elif choice == "4":
                predict_next_dlc(dlcs)
                print("--------------------------------------------------------------------")
                input("\nPress Enter to continue...")

if __name__ == "__main__":
    main()
