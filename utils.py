import json
import pandas as pd
from copy import deepcopy
from datetime import date
from config import games
import itertools
import math
import inspect
import trueskill

def process_username(player):
    if not player : return player
    return lower_first(strip_quote(player))

def lower_first(player):
    return player[0].lower() + player[1:]

def strip_quote(player):
    if player[0] == "'" and player[-1] == "'":
        return player.strip("'")
    return player

# adapted from https://stackoverflow.com/questions/18425225/getting-the-name-of-a-variable-as-a-string
def retrieve_name(var):
    callers_local_vars = inspect.currentframe().f_back.f_locals.items()
    return [var_name for var_name, var_val in callers_local_vars if var_val is var][0]


def winner_from_scores(team1score, team2score):
    if team1score > team2score: return '1'
    if team2score > team1score: return '2'
    else: return None

class PlayerInfo:
    def __init__(self):
        self.data = {}
        for game in games:
            players = pd.read_csv(f'data/processed/{game}_players.csv')
            id_to_birthdate = {row['pagename'] : row['birthdate'] for _, row in players.iterrows()}
            self.data[game] = deepcopy(id_to_birthdate)

    def age(self, player, game, date):
        birthdate = self.data[game].get(player, '1970-01-01')
        if birthdate == '1970-01-01':
            return None
        birthdate = date.fromisoformat(birthdate)
        age = int((date - birthdate).days // 365.25)
        return age


# from https://github.com/sublee/trueskill/issues/1#issuecomment-149762508
def win_probability(team1, team2):
    delta_mu = sum(r.mu for r in team1) - sum(r.mu for r in team2)
    sum_sigma = sum(r.sigma ** 2 for r in itertools.chain(team1, team2))
    size = len(team1) + len(team2)
    denom = math.sqrt(size * (trueskill.BETA * trueskill.BETA) + sum_sigma)
    ts = trueskill.global_env()
    return ts.cdf(delta_mu / denom)
