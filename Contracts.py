import dash_bootstrap_components as dbc
from dash import Dash, dcc, html, dash_table, Input, Output, State, callback_context
from ContractConstructor import *

# Dropdowns
teamDropdown = dcc.Dropdown(options = teamAbbrev, value= 'CAR', id = 'teamSelectedContract')
playerDropdown = dcc.Dropdown(options = [], id = 'playerSelectedContract')

#Structures
playerCard = dbc.Container(id = 'Contract Player Interface')

# Data Storage
playerData = dcc.Store(id = 'Contract Player Data', data = {})
