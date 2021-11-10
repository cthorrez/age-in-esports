"""config files for LPDB queries"""

### Player Query ###
player_query = {
    'version' : 'v2',
    'endpoint' : 'player',
    'query' : 'id, alternateid, birthdate, nationality, status, earnings',
    'conditions' : '[[status::!not player]] AND [[id::!Lin Guagua]]',
    'order' : 'id ASC'
}
####################

### Match Query ###
match_query = {
    'version' : 'v1',
    'endpoint' : 'match',
    'query' : 'date, opponent1, opponent2, opponent1score, opponent2score, opponent1players, opponent2players, ' + \
              'winner, mode, type, game, matchid, pageid, pagename, objectname, extradata',
    'conditions' : '[[date::!1970-01-01]] AND [[date::!1000-01-01]] AND [[walkover::!1]] AND [[walkover::!2]]', 
    'order' : 'date ASC'
}
####################

### Game Query ###
game_query = {
    'version' : 'v1',
    'endpoint' : 'game',
    'query' : 'opponent1, opponent2, opponent1score, opponent2score, ' + \
              'winner, mode, type, game, matchid, pageid, extradata',
}
####################

