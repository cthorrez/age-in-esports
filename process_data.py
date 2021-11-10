from copy import deepcopy
import os
import shutil
import json
import pandas as pd
from config import wikis, is_team, players_per_team
from utils import winner_from_scores

pd.set_option('display.max_colwidth', None)
pd.set_option('display.max_rows', None)
pd.set_option('display.width', 0)


def main():
    if not os.path.exists('data/processed'):
        os.makedirs('data/processed')

    shutil.rmtree('data/need_fixing', )
    os.makedirs('data/need_fixing')

    for wiki in wikis:
        players_raw = json.load(open(f'data/raw/{wiki}_players.json', 'rb'))
        player_df = pd.DataFrame(players_raw)[['pagename', 'birthdate']]
        print(len(player_df), wiki, 'players')
        if wiki != 'smash':
            player_df.to_csv(f'data/processed/{wiki}_players.csv', index=False)
        else:
            player_df.to_csv(f'data/processed/smash_melee_players.csv', index=False)
            player_df.to_csv(f'data/processed/smash_ultimate_players.csv', index=False)

        matches_raw = json.load(open(f'data/raw/{wiki}_matches.json', 'rb'))
        matches = []
        bad_cs = []
        for raw_match in matches_raw:
            team1 = raw_match['opponent1']
            team2 = raw_match['opponent2']
            if is_team[wiki]:
                if wiki == 'counterstrike' and ('p5' not in raw_match['opponent1players'] or 'p5' not in raw_match['opponent2players']):
                    bad_cs.append(raw_match)
                    continue

                if type(raw_match['opponent1players']) == list:
                    raw_match['opponent1players'] = dict(pair for d in raw_match['opponent1players'] for pair in d.items())
                    raw_match['opponent2players'] = dict(pair for d in raw_match['opponent2players'] for pair in d.items())


                if not raw_match['opponent1players'] : continue
                if not raw_match['opponent2players'] : continue
                team1players = [raw_match['opponent1players'][f'p{x+1}'] for x in range(players_per_team[wiki]) if raw_match['opponent1players'][f'p{x+1}']]
                team2players = [raw_match['opponent2players'][f'p{x+1}'] for x in range(players_per_team[wiki]) if raw_match['opponent2players'][f'p{x+1}']]
            else:
                team1players = [raw_match['opponent1']]
                team2players = [raw_match['opponent2']]

            match = {
                'date' : raw_match['date'],
                'team1' : team1,
                'team2' : team2,
                'team1players' : team1players,
                'team2players' : team2players,
                'team1score' : int(raw_match['opponent1score']),
                'team2score' : int(raw_match['opponent2score']),
                'winner' : raw_match['winner'],
                'game' : raw_match['game'],
                'matchid' : raw_match['matchid'],
                'pagename' : raw_match['pagename'],
                'mode' : raw_match['mode'],
                'objectname' : raw_match['objectname'],
                'parent' : raw_match.get('parent'),
                'comment' : raw_match.get('extradata', {}).get('comment') if raw_match.get('extradata') else None,
                'ffa' : raw_match.get('extradata', {}).get('ffa') if raw_match.get('extradata') else None,
                'url' : f'https://liquipedia.net/{wiki}/' +raw_match['pagename'].replace("'", '%27')
            }
            matches.append(match)

        match_df = pd.DataFrame(matches)
        match_df['date'] = pd.to_datetime(match_df['date'])
        
        if len(bad_cs) > 0:
            print(len(bad_cs), 'incomplete teams')
            json.dump(bad_cs, open(f'data/need_fixing/{wiki}_incomplete_team.json', 'w'), indent=2)

        # drop matches with empty teams
        match_df = match_df[match_df['team1players'].map(len) > 0]
        match_df = match_df[match_df['team2players'].map(len) > 0]

        # drop draws
        match_df = match_df[~match_df['winner'].isin({'draw', '0', 'skip', 's'})]
        match_df = match_df[~((match_df['winner']=='') & (match_df['team1score']==0) & (match_df['team2score']==0))]

        # drop byes and default wins (and pray there is no players named "bye")
        match_df = match_df[~match_df['team1'].str.match('bye', case=False)]
        match_df = match_df[~match_df['team2'].str.match('bye', case=False)]
        match_df = match_df[~match_df['comment'].astype(str).str.lower().str.contains('default win')]

        # if winner col is empty, infer it from scores
        match_df['score_winner'] = match_df.apply(lambda row: winner_from_scores(row['team1score'], row['team2score']), axis=1)
        match_df['winner'] = match_df.apply(lambda row: row['winner'] if row['winner'] else row['score_winner'], axis=1)

        # drop rows with bad date column
        match_df = match_df[~match_df['date'].astype(str).str.contains('1970-01-01')]

        # if winner col is empty and scores are equal drop the row, who the hell knows what happened there
        match_df = match_df[~match_df['winner'].isnull()]

        if wiki == 'callofduty':
            # filter out cod mobile
            match_df = match_df[match_df['game'].str.lower() != 'mobile']

        if wiki == 'warcraft':
            # filter to only 1v1
            match_df = match_df[match_df['mode'] == '1v1']
            match_df = match_df[~(match_df['pagename'].str.lower().str.contains('team') & match_df['pagename'].str.lower().str.contains('league'))]

            # handle grand finals double elim issue where loser is shown as winner if they win the first series of grands
            # disclaimer, this will not necessarily get the correct score for the added match
            fix_mask = (~match_df['winner'].isnull()) & (~match_df['score_winner'].isnull()) &\
                       (match_df['score_winner'] != match_df['winner']) & \
                       (match_df['team1score'] !=0) & (match_df['team2score'] !=0) & \
                       (match_df['objectname'].str.lower().str.contains('grand final'))

            need_fixing = deepcopy(match_df[fix_mask])
            # for original rows swap winner
            match_df.loc[fix_mask ,'winner'] = match_df[fix_mask]['score_winner']

            # make copy of original rows, swap scores and winners
            new_rows = []
            for idx, row in need_fixing.iterrows():
                if row['winner'] and row['score_winner'] and row['winner'] != row['score_winner'] and row['team1score'] !=0 and 'grand final' in row['objectname'].lower():
                    new_row = deepcopy(row)
                    new_row['score_winner'], new_row['team1score'], new_row['team2score'] = new_row['winner'], new_row['team2score'], new_row['team1score']
                    new_rows.append(new_row)
            new_df = pd.DataFrame(new_rows)
            match_df = pd.concat([match_df, new_df])

        if wiki == 'counterstrike':
            # get rid of a couple showmatches with weird rules
            match_df = match_df[~match_df['parent'].str.lower().str.contains('showmatch')]

        if wiki == 'smash':
            # smash writes player names in the win field rather than '1' or '2' so we map them to be consistent
            # the order of these two lines is important. If you can tell me why I'll give you 5 dollars. (first person) email claytonthorrez@gmail.com
            match_df.loc[match_df['winner'] == match_df['team2'], 'winner'] = '2'
            match_df.loc[match_df['winner'] == match_df['team1'], 'winner'] = '1'
            # smash sometimes puts -99 for unknown scores
            match_df.loc[match_df['team1score'] == -99, 'team1score'] = 0
            match_df.loc[match_df['team2score'] == -99, 'team1score'] = 0
            # drop games where scores are nonzero, and tied. These are extended series wins
            match_df = match_df[~((match_df['team1score'] != 0) & (match_df['team2score'] != 0) & (match_df['team1score'] == match_df['team2score']))]

        if wiki == 'rainbowsix':
            match_df = match_df[match_df['game'] != 'vegas2']
            match_df = match_df[match_df['date'].dt.year > 2008]
            # in rainbox six they mark draws and forfeiths with winner = -1 I think
            match_df = match_df[match_df['winner'] != '-1']
            # they mark unknown scores as -1
            match_df.loc[match_df['team1score'] == -1, 'team1score'] = 0
            match_df.loc[match_df['team2score'] == -1, 'team2score'] = 0

        if wiki in {'starcraft', 'starcraft2'}:
            # filter out team matches
            match_df = match_df[match_df['mode'] != 'team']
            match_df = match_df[~(match_df['pagename'].str.lower().str.contains('team') & match_df['pagename'].str.lower().str.contains('league'))]
            if wiki == 'starcraft2':
                # drop games where scores are nonzero, and tied. These are extended series wins
                match_df = match_df[~((match_df['team1score'] != 0) & (match_df['team2score'] != 0) & (match_df['team1score'] == match_df['team2score']))]
                # drop ffa
                match_df = match_df[match_df['ffa'] != 'true']
            
        if wiki == 'rocketleague':
            # in rocket league ties are automatically given to team 1 so we drop them
            match_df = match_df[~(match_df['team1score'] == match_df['team2score'])]
            match_df = match_df[~match_df['winner'].str.contains('Expression error')]

        if wiki == 'valorant':
            # lol...
            match_df = match_df[match_df['winner'] != 'Expression error: Unrecognized word "ff"']

        if wiki == 'dota2':
            match_df = match_df[match_df['date'].dt.year > 2008]

               
        bad_winner_mask = ((~match_df.winner.isnull()) & \
                          (match_df['score_winner'] != match_df['winner']) & \
                          (match_df['team1score'] !=0) & (match_df['team2score'] !=0)) | \
                          ~(match_df['winner'].isin({'1', '2'}))
        bad_winner_df = deepcopy(match_df[bad_winner_mask])
        print(len(bad_winner_df), 'matches with bad winner data')
        if len(bad_winner_df) > 0:
            bad_winner_df['date'] = bad_winner_df['date'].astype(str).str.slice(0,10)
            bad_winner_df = bad_winner_df[['date', 'team1', 'team2', 'team1score', 'team2score', 'winner', 'url']]
            bad_winner_df.to_csv(f'data/need_fixing/{wiki}_bad_winner.csv', index=False)

        
        bad_date_df = match_df[match_df['date'].astype(str).str.contains('1970')][['date', 'team1', 'team2', 'pagename']]
        print(len(bad_date_df), 'matches with bad dates')
        if len(bad_date_df) > 0:
            bad_date_df.to_csv(f'data/need_fixing/{wiki}_bad_dates.csv', index=False)
        
        match_df = match_df[~bad_winner_mask]
        match_df = match_df[~match_df['winner'].isnull()]
        match_df['winner'] = match_df['winner'].astype(int)
        match_df = match_df.sort_values('date')
        if wiki != 'smash':
            out_match_df = match_df[['date', 'team1', 'team2', 'team1players', 'team2players', 'team1score', 'team2score', 'winner', 'url']]
            out_match_df.to_csv(f'data/processed/{wiki}_matches.csv', index=False)
        else:
            melee_match_df = match_df[match_df['game'] == 'melee']
            ultimate_match_df = match_df[match_df['game'] == 'ultimate']
            melee_match_df = melee_match_df[['date', 'team1', 'team2', 'team1players', 'team2players', 'team1score', 'team2score', 'winner', 'url']]
            ultimate_match_df = ultimate_match_df[['date', 'team1', 'team2', 'team1players', 'team2players', 'team1score', 'team2score', 'winner', 'url']]
            melee_match_df.to_csv(f'data/processed/{wiki}_melee_matches.csv', index=False)
            ultimate_match_df.to_csv(f'data/processed/{wiki}_ultimate_matches.csv', index=False)
            print(len(melee_match_df), wiki, 'melee matches')
            print(len(ultimate_match_df), wiki, 'ultimate matches')


        games = json.load(open(f'data/raw/{wiki}_games.json'))
        game_df = pd.DataFrame(games)
        game_df = pd.merge(match_df, game_df, on='matchid', how='inner', suffixes=['_match', '_game'])
        game_df = game_df.rename(columns={'winner_game' : 'winner', 'game_match' : 'game'})

        game_df = game_df.sort_values('date')
        if wiki != 'smash':
            print(game_df['winner'].unique().tolist())
            game_df = game_df[['date', 'team1', 'team2', 'team1players', 'team2players', 'winner', 'url']]
            game_df.to_csv(f'data/processed/{wiki}_games.csv', index=False)
        else:
            melee_game_df = game_df[game_df['game'] == 'melee']
            ultimate_game_df = game_df[game_df['game'] == 'ultimate']
            melee_game_df = melee_game_df[['date', 'team1', 'team2', 'team1players', 'team2players', 'team1score', 'team2score', 'winner', 'url']]
            ultimate_game_df = ultimate_game_df[['date', 'team1', 'team2', 'team1players', 'team2players', 'team1score', 'team2score', 'winner', 'url']]
            melee_game_df.to_csv(f'data/processed/{wiki}_melee_games.csv', index=False)
            ultimate_game_df.to_csv(f'data/processed/{wiki}_ultimate_games.csv', index=False)
            print(len(melee_game_df), wiki, 'melee games')
            print(len(ultimate_game_df), wiki, 'ultimate games')
        
        print(len(match_df), wiki, 'matches')
        print(len(game_df), wiki, 'games')
        print('')


    

if __name__ == '__main__':
    main()