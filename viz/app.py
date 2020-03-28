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

#df_cases_death = pd.read_csv("https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_19-covid-Deaths.csv")
#fig_cases_death = go.Figure(data=[go.Scatter(x=df_cases_death.iloc[0][4:], y=df_cases_death[df_cases_death['Country/Region'] == 'Belgium'].iloc[0][4:])])

# Read the data from github
df_cases_belgium = pd.read_csv("https://raw.githubusercontent.com/sdiepend/stayinyourkot/master/COVID19_Belgium_cases.csv")

# Select only the severe cases columns
df_belgium_severe = df_cases_belgium[['date', 'daily_infected', 'death', 'icu', 'capacity_icu', 'hospitalized']][13:]

# Correctly format icu and hospitalized
df_belgium_severe[['icu', 'hospitalized']] = df_belgium_severe[['icu', 'hospitalized']].astype(int)

# create a table figure (ff = figure factory)
table_severe = ff.create_table(df_belgium_severe)

# create line chart for the severe cases
fig_severe = go.Figure()
fig_severe.layout = {'title': 'Severe Cases'}
fig_severe.add_trace(go.Scatter(x=df_belgium_severe['date'], y=df_belgium_severe['death'], name='deaths', line={'color': 'black'}))
fig_severe.add_trace(go.Scatter(x=df_belgium_severe['date'], y=df_belgium_severe['icu'], name='ICU', line={'color' : 'tomato'}))
fig_severe.add_trace(go.Scatter(x=df_belgium_severe['date'], y=df_belgium_severe['hospitalized'], name='hospitalized', line={'color': 'purple'}))
fig_severe.add_trace(go.Scatter(x=df_belgium_severe['date'], y=df_belgium_severe['capacity_icu'], name='ICU Capacity', line={'color': 'tomato', 'dash': 'dashdot'}))

fig_bar_infected_daily = go.Figure()
fig_bar_infected_daily.layout={'title': 'Daily new infections'}
fig_bar_infected_daily.add_trace(go.Bar(x=df_belgium_severe['date'], y=df_belgium_severe['daily_infected']))

app.layout = html.Div(style={}, children=[
    html.H1(children='COVID19 Dashboard',
        style={
            'textAlign': 'center',
        }
    ),

    html.P(
        "ICU capacity as commuincated by the daily update by the FOD Volksgezondheid"
    ),

    dcc.Graph(
        id='fig-severe-belgium',
        figure=fig_severe
    ),

    dcc.Graph(
        id='fig-infected-daily',
        figure=fig_bar_infected_daily
    ),

    dcc.Graph(
        id='table-severe-belgium',
            figure=table_severe
    ),
])

if __name__ == '__main__':
    app.run_server()