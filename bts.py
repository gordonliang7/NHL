from dash import Dash, dcc, html, dash_table, Input, Output, State, callback_context
import dash_bootstrap_components as dbc
from util import path_to_image

neural_network_description = '''A player's contract projection is determined by using a special Recurrent Neural Network\
 called Long Short Term Memory (LSTM). LSTM's are fit for this problem because, as the name implies, they discount older\
 input. So for example, if Alex Ovechkin hit the open market suddenly, I wouldn't want to offer him a contract for\
 the 100+ point player he was a decade ago. Then, after getting outputs from the LSTM, we added a linear layer with a\
  a non-linear activation before using a final layer to reduce our output to two numbers: Cap% and Years.
  \n
  \n
  Note that, because this is trained on actual contracts including recent ones from active players, some projections\
   might look exactly like their current contract because the data is from information that the model has literally\
    seen with an added season. (ex: Michael Bunting)'''

bts_layout = dbc.Container([dbc.Row(html.H1('How the Contract Projections Work...')),
                            dbc.Row([dbc.Col(html.H2(neural_network_description))]),
                            dbc.Row(html.Img(src= path_to_image('Salary Neural Network.jpg'),
                                             style={'height': 'auto', 'max-width': '100%'}))])
