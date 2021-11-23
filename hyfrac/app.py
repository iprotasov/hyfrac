# Run this app with `python app.py` and
# visit http://127.0.0.1:8050/ in your web browser.

import json
import numpy as np
import dash
from dash import html
from dash import dcc
from dash.dependencies import Input, Output, State
import time
import model
import plotly.express as px
import plotly.graph_objects as go

def generate_input_field(name, id_name, value):
    return html.Div([
        html.H4(name,style={'display':'inline-block', 'margin-left': 5, 'margin-top':5, 'margin-right':20}),
        dcc.Input(id=id_name, type='number', value=value, debounce=True, style={'width': '50px' , 'border': '1px solid black'})
                ], style={'height': '40px', 'width': '100%'})

app = dash.Dash(__name__)
application = app.server

app.layout = html.Div(children=[

    dcc.Store(id='memory'),

    html.H1(children='hyfrac'),

    html.Div([
        generate_input_field('q', 'q-par', '50'),
        generate_input_field('nu', 'nu-par', '0.2'),
        generate_input_field('dt', 'dt-par', '1'),
        generate_input_field('dx', 'dx-par', '1'),
        generate_input_field('E', 'e-par', str(15/(1-0.2**2))),
        generate_input_field('mu', 'mu-par', str(12*1e-10)),
        generate_input_field('K', 'k-par', str(4*(2/np.pi)**(1/2)*1)),
        generate_input_field('h', 'h-par', str(50)),
        generate_input_field('t', 't-par', str(100)),
        generate_input_field('Cp', 'cp-par', str(2*3*1e-6*1e3)),
        generate_input_field('N', 'n-par', str(10)),
        ], style={'float': 'left', 'width': '300px', 'height': '800px'}),

    html.Div([
        html.Div([
            #dcc.Graph(id='output-fig', figure=dict(data=[{'x': [], 'y': []}], layout=dict(xaxis=dict(range=[-100 ,100]), yaxis=dict(range=[0, 10]), updatemenus=[dict(type="buttons",buttons=[dict(label="Play",method="animate",args=[None])])]), frames=[dict(data=[{'x': [0], 'y': [0]}]), dict(data=[{'x': [1], 'y': [1]}])])),
            dcc.Graph(id='output-fig', figure=go.Figure()),
            dcc.Graph(id='output-fig-conv', figure=go.Figure()),
            ], style={'width': '600px', 'height': '600px'}),
        html.Div(id='output-text', children='', style={'width': '600px', 'height': '40px'}),
        html.Div([
            dcc.Loading(
                        id='loading',
                        type='default',
                        fullscreen=False,
                        children=''),
        ], style={'width': '300px', 'height': '40px'}),
        html.Button(id='submit-button', n_clicks=None, children='Submit'),
        ], style={'float':'left', 'width': '600px', 'height': '800px'}),
])

@app.callback(
        Output('output-fig', 'figure'),
        Output('output-fig-conv', 'figure'),
        Output('output-text', 'children'),
        Output('memory', 'data'),
        Output('loading', 'children'),
        Input('q-par', 'value'),
        Input('nu-par', 'value'),
        Input('dt-par', 'value'),
        Input('dx-par', 'value'),
        Input('e-par', 'value'),
        Input('mu-par', 'value'),
        Input('k-par', 'value'),
        Input('h-par', 'value'),
        Input('t-par', 'value'),
        Input('cp-par', 'value'),
        Input('n-par', 'value'),
        Input('submit-button', 'n_clicks'),
        State('memory', 'data'))
def update_problem_parameters(q_par,nu_par,dt_par,dx_par,e_par,mu_par,k_par,h_par,t_par,cp_par,n_par,n_clicks, data):
    if not n_clicks:
        initial_model = model.compute_initial_solution(float(nu_par),
                                float(e_par),
                                float(k_par),
                                float(cp_par),
                                float(mu_par),
                                float(q_par),
                                float(h_par),
                                int(n_par),
                                float(dt_par),
                                float(t_par))
        new_model = initial_model
        solution = new_model.solution
        fig = px.scatter(x=solution.x_vector, y=solution.w_vector, range_x=[-100,100], range_y=[0, 10], width=600, height=300)
        #fig = (dict(x=[solution.x_vector], y=[solution.w_vector]), [0], 10)
        conv_fig = px.scatter(x=solution.x_vector, y=solution.w_vector, range_x=[-100,100], range_y=[0, 10], width=600, height=300)
        return fig, conv_fig, f'Time = {int(new_model.parameters.t)} s, Initial model', new_model.asdict(), ''
    else:
        initial_model = model.Model.fromdict(data)
        try:
            new_model = initial_model.compute_next()
        except Exception as e:
            raise
            solution = initial_model.solution
            fig = px.scatter(x=solution.get_x_plot(), y=solution.get_w_plot(), range_x=[-100,100], range_y=[0, 10])
            conv_fig = px.scatter(y=initial_model.problem.convergence, log_y=True)
            return fig, conv_fig, f'{e}', initial_model.asdict(), ''


    solution = new_model.solution

    fig = px.scatter(x=solution.get_x_plot(), y=solution.get_w_plot(), range_x=[-100,100], range_y=[0, 10])
    #fig = dict(x=solution.get_x_plot(), y=solution.get_w_plot())
    conv_fig = px.scatter(y=initial_model.problem.convergence, log_y=True)

    return fig, conv_fig, f'Time = {int(new_model.parameters.t)} s, {new_model.solution.dl_vector[0]}', new_model.asdict(), ''


if __name__ == '__main__':
    application.run(debug=True, host='172.31.35.145')

