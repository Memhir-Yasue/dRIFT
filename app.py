from cProfile import label
from re import template
from turtle import title
from click import style
from dash import Dash, dcc, html, Input, Output
import plotly.express as px
import pandas as pd

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
            dcc.Graph(id="graph", style={"float": "left"}),
            html.Div(id="rGraphs", children=[
                dcc.Graph(id="graph2"),
                dcc.Graph(id="graph3"),
            ], style={"float": "right"}),
        ]
    ),
])

@app.callback(
    Output("graph", "figure"), 
    Input("dropDownVariablesX", "value"),
    Input("dropDownVariablesY", "value"),
    )
def generate_chart(dropDownVariablesX, dropDownVariablesY):
    all_shap = pd.read_parquet('Drift/shap.parquet')
    fig = px.scatter(all_shap, x=dropDownVariablesX, y=dropDownVariablesY, animation_frame="Model Num", color="Race", hover_name="outcome", template='plotly_dark')
    return fig

@app.callback(
    Output("graph2", "figure"),
    Input("dropDownVariablesX", "value"),
    ) 
def generate_chart(dropDownVariablesX):
    all_shap = pd.read_parquet('Drift/group_shap.parquet')
    fig = px.scatter(all_shap, x='Pred', color="Race", hover_name="Pred", template='plotly_dark')
    return fig

@app.callback(
    Output("graph3", "figure"),
    Input("dropDownVariablesX", "value"),
    ) 
def generate_chart(dropDownVariablesX):
    all_shap = pd.read_parquet('Drift/group_shap.parquet')
    fig = px.bar(all_shap, x='Race', color="Race", hover_name="Pred", template='plotly_dark')
    return fig

if __name__ == '__main__':
    app.run_server(debug=True)