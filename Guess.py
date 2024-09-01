import numpy as np
from dash import dcc
import dash_bootstrap_components as dbc
from dash import html

choosePlayerButton = dbc.Button(id = 'choose player button', n_clicks= 0, children= 'RANDOMIZE PLAYER')


players = dcc.Store(id = 'player_choices_guess', data = {})

player_info = dbc.Container(children= [], id = 'Correct Player Info')

names = ['Correct Button', 'wrong button 1', 'wrong button 2', 'wrong button 3']

buttons = dbc.Container(children= [dbc.Button(children= '', id = name, n_clicks_timestamp= 0) for name in names],
                        id = 'Guessing Buttons')
