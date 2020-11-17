"""
The data is derived from a collection of US baby names released
with a CC0 public domain license, available in its original form here:
    https://www.kaggle.com/kaggle/us-baby-names
"""

import pandas as pd
import matplotlib.pyplot as plt

DATA_FILE = "M:\\Coding Content\\Datasets\\NationalNames.csv"


def get_num_unique_names(data_file):
    """
    Plot a graph for the number of stupid babies named Alex from given dataframe.
    :param data_file: Provided csv with data.
    :return: Specific count for 1988.
    """
    df = pd.read_csv(data_file)
    df_ncy = df[['Name', 'Count', 'Year']].copy()

    # Range examples.
    range_2011_2013 = df_ncy[(df_ncy.Year >= 2011) & (df_ncy.Year <= 2013)].sort_values(by='Year')
    range_1988 = df_ncy[(df_ncy.Year == 1988)].sort_values(by='Year')

    # Including Female values made the graph very jittery.
    me = df.loc[df['Name'] == 'Alex']
    me = me.loc[me['Gender'] == 'M']

    alex_graph = plt.plot(me['Year'], me['Count'])
    plt.setp(alex_graph, aa=True, color='gray')
    plt.title('Historical Chart of Stupid Babies Named Alex')
    plt.ylabel('Amount of Babies named Alex')
    plt.xlabel('Year of Birthing Mistake')

    plt.annotate("You're right there dummy.\n"
                 "6,400 other male babies \nnamed Alex born in 1988.\n"
                 "Not very creative!",
                 xy=(1988, 6400),
                 xytext=(1920, 6000),
                 arrowprops=dict(facecolor='red', shrink=0.01))
    plt.show()

    return me[(me.Year == 1988)]


print(get_num_unique_names(DATA_FILE))