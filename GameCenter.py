from dash import Dash, dcc, html, dash_table, Input, Output, State, callback_context
from GameConstructor import *

# Dropdowns
teamDropdown = dcc.Dropdown(options = teamAbbrev, value= 'CAR', id = 'teamSelected')
gameDropdown = dcc.Dropdown(options = [], id = 'gameSelected')

# Structures
gameScoreboard = dbc.Container(id = 'Game Interface')

# Data kept
gameData = dcc.Store(id = 'Game Data', data = {})
gameShifts = dcc.Store(id = 'Game Shifts', data = [])
storage = [gameData, gameShifts]