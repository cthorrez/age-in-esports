"""config files for LPDB queries"""

### Player Query ###
player_query = {
    'version' : 'v2',
    'endpoint' : 'player',
    'query' : 'id, alternateid, birthdate, nationality, status, earnings',
    'conditions' : '[[birthdate::!1970-01-01]] AND [[status::!not player]] AND [[id::!Lin Guagua]]',
    'order' : 'id ASC'
}
####################

### Match Query ###
match_query = {
    'version' : 'v1',
    'endpoint' : 'match',
    'query' : 'date, opponent1, opponent2, opponent1score, opponent2score, opponent1players, opponent2players, ' + \
              'winner, mode, type, game, matchid, pageid',
    'conditions' : '[[date::!1970-01-01]] AND [[finished::1]]',
    'order' : 'date ASC'
}
####################

### Game Query ###
game_query = {
    'version' : 'v1',
    'endpoint' : 'game',
    'query' : 'date, opponent1, opponent2, opponent1score, opponent2score, ' + \
              'winner, mode, type, game, matchid, pageid',
}
####################

