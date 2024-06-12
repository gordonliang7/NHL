from NHL_API import *
from util import *
from dash import Dash, dcc, html, dash_table, Input, Output, State, callback_context
import dash_bootstrap_components as dbc


def playerData(playerId, data = 'summary'):
    query = f'https://api.nhle.com/stats/rest/en/skater/{data}?limit=-1&cayenneExp= playerId = {playerId} and gameTypeId = 2 and seasonId > 20082009'
    df = pd.DataFrame(ask(query)['data'])
    df['sznStart'] = df['seasonId']//10000
    df['sznEnd'] = df['seasonId'] % 10000
    return df.sort_values('seasonId')


cols = [i + indexCols for i in [sumCols, scoringCols, gfaCols, sumshootCols, penCols]]


def playerToStats(playerId):
    df = playerData(playerId, data=queries[0])[cols[0]]
    for query, col in zip(queries[1:], cols[1:]):
        newDF = playerData(playerId, data=query)[col]
        df = df.merge(newDF, on=indexCols, copy=False, validate='one_to_one')
    for col in df.columns.values:
        df[col] = df[col].fillna(0)
    return df


def df_model_prep(df):
    #print(df)
    seasons = list(df['seasonId'])
    df = df.drop(columns = ['playerId']).sort_values('seasonId').set_index('seasonId')
    #print(df)
    #print(df.columns.values)
    df = (df - sznMeans) / sznSTDs
    #print(df)
    #print(df.columns.values)
    return df.filter(items = seasons, axis = 0)


def playerToInfo(playerID):
    '''TO DO: Fix case of Ryan Suzuki where a player hasn't played an NHL Game at all'''
    data = getPlayer(playerID)
    image_src = data['headshot']
    stats = playerToStats(playerID)
    position = data['position']
    pred = forward_UFA.run(df_model_prep(stats))
    cap_perc, term = float(pred[0]), max([float(pred[1]), 1])
    aav = max([cap_perc*cap_history[20242025], 750000])
    return {'image_src': image_src,
            'stats': stats.to_dict('records'),
            'position': position,
            'Predicted AAV': aav,
            'Predicted Cap %': cap_perc,
            'Predicted Term': term,
            'Name': data['firstName']['default'] + ' ' + data['lastName']['default']}


def makeInterface(data):
    stats = []
    for year in data['stats']:
        year_line = year.copy()
        year_line['seasonId'] = f'{year_line["seasonId"]//10000}-{year_line["seasonId"]%10000}'
        year_line['faceoffWinPct'] = round(year_line['faceoffWinPct'] * 100, 3)
        year_line['shootingPct'] = round(year_line['shootingPct'] * 100, 3)
        TOI = round(year_line['timeOnIcePerGame'])
        year_line['timeOnIcePerGame'] =f'{TOI//60}:{TOI%60}'
        stats += [year_line]
    stats_table = dash_table.DataTable(stats,
                                       table_cols,
                                       style_table={'overflowX': 'auto'})
    row_one = dbc.Row([dbc.Col([html.H1(f"{data['Name']} ({data['position']})", style={'fontSize': '24px',
                                                                                       'color': '#333', 'textAlign':
                                                                                           'center', 'margin': '10px 0'}),
                                html.H1(f'Contract Projection if {data["Name"]} was a UFA:', style={'fontSize': '20px',
                                                                                                    'color': '#555',
                                                                                                    'textAlign': 'center',
                                                                                                    'margin': '10px 0'}),
                                html.H1(f"${round(data['Predicted AAV']/1000000, 2)}M AAV", style={'fontSize': '22px',
                                                                                                   'color': '#2e8b57',
                                                                                                   'textAlign': 'center',
                                                                                                   'margin': '10px 0'}),
                                html.H1(f"{round(data['Predicted Term'])} YEARS", style={'fontSize': '22px',
                                                                                         'color': '#1e90ff',
                                                                                         'textAlign': 'center',
                                                                                         'margin': '10px 0'}),
                                html.H1('See "Behind The Scenes" for an explanation of contract projections',
                                        style={'fontSize': '22px',
                                               'color': '#FFFFFF',
                                               'textAlign': 'center',
                                               'margin': '10px 0'})
                                ]),
                       dbc.Col(html.Img(src=data['image_src'], style={'max-width': '100%',
                                                                      'height': 'auto'},
                                        className='d-flex justify-content-center'))],
                      style={'marginBottom': '30px'})
    row_two = dbc.Row(stats_table)
    return dbc.Container([row_one, row_two])


