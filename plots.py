import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from config import game_info

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
    plt.ylim((16, 30))
    plt.legend()
    plt.show()

def age_distribution(game, events):
    events = events[~events['age'].isnull()]
    ages = events['age']


    plt.hist(ages, bins=12, density=True)
    plt.xlabel('age')
    plt.ylabel('density')
    plt.title(f'Age distribution for {game}')
    plt.show()




def career_distribution(game, events):
    players = events.groupby('player').agg({'date' : ['min', 'max', 'count']})
    print(len(players))
    print(players.head(10))

    players = players[players[('date', 'count')] >= 20]
    players['career_length'] = players[('date', 'max')] - players[('date', 'min')]
    career_length = players['career_length'].dt.total_seconds().values / (3600 * 24 * 365.25)
    print(type(career_length))
    print(len(career_length), career_length.dtype)

    plt.hist(career_length, bins=12, density=True)
    plt.xlabel('career length')
    plt.ylabel('density')
    plt.title(f'Career length distribution for {game}')
    plt.show()


def performance_distribution(game, events):
    events = events[~events['age'].isnull()]
    events['age'] = events['age'].map(lambda age: np.clip(age, *game_info[game]['ages'])) 
    groups = events.groupby(events.age).agg({'rating' : ['mean', 'count'], 'win' : 'mean'})
    ages = groups[('rating', 'mean')].index.values
    ratings = groups[('rating', 'mean')].values
    counts = groups[('rating', 'count')].values
    win_rates = groups[('win', 'mean')].values

    print('ages', ages)
    print('ratings', ratings)
    print('win rates', win_rates)
    print('counts', counts)

    xticks = [str(int(a)) for a in ages]
    xticks[0] = '<=' + xticks[0]
    xticks[-1] += '<=' + xticks[-1] 


    plt.plot(ages, ratings, linewidth=3, label=game)
    plt.xlabel('age')
    plt.ylabel('TrueSkill rating')
    plt.title(f'TrueSkill rating by age for {game}')
    plt.xticks(ages, labels=xticks)
    plt.show()

    plt.plot(ages, win_rates, linewidth=3, label=game)
    plt.xlabel('age')
    plt.ylabel('win rate')
    plt.ylim(0.3,0.7)
    plt.title(f'win rate by age for {game}')
    plt.xticks(ages, labels=xticks)
    plt.show()


    

