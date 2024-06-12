import pandas as pd
from dash import Dash, dcc, html, dash_table, Input, Output, State, callback_context
import dash_bootstrap_components as dbc
from NHL_API import *
import GameCenter as gc
import GameConstructor as game
import ContractConstructor as contract
import Contracts as cc
from util import path_to_image
from bts import bts_layout

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

# Total Layout


contentTabs = dcc.Tabs(id="content", value='contracts', children=[
    dcc.Tab(label='Contract Projections', value='contracts', children = contract_layout),
    dcc.Tab(label='Game Center (WORK IN PROGRESS)', value='games', children = gamecenter_layout, disabled = True),
    dcc.Tab(label = 'Faceoffs (COMING SOON)', disabled = True),
    dcc.Tab(label = 'Behind The Scenes', children= bts_layout)
])


logo = html.Img(src=path_to_image('Logo.jpg'))

app.layout = dbc.Container([dbc.Row(logo, style={'marginBottom': '30px'}),
                            dbc.Row(contentTabs)], fluid=True)
if __name__ == "__main__":
    app.run_server(debug=True)
