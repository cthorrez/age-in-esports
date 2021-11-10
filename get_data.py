import os
import pandas as pd
import json
from copy import deepcopy
from lpdb_cache import LPDBCache
from queries import player_query, match_query, game_query
from config import wikis



def main():
    # wikis = ['valorant', 'leagueoflegends', 'counterstrike'] + wikis

    # wikis = ['leagueoflegends']

    if not os.path.exists('data/raw'):
        os.makedirs('data/raw/')

    limit = 5000
    force_refresh = False
    cache = LPDBCache(timeout=10, limit=limit)

    for wiki in wikis:
        wiki_player_query = deepcopy(player_query)
        wiki_player_query['wiki'] = wiki

        players = cache.get(wiki_player_query, offset=0)
        print(wiki, len(players), 'players')
        json.dump(players, open(f'data/raw/{wiki}_players.json', 'w'), indent=2, sort_keys=True, ensure_ascii=True)

        wiki_match_query = deepcopy(match_query)
        wiki_match_query['wiki'] = wiki
        if wiki == 'smash':
            wiki_match_query['conditions'] += ' AND [[mode::singles]]'
        if wiki == 'counterstrike':
            wiki_match_query['query'] += ', parent'

        if wiki == 'leagueoflegends':
            cache.limit = 1000
        elif wiki == 'dota2':
            cache.limit = 600
        else:
            cache.limit = limit

        

        matches = cache.get(wiki_match_query, offset=0, force_refresh=force_refresh)
        print(wiki, len(matches), 'matches')
        json.dump(matches, open(f'data/raw/{wiki}_matches.json', 'w'), indent=2, sort_keys=True, ensure_ascii=True)

        wiki_game_query = deepcopy(game_query)
        if wiki == 'smash':
            wiki_game_query['conditions'] ='[[mode::singles]] AND ([[game::melee]] OR [[game::ultimate]])'
        wiki_game_query['wiki'] = wiki
        games = cache.get(wiki_game_query, force_refresh=force_refresh)
        print(len(games), 'games')
        json.dump(games, open(f'data/raw/{wiki}_games.json', 'w'), indent=2, sort_keys=True, ensure_ascii=True)


if __name__ == '__main__':
    main()