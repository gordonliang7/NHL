from NHL_API import *
from util import *
from dash import Dash, dcc, html, dash_table, Input, Output, State, callback_context
import dash_bootstrap_components as dbc

# Want it to go from Team -> Player -> Player Card -> Table

def makeStatsTable(playerId, query):
    data = ask(f'https://api.nhle.com/stats/rest/en/skater/{query}?limit=-1&cayenneExp= playerId=={playerId}')
    #print(data)
    if data is None:
        return html.H1(f"NO QUERY SELECTED", style={'fontSize': '24px',
                                                    'color': '#333',
                                                    'textAlign': 'center',
                                                    'margin': '10px 0'})
    data = data['data']
    if len(data) == 0:
        return html.H1(f"NO DATA AVAILABLE", style={'fontSize': '24px',
                                                     'color': '#333',
                                                     'textAlign': 'center',
                                                     'margin': '10px 0'})
    return dash_table.DataTable(data,
                         make_col_list(list(data[0].keys())),
                         style_table={'overflowX': 'auto'})

def playerToInfo(playerID):
    '''TO DO: Fix case of Ryan Suzuki where a player hasn't played an NHL Game at all'''
    data = getPlayer(playerID)
    image_src = data['headshot']
    position = data['position']
    return {'image_src': image_src,
            'position': position,
            'Name': data['firstName']['default'] + ' ' + data['lastName']['default'],
            'Player ID': playerID}


def makeInterface(data):
    row_one = dbc.Row([dbc.Col([html.H1(f"{data['Name']} ({data['position']})", style={'fontSize': '24px',
                                                                                       'color': '#333', 'textAlign':
                                                                                           'center', 'margin': '10px 0'}),
                                dcc.Dropdown(id = 'Player Query',
                                             options = [{'label': nice,
                                                         'value': ugly} for nice, ugly in zip(niceQueries, allQueries)],
                                             value = 'Summary')
                                ]),
                       dbc.Col(html.Img(src=data['image_src'], style={'max-width': '100%',
                                                                      'height': 'auto'},
                                        className='d-flex justify-content-center'))],
                      style={'marginBottom': '30px'})
    row_two = dbc.Container(id = 'Player Stats Table')
    return dbc.Container([row_one, row_two])