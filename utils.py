import json
import pandas as pd
from copy import deepcopy
from datetime import date
from config import games

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
