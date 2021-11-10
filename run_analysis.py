import pandas as pd
from ast import literal_eval
from config import games
from utils import PlayerInfo

def main():
    # games = ['warcraft']
    for game in games:
        analyze_game(game)


def analyze_game(game):
    print(f'Analyzing data for {game}')
    info = PlayerInfo()
    matches = pd.read_csv(f'data/processed/{game}_matches.csv', converters={'team1players' : literal_eval, 'team2players' : literal_eval})
    matches['date'] = pd.to_datetime(matches['date'])
    matches['winner'] = matches['winner'].astype(int)
    events = []
    for _, row in matches.iterrows():
        for team_num in {1,2}:
            for player in row[f'team{team_num}players']:
                age = info.age(player, game, row['date'])
                if age is not None:
                    events.append({'date':row['date'], 'age':age, 'win':row['winner']==team_num})
                    if age < 10:
                        print(age, player, row['date'], row['url'])
    events = pd.DataFrame(events)

    print(game, 'num events:', len(events))
    print(game, 'average age:', events['age'].mean())
    print(game, 'winrate of known age players;', events['win'].mean())
    print('average age by year')
    print(events.groupby(events.date.dt.year).agg({'age' : ['mean', 'count'], 'win' : 'mean'}))
    print(game, 'winrate by age')
    print(events[['age', 'win']].groupby('age').agg({'win' : ['mean', 'count']}))
    print()


if __name__ == '__main__':
    main()