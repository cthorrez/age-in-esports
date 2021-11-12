import os
import numpy as np
import pandas as pd
from ast import literal_eval
from collections import defaultdict
import trueskill
from config import games, game_info, mobas, shooters, fighters, strategy, big
from utils import PlayerInfo, win_probability
from plots import age_over_time, career_distribution, performance_distribution, age_distribution


def main():
    # games = ['counterstrike']
    group = games
    events_list = []
    for game in group:
        events = get_player_match_events(game, recompute=False)
        events_list.append(events)
        # career_distribution(game, events)
        # performance_distribution(game, events)
        age_distribution(game, events)
    age_over_time(group, events_list)

    

# a player_match_event is a tuple: (date, player, age, win)
# it tells you a player of a certain age played a match on a certain date and whether they won or not
def get_player_match_events(game, recompute=True):
    if not os.path.exists('data/processed'):
        os.makedirs('data/processed')
    file_path = f'data/processed/{game}_player_match_events.h5'
    if recompute and os.path.exists(file_path):
        os.remove(file_path)
    if not recompute and os.path.exists(file_path):
        store = pd.HDFStore(file_path)
        return store['events']
    
    info = PlayerInfo()
    matches = pd.read_csv(f'data/processed/{game}_matches.csv', converters={'team1players' : literal_eval, 'team2players' : literal_eval})
    print(f'using data on {len(matches)}, matches for {game}')
    matches['date'] = pd.to_datetime(matches['date'])
    matches['winner'] = matches['winner'].astype(int)
    matches = matches[(matches.date.dt.year >= game_info[game]['years'][0]) & \
                      (matches.date.dt.year <= game_info[game]['years'][1])]

    num_correct = 0
    num_predicted = 0
    env = trueskill.TrueSkill()
    events = []
    ratings = defaultdict(lambda : env.create_rating())
    for _, row in matches.iterrows():
        team1ratings = [ratings[p] for p in row['team1players']]
        team2ratings = [ratings[p] for p in row['team2players']]
        prediction = win_probability(team1ratings, team2ratings) > 0.5
        ranks = [int(row['winner']==1), int(row['winner']==2)]

        if len(team1ratings) == len(team2ratings):
            num_predicted += 1
            num_correct += prediction == ranks[0]
            updated_ratings = env.rate([team1ratings, team2ratings])
        else:
            # skip predicting and rating matches with uneven team sizes
            updated_ratings = [team1ratings, team2ratings]
        for team_num in [1,2]:
            for player_num, player in enumerate(row[f'team{team_num}players']):
                age = info.age(player, game, row['date'])
                rating = updated_ratings[team_num-1][player_num]
                events.append({'player': player, 'date':row['date'], 'age':age, 'rating': trueskill.expose(rating), 'win':row['winner']==team_num})
                ratings[player] = rating
                if age and age < 10:
                    print(age, player, row['date'], row['url'])
    

    print(f'trueskill accuracy for {game}: {num_correct/num_predicted}')
    print(f'top players in {game} by trueskill')
    ranking = sorted(ratings, key=lambda x: -trueskill.expose(ratings[x]))
    for i in range(20):
        print(i+1, ranking[i], trueskill.expose(ratings[ranking[i]]))
    print('')


    events = pd.DataFrame(events)
    store = pd.HDFStore(file_path)
    store['events'] = events
    return events


if __name__ == '__main__':
    main()
