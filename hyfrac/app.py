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
    html.H1(children='Frequency Band Calculation'),

    html.Div(children='This app calculates the frequency bands'),

    html.Button(id='submit-button', n_clicks=None, children='Submit'),

    html.Div(id='output-text', children='hey'),

    html.Div(id='output-fig', children='hey')
])

@app.callback(Output('output-fig', 'children'),
              Input('submit-button', 'n_clicks'))
def update_text(n_clicks):
    if not n_clicks:
        raise PreventUpdate
    return dcc.Loading(
            id='loading',
            type='default',
            children=dcc.Graph(id='figure'))

@app.callback(Output('figure', 'figure'),
              Output('output-text', 'children'),
              Input('output-fig','children'))
def update_text2(children):
    solution = model.test()
    fig = px.line(x=solution.x_vector,y=solution.w_vector)
    out_text = solution.p_vector[0]
    out_text = f'{(solution.w_vector*solution.h_vector*solution.dl_vector).sum()}\n,{solution.fracture_volume}'
    return fig, out_text

if __name__ == '__main__':
    application.run(debug=True, host='172.31.35.145')

