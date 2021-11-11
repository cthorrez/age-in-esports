import numpy as np
import pandas as pd
from ast import literal_eval
from config import games, game_info, mobas, shooters, fighters, strategy, big
from utils import PlayerInfo
from plots import age_over_time, career_distribution
import os


def main():
    # games = ['starcraft']
    group = games
    events_list = []
    for game in group:
        events = get_player_match_events(game)
        events_list.append(events)
        # career_distribution(game, events)
    age_over_time(group, events_list)

    

# a player_match_event is a tuple: (date, player, age, win)
# it tells you a player of a certain age played a match on a certain date and whether they won or not
def get_player_match_events(game, recompute=False):
    if not os.path.exists('data/processed'):
        os.makedirs('data/processed')
    file_path = f'data/processed/{game}_player_match_events.h5'
    if not recompute and os.path.exists(file_path):
        store = pd.HDFStore(file_path)
        return store['events']
    

    info = PlayerInfo()
    matches = pd.read_csv(f'data/processed/{game}_matches.csv', converters={'team1players' : literal_eval, 'team2players' : literal_eval})
    matches['date'] = pd.to_datetime(matches['date'])
    matches['winner'] = matches['winner'].astype(int)
    matches = matches[(matches.date.dt.year >= game_info[game]['years'][0]) & \
                      (matches.date.dt.year <= game_info[game]['years'][1])]

    # team1events = matches.explode('team1players').rename({'team1players' : 'player'})
    # team1events['win'] = team1events['winner'] == '1'
    # team2events = matches.explode('team2players').rename({'team2players' : 'player'})
    # team2events['win'] = team2events['winner'] == '2'
    # events = pd.concat([team1events, team2events], axis=1)[['player', 'date', 'win']]
    # events['age'] = events['player'].map(lambda p : info.age(p, ))


    events = []
    for _, row in matches.iterrows():
        for team_num in {1,2}:
            for player in row[f'team{team_num}players']:
                age = info.age(player, game, row['date'])
                age = np.clip(age, *game_info[game]['ages']) if age else None
                events.append({'player': player, 'date':row['date'], 'age':age, 'win':row['winner']==team_num})
                if age and age < 10:
                    print(age, player, row['date'], row['url'])
    events = pd.DataFrame(events)
    store = pd.HDFStore(file_path)
    store['events'] = events
    return events


if __name__ == '__main__':
    main()
