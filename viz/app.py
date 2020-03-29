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
df_cases_belgium = pd.read_csv("https://raw.githubusercontent.com/sdiepend/stayinyourkot/master/data/COVID19_Belgium_cases.csv")
df_growth_belgium = pd.read_csv("https://raw.githubusercontent.com/sdiepend/stayinyourkot/master/data/COVID19_Belgium_growth.csv")

# Select only the severe cases columns
df_belgium_severe = df_cases_belgium[['date', 'daily_infected', 'daily_deceased', 'deceased', 'icu', 'capacity_icu', 'hospitalized']][13:]
df_growth_belgium_severe = df_growth_belgium[['date', 'daily_infected', 'infected', 'daily_deceased', 'deceased', 'icu', 'capacity_icu', 'hospitalized', 'recoverd']][13:]

# Correctly format icu and hospitalized
df_belgium_severe[['daily_deceased', 'icu', 'hospitalized']] = df_belgium_severe[['daily_deceased', 'icu', 'hospitalized']].astype(int)

# create a table figure (ff = figure factory)
table_severe = ff.create_table(df_belgium_severe)
#table_severe.layout = {'title': 'Data'}

# create line chart for the severe cases
fig_severe = go.Figure()
fig_severe.layout = {'title': 'Severe Cases'}
fig_severe.add_trace(go.Scatter(x=df_belgium_severe['date'], y=df_belgium_severe['deceased'], name='deaths', line={'color': 'black'}))
fig_severe.add_trace(go.Scatter(x=df_belgium_severe['date'], y=df_belgium_severe['icu'], name='ICU', line={'color' : 'tomato'}))
fig_severe.add_trace(go.Scatter(x=df_belgium_severe['date'], y=df_belgium_severe['hospitalized'], name='hospitalized', line={'color': 'purple'}))
fig_severe.add_trace(go.Scatter(x=df_belgium_severe['date'], y=df_belgium_severe['capacity_icu'], name='ICU Capacity', line={'color': 'tomato', 'dash': 'dashdot'}))
fig_severe.add_shape(
    # Line Vertical
    dict(
        type="line",
        x0="3/18/2020",
        x1="3/18/2020",
        y0=0,
        y1=4000,
        line=dict(
            color="RoyalBlue",
            dash="dashdot",
        )
    )
)
fig_severe.add_trace(go.Scatter(x=["3/19/2020"], y=[3500], text=["Lockdown"], mode="text", name="Lockdown"))
fig_severe.add_shape(
    # Line Vertical
    dict(
        type="line",
        x0="3/14/2020",
        x1="3/14/2020",
        y0=0,
        y1=4000,
        line=dict(
            color="RoyalBlue",
            dash="dashdot",
        )
    )
)
fig_severe.add_trace(go.Scatter(x=["3/15/2020"], y=[3500], text=["Lockdown Light"], mode="text", name="Lockdown Light"))


fig_bar_infected_daily = go.Figure()
fig_bar_infected_daily.layout={'title': 'Daily new infections and deaths'}
fig_bar_infected_daily.add_trace(go.Bar(x=df_belgium_severe['date'], y=df_belgium_severe['daily_infected'], name='New Infections'))
fig_bar_infected_daily.add_trace(go.Bar(x=df_belgium_severe['date'], y=df_belgium_severe['daily_deceased'], name='New Deaths'))

fig_bar_growth = go.Figure()
#fig_bar_growth.
fig_bar_growth.layout={'title': 'Growth Rate'}
fig_bar_growth.add_trace(go.Bar(x=df_growth_belgium_severe['date'], y=df_growth_belgium_severe['infected'], name='% growth infected', text=df_growth_belgium_severe['infected'], textposition='auto'))
fig_bar_growth.add_trace(go.Bar(x=df_growth_belgium_severe['date'], y=df_growth_belgium_severe['recoverd'], name='% growth recoverd', marker={'color':'green'}))

app.layout = html.Div(style={}, children=[
    html.H1(children='COVID19 Dashboard',
        style={
            'textAlign': 'center',
        }
    ),

    html.P(
        "ICU capacity as commuincated by the daily update by the FOD Volksgezondheid(https://youtu.be/-0ErsaJ52oY?t=2018)"
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
        id='fig-bar-growth',
        figure=fig_bar_growth
    ),

    dcc.Graph(
        id='table-severe-belgium',
            figure=table_severe
    ),
])

if __name__ == '__main__':
    app.run_server()