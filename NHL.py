import pandas as pd
import numpy as np
from dash import Dash, dcc, html, dash_table, Input, Output, State, callback_context
import dash_bootstrap_components as dbc
from NHL_API import *
import GameCenter as gc
import GameConstructor as game
import ContractConstructor as contract
import Contracts as cc
from util import path_to_image, pickRandom, translate_col, makeButton
from bts import bts_layout
import Guess as gg
import PlayerStats as ps
import StatsConstructor as sc

#print(playerToInfo(8477404))

gap = html.Div(style={'height': '20px'})

app = Dash(
    __name__,
    external_stylesheets=[dbc.themes.MORPH])
server = app.server

gamecenter_layout = dbc.Container([dbc.Row([dbc.Col(gc.teamDropdown), dbc.Col(gc.gameDropdown)]),
                            gc.gameScoreboard] + gc.storage, fluid = True)

contract_layout = dbc.Container([dbc.Row([dbc.Col(cc.teamDropdown), dbc.Col(cc.playerDropdown)]),
                                 dbc.Row(cc.playerCard), cc.playerData], fluid = True)

stats_layout = dbc.Container([dbc.Row([dbc.Col(ps.teamDropdown), dbc.Col(ps.playerDropdown)]),
                                 dbc.Row(ps.playerCard), ps.playerData], fluid = True)

guess_layout = dbc.Container([dbc.Row(gg.choosePlayerButton),
                              dbc.Row(gg.player_info),
                              dbc.Row(gg.buttons), gg.players])

# gamePlayTable = dash_table.DataTable([],id = 'shiftTable')
# teamImage = html.Img(src = '', id = 'teamIMG')

# Gamecenter Callbacks


@app.callback(Output(component_id='gameSelected', component_property='options'),
              Input(component_id='teamSelected', component_property='value'))
def updateGameDropdown(team):
    '''When the user selects a team, the dropdown shows games to select'''
    games = ask(f'https://api-web.nhle.com/v1/club-schedule-season/{team}/now')['games']
    return seasonToGames(games, team)


@app.callback(Output(component_id='Game Data', component_property='data'),
              Output(component_id='Game Shifts', component_property='data'),
              Input(component_id='gameSelected', component_property='value'))
def updateTeamImage(gameID):
    '''When the user selects a game, the data is collected from the NHL API
    and the respective components are updated'''
    if gameID is None:
        return {}, []
    game_data = getGame(gameID)
    shifts = ask(f'https://api.nhle.com/stats/rest/en/shiftcharts?cayenneExp=gameId={gameID}')['data']
    return game_data, shifts


@app.callback(Output(component_id='Game Interface', component_property='children'),
              Input(component_id='Game Data', component_property='data'),
              Input(component_id='Game Shifts', component_property='data'))
def updateGameInterface(data, shifts):
    if data == {}:
        return None
    return game.makeScoreboard(data, shifts)

# Contract Callbacks


@app.callback(Output(component_id= 'playerSelectedContract', component_property= 'options'),
              Input(component_id= 'teamSelectedContract', component_property= 'value'))
def updateContractPlayerDropdown(team):
    roster = getRoster(team)
    return [{'label': f'{i["Name"]} ({i["#"]})', 'value': i['Player ID']} for i in roster if i['Player ID']]


@app.callback(Output(component_id= 'Contract Player Data', component_property= 'data'),
              Input(component_id= 'playerSelectedContract', component_property= 'value'))
def retrievePlayerContractProjection(playerId):
    if playerId is None:
        return {}
    return contract.playerToInfo(playerId)


@app.callback(Output(component_id= 'Contract Player Interface', component_property= 'children'),
              Input(component_id= 'Contract Player Data', component_property= 'data'))
def updatePlayerContractInterface(data):
    if data == {}:
        return None
    return contract.makeInterface(data)


# Guess Player Callbacks

@app.callback((Output(component_id= 'player_choices_guess', component_property= 'data')),
              Input(component_id= 'choose player button', component_property= 'n_clicks'))
def pickPlayers(_):
    players = pickRandom()
    #print(players)
    correct_player = np.random.choice(players)
    others = [i['skaterFullName'] for i in players if i != correct_player]
    return {'Correct Player': correct_player, 'Other Players': others}


@app.callback(Output(component_id= 'Guessing Buttons', component_property= 'children'),
              Input(component_id= 'player_choices_guess', component_property= 'data'))
def makeButtons(data):
    correctButton = makeButton(data['Correct Player']['skaterFullName'], 'Correct Button')
    other_buttons = [makeButton(data['Other Players'][i],
                                f'wrong button {i+1}') for i in range(len(data['Other Players']))]
    all_buttons = other_buttons + [correctButton]
    shuffled_index = np.random.choice(range(len(all_buttons)), size = len(all_buttons), replace= False)
    return html.Div([all_buttons[i] for i in shuffled_index], className= "d-grid gap-2")


@app.callback(Output(component_id= 'Correct Player Info', component_property= 'children'),
              Input(component_id= 'player_choices_guess', component_property= 'data'))
def show_data(data):
    player = data['Correct Player'].copy()
    toi = player['timeOnIcePerGame']
    player['timeOnIcePerGame'] = f'{int(toi//60)}:{0 if toi%60 < 10 else ""}{int(toi%60)}'
    total_chain, current_chain = [], []
    for key in player.keys():
        if key in ['skaterFullName', 'Cluster']:
            continue
        current_chain += [dbc.Col([
                html.Span(str(player[key]), style={'fontSize': '2em', 'marginRight': '10px'}),
                html.Span(translate_col[key], style={'fontSize': '1em'})
            ])]
        if len(current_chain) == 3:
            total_chain += [dbc.Row(current_chain)]
            current_chain = []
    if len(current_chain) > 0:
        total_chain += [dbc.Row(current_chain)]
    print(total_chain)
    return total_chain


@app.callback(Output(component_id= 'Correct Button', component_property= 'color'),
              Output(component_id= 'wrong button 1', component_property= 'color'),
              Output(component_id= 'wrong button 2', component_property= 'color'),
              Output(component_id= 'wrong button 3', component_property= 'color'),
              Input(component_id= 'Correct Button', component_property= 'n_clicks_timestamp'),
              Input(component_id= 'wrong button 1', component_property= 'n_clicks_timestamp'),
              Input(component_id= 'wrong button 2', component_property= 'n_clicks_timestamp'),
              Input(component_id= 'wrong button 3', component_property= 'n_clicks_timestamp'))
def updateColors(right, w1, w2, w3):
    print('clicked')
    args, colors = [right, w1, w2, w3], ['light' for i in range(4)]
    max_time = max(args)
    if max_time == right:
        colors[0] = 'success'
    for i in range(1,4):
        if max_time == args[i]:
            colors[i] == 'danger'
    print(colors)
    return tuple(colors)

# Stats Callbacks


@app.callback(Output(component_id= 'playerSelectedStats', component_property= 'options'),
              Input(component_id= 'teamSelectedStats', component_property= 'value'))
def updateStatsPlayerDropdown(team):
    roster = getRoster(team, True, True, filter_out= False)
    return [{'label': f'{i["Name"]} ({i["#"]})', 'value': i['Player ID']} for i in roster if i['Player ID']]

@app.callback(Output(component_id= 'Stats Player Data', component_property= 'data'),
              Input(component_id= 'playerSelectedStats', component_property= 'value'))
def updatePlayerStatsGlobal(playerID):
    if playerID is None:
        return {}
    return sc.playerToInfo(playerID)

@app.callback(Output(component_id= 'Stats Player Interface', component_property= 'children'),
              Input(component_id= 'Stats Player Data', component_property= 'data'))
def makePreliminaryPlayerStatsInterface(data):
    if data == {}:
        return None
    return sc.makeInterface(data)

@app.callback(Output(component_id= 'Player Stats Table', component_property= 'children'),
              Input(component_id= 'Stats Player Data', component_property= 'data'),
              Input(component_id= 'Player Query', component_property= 'value'))
def makePreliminaryPlayerStatsInterface(data, query):
    if query is None:
        return None
    return sc.makeStatsTable(data['Player ID'], query)



# Total Layout


contentTabs = dcc.Tabs(id="content", value='contracts', children=[
    dcc.Tab(label='Contract Projections', value='contracts', children = contract_layout),
    dcc.Tab(label = 'Player Stats', children = stats_layout),
    dcc.Tab(label = 'GUESS A PLAYER (PROB NEVER COMING)', value = 'guess', children= guess_layout, disabled = True),
    dcc.Tab(label='Game Center (WORK IN PROGRESS... ALSO PROB NEVER)', value='games', children = gamecenter_layout, disabled = True),
    dcc.Tab(label = 'Faceoffs (COMING SOON... IF I AM NOT LAZY)', disabled = True),
    dcc.Tab(label = 'Behind The Scenes', children= bts_layout)
])

logo = html.Img(src=path_to_image('Logo.jpg'))

app.layout = dbc.Container([dbc.Row(logo, style={'marginBottom': '30px'}),
                            dbc.Row(contentTabs)], fluid=True)
if __name__ == "__main__":
    app.run_server(debug=True)
