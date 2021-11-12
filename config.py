# list of wikis to get data from
wikis = ['callofduty', 'counterstrike', 'warcraft', 'dota2', 'rocketleague', 'smash', \
         'overwatch', 'rainbowsix', 'leagueoflegends', 'valorant', 'starcraft2', 'starcraft',]

# same as above with smash split between melee and ultimate
games = ['leagueoflegends', 'dota2', 'counterstrike', 'overwatch', 'rainbowsix', 'callofduty', 'valorant', \
         'rocketleague', 'smash_melee', 'smash_ultimate', 'starcraft', 'starcraft2', 'warcraft']


game_categories = {
    'all' : games, 
    'moba' : ['leagueoflegends', 'dota2'],
    'shooting' : ['counterstrike', 'overwatch', 'rainbowsix', 'callofduty', 'valorant'],
    'fighting' : ['smash_melee', 'smash_ultimate'],
    'strategy' : ['starcraft', 'starcraft2', 'warcraft'],
    'big' : ['leagueoflegends', 'dota2', 'counterstrike', 'smash_melee', 'starcraft2']
}

game_info = {
    'starcraft': {
        'team_size' : None,
        'years' : [2000, 2021],
        'ages' : [15, 35]
    },
    'starcraft2': {
        'team_size' : None,
        'years' : [2010, 2021],
        'ages' : [14, 33]
    },
    'warcraft': {
        'team_size' : None,
        'years' : [2003, 2021],
        'ages' : [15, 33] 
    },
    'smash' : {
        'team_size': None
    },
    'smash_melee': {
        'years' : [2005, 2021],
        'ages' : [16, 33]
    },
    'smash_ultimate': {
        'years': [2019, 2021],
        'ages': [16, 31]
    },
    'rocketleague': {
        'team_size' : 3,
        'years' : [2016, 2021],
        'ages' : [14, 25]
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
        'ages': [17, 30]
    },
    'rainbowsix': {
        'team_size': 4,
        'years': [2016, 2021],
        'ages': [18, 28]
    },
    'callofduty': {
        'team_size': 5,
        'years': [2014, 2021],
        'ages': [17, 26]
    },
    'leagueoflegends': {
        'team_size' : 5,
        'years': [2011, 2021],
        'ages': [16, 27]
    },
    'dota2': {
        'team_size': 5,
        'years': [2011, 2021],
        'ages': [15, 31]
    }
}