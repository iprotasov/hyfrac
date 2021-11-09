# Run this app with `python app.py` and
# visit http://127.0.0.1:8050/ in your web browser.

import numpy as np
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
import time
import model
import plotly.express as px

app = dash.Dash(__name__)
application = app.server

app.layout = html.Div(children=[
    html.H1(children='hyfrac'),

    html.Div(children='hyfrac testing'),

    html.Button(id='submit-button', n_clicks=None, children='Submit'),

    html.Div(id='output-text', children=''),

    html.Div(id='output-fig', children='')
])

@app.callback(Output('output-fig', 'children'),
              Input('submit-button', 'n_clicks'))
def update_text(n_clicks):
    if not n_clicks:
        raise PreventUpdate
    return dcc.Loading(
            id='loading',
            type='default',
            children=[dcc.Graph(id='figure'),
                      dcc.Graph(id='figure2')])

@app.callback(Output('figure', 'figure'),
              Output('figure2', 'figure'),
              Output('output-text', 'children'),
              Input('output-fig','children'))
def update_text2(children):
    solution, new_solution = model.test()
    fig = px.line(x=solution.x_vector,y=solution.w_vector)
    fig2 = px.line(x=new_solution.x_vector,y=new_solution.w_vector)
    out_text = f'{new_solution.p_vector}'
    return fig, fig2, out_text

if __name__ == '__main__':
    application.run(debug=True, host='172.31.35.145')

