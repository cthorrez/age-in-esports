import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

def age_over_time(games, events_list):
    min_year = 9999
    max_year = 0
    for game, events in zip(games, events_list):
        events = events[~events['age'].isnull()]
        groups = events.groupby(events.date.dt.year).agg({'age' : ['mean', 'count'], 'win' : 'mean'})
        years = groups[('age', 'mean')].index.values
        min_year = min(min_year, min(years))
        max_year = max(max_year, max(years))
        ages = groups[('age', 'mean')].values
        counts = groups[('age', 'count')].values
        plt.plot(years, ages, linewidth=3, label=game)
    
    plt.xlabel('year')
    plt.ylabel('average age')
    # plt.title(f'Average age in {game}')
    plt.xticks(np.arange(min_year, max_year+1))
    plt.ylim((14, 32))
    plt.legend()
    plt.show()


def career_distribution(game, events):
    players = events.groupby('player').agg({'date' : ['min', 'max', 'count']})
    print(len(players))
    print(players.head(10))

    players = players[players[('date', 'count')] >= 50]
    players['career_length'] = players[('date', 'max')] - players[('date', 'min')]
    career_length = players['career_length'].dt.total_seconds().values / (3600 * 24 * 365.25)
    print(type(career_length))
    print(len(career_length), career_length.dtype)

    plt.hist(career_length, 20)
    plt.title(game)
    plt.show()
    

