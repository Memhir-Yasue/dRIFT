from cProfile import label
from re import template
from turtle import title
from click import style
from dash import Dash, dcc, html, Input, Output
import plotly.express as px
import pandas as pd
import numpy as np

app = Dash(__name__)

axis = [{'label': "Income", "value": "Income"},
        {"label": 'Loaning Risk', "value": "Loaning Risk"},
        {"label": 'Credit', "value": "Credit"},
        {"label": 'Finance', "value": "Finance"},
        {"label": 'Health', "value": "Health"},
        {"label": 'Social Media', "value": "SocialMedia"},
        {"label": "Base", "value": "base_value"},
        {"label": "Outcome", "value": "outcome"}]

app.layout = html.Div(children=[
    html.Div(
        id='header',
        children=[
            html.H1(children='Shapley Drift', id="title"),
            dcc.Dropdown(
                    id="dropDownVariablesX",
                    value="Income",
                    options=axis,
                    placeholder="x-axis",
                ),
            dcc.Dropdown(
                    id="dropDownVariablesY",
                    value="outcome",
                    options=axis,
                    placeholder="y-axis"
                ),
        ]
    ),
    html.Div(
        id='content',
        children=[
            dcc.Graph(id="graph1", style={"float": "left"}),
            html.Div(id="rGraphs", children=[
                dcc.Graph(id="graph2"),
                dcc.Graph(id="graph3"),
            ], style={"float": "right"}),
        ]
    ),
])

@app.callback(
    Output("graph1", "figure"),
    Input("dropDownVariablesX", "value"),
    Input("dropDownVariablesY", "value"),
    )
def generate_chart(dropDownVariablesX, dropDownVariablesY):
    all_shap = pd.read_parquet('Drift/shap.parquet')
    fig = px.scatter(all_shap, x=dropDownVariablesX, y=dropDownVariablesY, animation_frame="Model Num", color="Race",
                     hover_name="outcome", template='plotly_dark', title="SHAP Feature values Drift")
    return fig

@app.callback(
    Output("graph2", "figure"),
    Input("dropDownVariablesX", "value"),
    ) 
def generate_chart(dropDownVariablesX):
    group_shap = pd.read_parquet('Drift/group_shap.parquet')
    fig = px.bar(group_shap, x='Model Num',
                 y=['Income', 'Credit', 'Loaning Risk', 'Travel', 'Finance', 'Health', 'SocialMedia'], template='plotly_dark',
                 title="Cumulative Feature Contribution (SHAP abs magnitude)")
    return fig

@app.callback(
    Output("graph3", "figure"),
    Input('dropDownVariablesX', 'value'),
    ) 
def generate_chart(dropDownVariablesX):
    all_shap = pd.read_parquet('Drift/shap.parquet')

    total = all_shap.shape[0]

    b_accepted = len(np.where((all_shap['Race'] == 'Black') & (all_shap['outcome'] >= 0.5))[0])
    #b_rejected = len(np.where((all_shap['Race'] == 'Black') & (all_shap['outcome'] < 0.5)))[0]

    w_accepted = len(np.where((all_shap['Race'] == 'White') & (all_shap['outcome'] >= 0.5))[0])
    #w_rejected = len(np.where((all_shap['Race'] == 'White') & (all_shap['outcome'] < 0.5)))[0]


    tmp_data = {'Acceptance': [b_accepted/total, w_accepted/total],
                'Race': ['Black', 'White']}

    tmp_df = pd.DataFrame(tmp_data)
    fig = px.pie(tmp_df, values='Acceptance', names='Race', template='plotly_dark', title="Loan Approval Rate by Race")
    return fig


if __name__ == '__main__':
    app.run_server(debug=True)
