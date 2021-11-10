# list of wikis to get data from
wikis = ['callofduty', 'counterstrike', 'starcraft', 'starcraft2', 'rocketleague', 'smash', \
         'overwatch', 'rainbowsix', 'leagueoflegends', 'valorant', 'warcraft', 'dota2', ]

# same as above with smash split between melee and ultimate
games = ['callofduty', 'counterstrike', 'starcraft', 'starcraft2', 'rocketleague', 'overwatch', \
         'smash_melee', 'smash_ultimate', 'rainbowsix', 'leagueoflegends', 'valorant', 'warcraft', 'dota2', ]

# maps game title to a boolean representing whether it is a team game or not
is_team = {
    'starcraft' : False,
    'starcraft2' : False,
    'warcraft' : False,
    'smash' : False,
    'rocketleague' : True,
    'counterstrike' : True,
    'valorant' : True,
    'rainbowsix' : True,
    'overwatch' : True,
    'callofduty' : True,
    'leagueoflegends' : True,
    'dota2' : True
}

# number of players per team in a game
players_per_team = {
    'callofduty' : 5,
    'counterstrike' : 5,
    'overwatch' : 6,
    'leagueoflegends' : 5,
    'rocketleague' : 3,
    'valorant' : 5,
    'rainbowsix' : 4,
    'dota2' : 5
}