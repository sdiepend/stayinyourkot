import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go
from dash.dependencies import Input, Output

import requests
import json
import pandas as pd

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
df_cases_death = pd.read_csv("https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_19-covid-Deaths.csv")
fig_cases_death = go.Figure(data=[go.Scatter(x=df_cases_death.iloc[0][4:], y=df_cases_death[df_cases_death['Country/Region'] == 'Belgium'].iloc[0][4:])])

app.layout = html.Div(style={}, children=[
    html.H1(children='Dashboard',
        style={
            'textAlign': 'center',
        }
    ),

    dcc.Graph(
        id='cases-death',
        figure=fig_cases_death
    ),
])

if __name__ == '__main__':
    app.run_server(debug=True, host='0.0.0.0', port=8050)