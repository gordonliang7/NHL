from requests import get
import pandas as pd
from util import bad_players
import datetime as dt
import numpy as np
from math import atan as arctan, degrees


def readThrough(lst,key):
    return [i[key] if key in i.keys() else None for i in lst]


def ask(link):
    '''Input: Link (str)
    Output: Json of Info (dict)'''
    return get(link).json()


def form(num):
    if num < 10:
        return '0' + str(num)
    return num

def getPlayer(player):
    '''Input: Player ID (int)
    Output: JSON of player info
    Keys: 'playerId', 'isActive', 'currentTeamId', 'currentTeamAbbrev', 'fullTeamName', 'firstName',
    'lastName', 'teamLogo', 'sweaterNumber', 'position', 'headshot', 'heroImage', 'heightInInches',
    'heightInCentimeters', 'weightInPounds', 'weightInKilograms', 'birthDate', 'birthCity', 'birthCountry',
    'shootsCatches', 'draftDetails', 'playerSlug', 'inTop100AllTime', 'inHHOF', 'featuredStats', 'careerTotals',
    'shopLink', 'twitterLink', 'watchLink', 'last5Games', 'seasonTotals', 'currentTeamRoster' '''
    return ask(f'https://api-web.nhle.com/v1/player/{player}/landing')

def getGame(gameID):
    query = f'https://api-web.nhle.com/v1/gamecenter/{gameID}/play-by-play'
    return ask(query)


teamAbbrev = sorted([i['default'] for i in pd.DataFrame(get('https://api-web.nhle.com/v1/standings/now').json()['standings'])['teamAbbrev']])


def doHome(data):
    res = ''
    if data['gameState'] == 'LIVE':
        res = 'LIVE'
    elif data['awayTeam']['score'] > data['homeTeam']['score']:
        res = 'L'
    else:
        res = 'W'
    return f'{res} vs {data["awayTeam"]["abbrev"]} ({data["gameDate"]})'

def getRoster(team, forwards = True, defensemen = False, goalies = False, filter_out = True):
    data = ask(f'https://api-web.nhle.com/v1/roster/{team}/20232024')
    roster = []
    extract = lambda x: [{'Player ID': i['id'], 'Name': i['firstName']['default'] + ' ' + i['lastName']['default'],
                          '#': i.get('sweaterNumber', 'NA')} for i in x]
    pos = ['forwards', 'defensemen', 'goalies']
    for positional_data, include in zip(pos, [forwards, defensemen, goalies]):
        if include:
            roster += extract(data[positional_data])
    if not filter_out:
        return roster
    return [i for i in roster if i['Player ID'] not in bad_players]


def doAway(data):
    res = ''
    if data['gameState'] == 'LIVE':
        res = 'LIVE'
    elif data['awayTeam']['score'] < data['homeTeam']['score']:
        res = 'L'
    else:
        res = 'W'
    return f'{res} @ {data["homeTeam"]["abbrev"]} ({data["gameDate"]})'


def seasonToGames(data, team):
    '''Input: data- list of dictionaries with each representing a game
    team- the team which the perspective is from

    Output: list of dictionaries {label: game label, value: GAME ID}'''
    return [{'label': doHome(game) if game['homeTeam']['abbrev'] == team else doAway(game),
            'value':game['id']} for game in data if game['gameState'] in ['OFF', 'LIVE']]


def getGame(gameID):
    '''Input : gameID- int
    Output: dictionary of game information'''
    query = f'https://api-web.nhle.com/v1/gamecenter/{gameID}/play-by-play'
    return ask(query)

