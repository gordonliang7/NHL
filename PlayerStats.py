import dash_bootstrap_components as dbc
from dash import Dash, dcc, html, dash_table, Input, Output, State, callback_context
#from StatsConstructor import *
from NHL_API import teamAbbrev

# Dropdowns
teamDropdown = dcc.Dropdown(options = teamAbbrev, value= 'CAR', id = 'teamSelectedStats')
playerDropdown = dcc.Dropdown(options = [], id = 'playerSelectedStats')

#Structures
playerCard = dbc.Container(id = 'Stats Player Interface')

# Data Storage
playerData = dcc.Store(id = 'Stats Player Data', data = {})