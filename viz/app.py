import flask
import dash
import dash_table
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go
import plotly.figure_factory as ff
from plotly.subplots import make_subplots
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
df_belgium_severe = df_cases_belgium[['date', 'tested', 'daily_infected', 'percentage_infected', 'daily_deceased', 'deceased', 'icu', 'capacity_icu', 'hospitalized']][13:]
df_growth_belgium_severe = df_growth_belgium[['date', 'daily_infected', 'infected', 'daily_deceased', 'deceased', 'icu', 'capacity_icu', 'hospitalized', 'released']][13:]

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

# Lockdown
fig_severe.add_shape(
    dict(
        type="line",
        x0="3/18/2020",
        x1="3/18/2020",
        y0=0,
        y1=6000,
        line=dict(
            color="RoyalBlue",
            dash="dashdot",
        )
    )
)
fig_severe.add_trace(go.Scatter(x=["3/19/2020"], y=[3500], text=["Lockdown"], mode="text", name="Lockdown"))

# Lockdown light
fig_severe.add_shape(
    dict(
        type="line",
        x0="3/14/2020",
        x1="3/14/2020",
        y0=0,
        y1=6000,
        line=dict(
            color="RoyalBlue",
            dash="dashdot",
        )
    )
)
fig_severe.add_trace(go.Scatter(x=["3/15/2020"], y=[3500], text=["Lockdown Light"], mode="text", name="Lockdown Light"))

#### Tested vs Tested Positive ####
fig_bar_infected_daily = make_subplots(specs=[[{"secondary_y": True}]])
fig_bar_infected_daily.layout={'title': 'Daily tests performed and new infections'}
fig_bar_infected_daily.add_trace(go.Bar(x=df_belgium_severe['date'], y=df_belgium_severe['tested'], name='Tests Performed', yaxis="y1"))
fig_bar_infected_daily.add_trace(go.Bar(x=df_belgium_severe['date'], y=df_belgium_severe['daily_infected'], name='New Infections', yaxis="y1"))
fig_bar_infected_daily.add_trace(go.Scatter(x=df_belgium_severe['date'], y=df_belgium_severe['percentage_infected'], name='% Infected', yaxis="y2"))
fig_bar_infected_daily.update_layout(
    xaxis=dict(
        domain=[0, 1]
    ),
    yaxis=dict(
        title="tested (positive)",
        titlefont=dict(
            color="#1f77b4"
        ),
        tickfont=dict(
            color="#1f77b4"
        )
    ),
    yaxis2=dict(
        title="percentage infected",
        titlefont=dict(
            color="#ff7f0e"
        ),
        tickfont=dict(
            color="#ff7f0e"
        ),
        anchor="free",
        overlaying="y",
        side="right",
        position=1
    ))

fig_bar_growth = go.Figure()
fig_bar_growth.layout={'title': 'Growth Rate infected and released'}
fig_bar_growth.add_trace(go.Bar(x=df_growth_belgium_severe['date'], y=df_growth_belgium_severe['infected'], name='% growth infected', text=df_growth_belgium_severe['infected'], textposition='auto'))
fig_bar_growth.add_trace(go.Bar(x=df_growth_belgium_severe['date'], y=df_growth_belgium_severe['released'], name='% growth released', marker={'color':'green'}))

fig_bar_growth_severe = go.Figure()
fig_bar_growth_severe.layout={'title': 'Growth Rate hospitalizations, intensive care and deceased'}
fig_bar_growth_severe.add_trace(go.Bar(x=df_growth_belgium_severe['date'], y=df_growth_belgium_severe['hospitalized'], name='% growth hospitalizations'))
fig_bar_growth_severe.add_trace(go.Bar(x=df_growth_belgium_severe['date'], y=df_growth_belgium_severe['icu'], name='% growth ICU', marker={'color':'tomato'}))
#fig_bar_growth_severe.add_trace(go.Scatter(x=df_growth_belgium_severe['date'], y=df_growth_belgium_severe['deceased'], name='% growth deceased', marker={'color':'black'}))

labels = ['Flanders', 'Wallonia', 'Brussels', 'unkown']
values = df_cases_belgium.loc[:,['infected_flanders', 'infected_brussels', 'infected_wallonia', 'infected_unknown']].iloc[-1].astype(int).values
fig_pie_regions = go.Figure(data=[go.Pie(labels=labels,values=sorted(values, reverse=True), hole=.4, sort=False, direction="clockwise")])
fig_pie_regions.layout={'title': 'Infections in different regions'}



# Get the data for deceased in the different regions and location of death
df_deceased_belgium = pd.read_csv("https://raw.githubusercontent.com/sdiepend/stayinyourkot/master/data/COVID19_Belgium_deceased.csv")
# select data for flanders
flanders_deceased=df_deceased_belgium.loc[:,['total_deceased_flanders_hospital', 'total_deceased_flanders_elderlyhome', 'total_deceased_flanders_home', 'total_deceased_flanders_elsewhere', 'total_deceased_flanders_unknown']].iloc[-1].astype(int).sort_values(ascending=False)
# map the right labels
labels_mapping = {'hospital': 'Ziekenhuis', 'elderlyhome': 'WZC', '_home': 'Thuis', 'elsewhere': 'Elders', 'unknown': 'Onbekend'}
flanders_labels = []
for index_name in flanders_deceased.index:
    for key, val in labels_mapping.items():
        if key in index_name:
            flanders_labels.append(val)
# Plot in a pie chart
fig_pie_flanders_places = go.Figure(data=[go.Pie(labels=flanders_labels,values=flanders_deceased.values, hole=.4, sort=False, direction="clockwise")])
fig_pie_flanders_places.layout={'title': 'Deceased Flanders'}
wallonia_deceased=df_deceased_belgium.loc[:,['total_deceased_wallonia_hospital', 'total_deceased_wallonia_elderlyhome', 
                                             'total_deceased_wallonia_home', 'total_deceased_wallonia_elsewhere', 
                                             'total_deceased_wallonia_unknown']].iloc[-1].astype(int).sort_values(ascending=False)

wallonia_labels = []
for index_name in wallonia_deceased.index:
    for key, val in labels_mapping.items():
        if key in index_name:
            wallonia_labels.append(val)

fig_pie_wallonia_places = go.Figure(data=[go.Pie(labels=wallonia_labels,values=wallonia_deceased.values, hole=.4, sort=False, direction="clockwise")])
fig_pie_wallonia_places.layout={'title': 'Deceased Wallonia'}

app.index_string = '''
<!DOCTYPE html>
<html>
    <head>
        <!-- Global site tag (gtag.js) - Google Analytics -->
        <script async src="https://www.googletagmanager.com/gtag/js?id=UA-55273305-4"></script>
        <script>
            window.dataLayer = window.dataLayer || [];
            function gtag(){dataLayer.push(arguments);}
            gtag('js', new Date());

            gtag('config', 'UA-55273305-4');
        </script>

        {%metas%}
        <title>Corona Situation</title>
        {%favicon%}
        {%css%}
    </head>
    <body>
        <div></div>
        {%app_entry%}
        <footer>
            {%config%}
            {%scripts%}
            {%renderer%}
        </footer>
        <div></div>
    </body>
</html>
'''

app.layout = html.Div(style={}, children=[
    html.H1(children='COVID19 Dashboard',
        style={
            'textAlign': 'center',
        }
    ),

    html.P(
        "ICU capacity as communicated by the daily update by the FOD Volksgezondheid(https://youtu.be/-0ErsaJ52oY?t=2018)"
    ),

    dcc.Graph(
        id='fig-severe-belgium',
        figure=fig_severe
    ),

    html.Div([
        dcc.Graph(
            figure=fig_bar_infected_daily
        )
    ], className="row"),

    # html.Div([
    #     html.Div([
    #         dcc.Graph(
    #             id='fig-infected-daily',
    #             figure=fig_bar_infected_daily
    #         )
    #     ], className="eight columns"),

    #     html.Div([
    #         dcc.Graph(
    #             figure=fig_pie_regions
    #         )
    #     ], className="four columns")
    # ], className="row"),


    dcc.Graph(
        id='fig-bar-growth',    
        figure=fig_bar_growth
    ),

    dcc.Graph(
        id='fig-bar-growth-severe',
        figure=fig_bar_growth_severe
    ),

    dcc.Graph(
        id='table-severe-belgium',
        figure=table_severe
    ),
])

if __name__ == '__main__':
    app.run_server()