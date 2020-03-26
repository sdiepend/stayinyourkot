import flask
import dash
import dash_table
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go
import plotly.figure_factory as ff
from dash.dependencies import Input, Output

import requests
import json
import pandas as pd

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

server = flask.Flask(__name__) # define flask app.server
app = dash.Dash(__name__, external_stylesheets=external_stylesheets, server=server)

df_cases_death = pd.read_csv("https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_19-covid-Deaths.csv")
#fig_cases_death = go.Figure(data=[go.Scatter(x=df_cases_death.iloc[0][4:], y=df_cases_death[df_cases_death['Country/Region'] == 'Belgium'].iloc[0][4:])])

# Read the data from github
df_cases_belgium = pd.read_csv("https://raw.githubusercontent.com/sdiepend/stayinyourkot/master/COVID19_Belgium_cases.csv")

# Select only the severe cases columns
df_belgium_severe = df_cases_belgium[['date', 'death', 'icu', 'capacity_icu', 'hospitalized']][16:]

# Correctly format icu and hospitalized
df_belgium_severe[['icu', 'hospitalized']] = df_belgium_severe[['icu', 'hospitalized']].astype(int)

# create a table figure (ff = figure factory)
table_severe = ff.create_table(df_belgium_severe)

# create line chart for the severe cases
fig_severe = go.Figure()
fig_severe.update_yaxes(range=[0, 3000])
fig_severe.add_trace(go.Scatter(x=df_belgium_severe['date'], y=df_belgium_severe['death'], name='deaths', text=["ICU Capacity"]))
fig_severe.add_trace(go.Scatter(x=df_belgium_severe['date'], y=df_belgium_severe['icu'], name='icu'))
fig_severe.add_trace(go.Scatter(x=df_belgium_severe['date'], y=df_belgium_severe['hospitalized'], name='hospitalized'))
fig_severe.add_trace(go.Scatter(x=df_belgium_severe['date'], y=df_belgium_severe['capacity_icu'], name='ICU Capacity', 
            line=dict(
                color="RoyalBlue",
                dash="dashdot",
            )))

app.layout = html.Div(style={}, children=[
    html.H1(children='Dashboard',
        style={
            'textAlign': 'center',
        }
    ),

    html.Div(className='row', style={'display': 'flex'}, children=[
        html.Div(className='col s12 m6', children=[
            dcc.Graph(
                id='table-severe-belgium',
                figure=table_severe
            )]
        ),

        html.Div(className='col s12 m6', children=[
            dcc.Graph(
                id='fig-severe-belgium',
                figure=fig_severe
            )]
        )]
    ),


    # dcc.Graph(
    #     id='cases-death',
    #     figure=fig_cases_death
    # ),
])

if __name__ == '__main__':
    app.run_server()