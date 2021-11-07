import os
import pandas as pd
import json
from copy import deepcopy
from lpdb_cache import LPDBCache
from queries import player_query, match_query, game_query

def main():
    wikis = ['starcraft', 'starcraft2', 'counterstrike', 'rocketleague', 'overwatch',
             'valorant', 'rainbowsix', 'leagueoflegends', 'ageofempires', 'smash',
             'warcraft']
    wikis = ['warcraft', 'overwatch', 'ageofempires', 'starcraft2', 'rocketleague', 'smash']

    wikis = ['starcraft2', 'heroes']

    if not os.path.exists('data/raw'):
        os.makedirs('data/raw/')

    cache = LPDBCache(timeout=8, limit=5000)

    for wiki in wikis:
        wiki_player_query = deepcopy(player_query)
        wiki_player_query['wiki'] = wiki

        cache.limit = 1000
        cache.timeout = 1
        players = cache.get(wiki_player_query, offset=0)
        print(wiki, len(players), 'players')
        json.dump(players, open(f'data/raw/{wiki}_players.json', 'w'), indent=2, sort_keys=True, ensure_ascii=True)

        wiki_match_query = deepcopy(match_query)
        wiki_match_query['wiki'] = wiki
        cache.limit = 5000
        cache.timeout = 5
        matches = cache.get(wiki_match_query)
        print(wiki, len(matches), 'matches')
        json.dump(matches, open(f'data/raw/{wiki}_matches.json', 'w'), indent=2, sort_keys=True, ensure_ascii=True)

        wiki_game_query = deepcopy(game_query)
        wiki_game_query['wiki'] = wiki
        games = cache.get(wiki_game_query)
        print(len(games), 'games')
        json.dump(games, open(f'data/raw/{wiki}_games.json', 'w'), indent=2, sort_keys=True, ensure_ascii=True)


if __name__ == '__main__':
    main()