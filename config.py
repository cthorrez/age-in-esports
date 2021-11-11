# list of wikis to get data from
wikis = ['callofduty', 'counterstrike', 'warcraft', 'dota2', 'rocketleague', 'smash', \
         'overwatch', 'rainbowsix', 'leagueoflegends', 'valorant', 'starcraft2', 'starcraft',]

# same as above with smash split between melee and ultimate
games = ['leagueoflegends', 'dota2', 'counterstrike', 'overwatch', 'rainbowsix', 'callofduty', 'valorant', \
         'rocketleague', 'smash_melee', 'smash_ultimate', 'starcraft', 'starcraft2', 'warcraft']

mobas = ['leagueoflegends', 'dota2']
shooters = ['counterstrike', 'overwatch', 'rainbowsix', 'callofduty', 'valorant']
fighters = ['smash_melee', 'smash_ultimate']
strategy = ['starcraft', 'starcraft2', 'warcraft']
big = ['leagueoflegends', 'dota2', 'counterstrike', 'smash_melee', 'starcraft2']

game_info = {
    'starcraft': {
        'team_size' : None,
        'years' : [2000, 2021],
        'ages' : [14, 36]
    },
    'starcraft2': {
        'team_size' : None,
        'years' : [2010, 2021],
        'ages' : [14, 36]
    },
    'warcraft': {
        'team_size' : None,
        'years' : [2003, 2021],
        'ages' : [14, 36] 
    },
    'smash' : {
        'team_size': None
    },
    'smash_melee': {
        'years' : [2005, 2021],
        'ages' : [14, 36]
    },
    'smash_ultimate': {
        'years': [2019, 2021],
        'ages': [14, 32]
    },
    'rocketleague': {
        'team_size' : 3,
        'years' : [2016, 2021],
        'ages' : [13, 28]
    },
    'counterstrike': {
        'team_size': 5,
        'years': [2003, 2021],
        'ages': [14, 35]
    },
    'overwatch' : {
        'team_size' : 6,
        'years': [2016, 2021],
        'ages': [15, 29]
    },
    'valorant' : {
        'team_size': 5,
        'years': [2020, 2021],
        'ages': [16, 33]
    },
    'rainbowsix': {
        'team_size': 4,
        'years': [2016, 2021],
        'ages': [16, 32]
    },
    'callofduty': {
        'team_size': 5,
        'years': [2014, 2021],
        'ages': [16, 28]
    },
    'leagueoflegends': {
        'team_size' : 5,
        'years': [2011, 2021],
        'ages': [16, 28]
    },
    'dota2': {
        'team_size': 5,
        'years': [2011, 2021],
        'ages': [15, 31]
    }
}