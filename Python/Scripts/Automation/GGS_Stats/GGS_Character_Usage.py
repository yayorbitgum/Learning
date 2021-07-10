# ---------------------------------------------------
import matplotlib.pyplot
import seaborn as sns
import pandas as pd
from matplotlib import patches, pyplot as plt


# ---------------------------------------------------
def ggs_barplot(csv_file, title):
    ungas = pd.read_csv(csv_file)
    print(ungas.head())

    sns.set_style("darkgrid")

    totals = ungas.copy()
    celestials = ungas.copy()

    del totals['Celestial']
    del celestials['TotalPlayers']

    # ----------------------------------------------
    bar_totals: matplotlib.pyplot.Axes = sns.barplot(
        x="Character",
        y="TotalPlayers",
        data=totals,
        color='orange').set_title(title)

    # ----------------------------------------------
    bar_celestials: matplotlib.pyplot.Axes = sns.barplot(
        x="Character",
        y="Celestial",
        data=celestials,
        color='pink').set_title(title)

    celestial_percentages = []
    for total, celest in zip(totals['TotalPlayers'], celestials['Celestial']):
        celestial_percentages.append(celest / total)

    celestial_formatted = []
    for percent in celestial_percentages:
        celestial_formatted.append(f"{round(percent * 100, 2)}%")

    print(celestial_formatted)

    # ----------------------------------------------
    top_bar = patches.Patch(color='orange', label='Total Players')
    bottom_bar = patches.Patch(color='pink', label='Celestial Players')
    plt.legend(handles=[top_bar, bottom_bar])
    plt.xlabel("Character", size=14)
    plt.ylabel("Players", size=14)
    plt.show()


# ---------------------------------------------------
ggs_barplot("PlaystationPlayers.csv", "Playstation")
ggs_barplot("PCPlayers.csv", "Steam")
