from cProfile import label
from turtle import title
from dash import Dash, dcc, html, Input, Output
import plotly.express as px

app = Dash(__name__)

app.layout = html.Div(children=[
    html.Div(
        id='header',
        children=[
            html.H1(children='Model Drift Detection', id="title"),
            dcc.Dropdown(
                    id="dropDownVariables",
                    options=[
                        {'label': 'Prediction', 'value': 'x'},
                        {'label': 'Feature: x', 'value': 'fx'},
                        {'label': 'Feature: y', 'value': 'fy'},
                    ],
                ),
            html.Button(
                id="startBTN",
                children='Start')
        ]
    ),
    html.Div(
        id='content',
            children=[
                dcc.Graph(
                    id="graph", style={"float": "left"}),
                dcc.Graph(
                    style={"float": "right"},
                    id="graph2"),
                dcc.Dropdown(id='names', value='day', clearable=False, style={"display": "none"}),
            ]
        
    )
])

@app.callback(
    Output("graph", "figure"), 
    Input("names", "value"))
def generate_chart(names):
    df = px.data.tips() # replace with your own data source
    fig = px.pie(df, names=names, hole=.3)
    return fig

@app.callback(
    Output("graph2", "figure"), 
    Input("names", "value"))
def generate_chart(names):
    df = px.data.tips() # replace with your own data source
    fig = px.pie(df, names=names, hole=.3)
    return fig

if __name__ == '__main__':
    app.run_server(debug=True)