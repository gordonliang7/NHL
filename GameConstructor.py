import pandas as pd
from dash import Dash, dcc, html, dash_table, Input, Output, State, callback_context
import dash_bootstrap_components as dbc
from NHL_API import *
gap = html.Div(style={'height': '20px'})
center = {'text-align':'center'}


def getTeamLogo(teamAbbrev):
    return f'https://assets.nhle.com/logos/nhl/svg/{teamAbbrev}_light.svg'

def scoreCols(homeTeam, awayTeam, homeScore, awayScore):
    homeLogo = html.Img(src=getTeamLogo(homeTeam), style={'max-width': '100%', 'height': 'auto'})
    awayLogo = html.Img(src=getTeamLogo(awayTeam), style={'max-width': '100%', 'height': 'auto'})
    awayCol = dbc.Col([dbc.Row(awayLogo, align='left'), gap, dbc.Row([html.H1(awayScore)])])
    homeCol = dbc.Col([dbc.Row(homeLogo, align='right'), gap, dbc.Row([html.H1(homeScore)])])
    return homeCol, awayCol


def create_live_game_banner(homeTeam, awayTeam, per, time, homeScore, awayScore):
    homeCol, awayCol = scoreCols(homeTeam, awayTeam, homeScore, awayScore)
    timeCol = dbc.Col([dbc.Row(html.H1('@', style = center)),
                       dbc.Row(html.H1(per, style= center)),
                       dbc.Row(html.H1(time, stile = center))])
    return dbc.Row([awayCol, timeCol, homeCol])

def create_finished_game_banner(homeTeam, awayTeam, homeScore, awayScore):
    homeCol, awayCol = scoreCols(homeTeam, awayTeam, homeScore, awayScore)
    timeCol = dbc.Col([dbc.Row(html.H1('@',style = center)),
                       dbc.Row('FINAL', style = {'font-family': 'monospace', 'text-align': 'center'})])
    return dbc.Row(dbc.Row([awayCol, timeCol, homeCol]))

def makeScoreboard(data, shifts):
    homeTeam = data['homeTeam']['abbrev']
    awayTeam = data['awayTeam']['abbrev']
    homeScore = data['homeTeam']['score']
    awayScore = data['awayTeam']['score']
    gameState = data['gameState']
    if gameState == 'LIVE':
        return create_live_game_banner(homeTeam, awayTeam, 3, '4:20', homeScore, awayScore)
    else:
        if gameState != 'OFF':
            print('wut')
        return create_finished_game_banner(homeTeam, awayTeam, homeScore, awayScore)