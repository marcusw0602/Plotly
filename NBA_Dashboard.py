import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly
import plotly.express as px
from dash.dependencies import Input, Output, ALL, State, MATCH, ALLSMALLER
import pandas as pd
import numpy as np

df = pd.read_csv('D:\players_stats_by_season_full_details.csv')

df.head(2)
#players=['Kevin Durant','LeBron James']
#df = df[df.Player.isin(players)]
df.loc[df['Player']=='LeBron James']
Players=list(df.Player.unique())
df.head(10)
#df = df.drop(['Unnamed: 0', 'Unnamed: 0.1'], axis=1)
options=df.columns
options
app = dash.Dash()
app.title='NBA'
app.layout=html.Div([
    html.Div([
        html.Label('xaxis'),
        html.Div([
            dcc.Dropdown(
                id='dropdown1',
                options=[{'label':i,'value':i} for i in options],
                value='Player'
            )
        ]),
        html.Label('yaxis'),
        html.Div([
            dcc.Dropdown(
                id='dropdown2',
                options=[{'label':i,'value':i} for i in options],
                value='PTS'
            )
        ]),
        dcc.Dropdown(
            id='Players',
            options=[{'label':i,'value':i} for i in Players],
            multi=True,
            value=['Kevin Durant','LeBron James']
        ),
        dcc.Graph(id='BarGraph')
    ])
])
@app.callback(Output(component_id='BarGraph',component_property='figure'),
    [Input(component_id='dropdown1',component_property='value'),
    Input(component_id='dropdown2',component_property='value'),
    Input(component_id='Players',component_property='value')])

def update_graph_Bar(dropdown1,dropdown2,Players):
    dff = df[df.Player.isin(Players)]
    BarChart=px.histogram(
        data_frame=dff,
        x=dropdown1,
        y=dropdown2,
        color='Season',
        histfunc='sum',
        barmode='group'
    )
    return(BarChart)


if __name__=='__main__':
    app.run_server()
