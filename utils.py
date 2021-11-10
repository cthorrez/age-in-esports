import json
import pandas as pd

def winner_from_scores(team1score, team2score):
    if team1score > team2score: return '1'
    if team2score > team1score: return '2'
    else: return None