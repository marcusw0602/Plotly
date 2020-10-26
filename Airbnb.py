import dash
import dash_table
import dash_core_components as dcc
import dash_html_components as html
import plotly
import plotly.express as px
from dash.dependencies import Input, Output, ALL, State, MATCH, ALLSMALLER
import pandas as pd
import numpy as np

df = pd.read_csv('D:\Finalrecycling.csv')
df.head(1)

app = dash.Dash(__name__)
app.layout = html.Div([
    html.Div([
        # Classification list
        html.Ul([
                html.Li("Compost", className='circle', style={'background': '#ff00ff','color':'black',
                    'list-style':'none','text-indent': '17px'}),
                html.Li("Electronics", className='circle', style={'background': '#0000ff','color':'black',
                    'list-style':'none','text-indent': '17px','white-space':'nowrap'}),
                html.Li("Hazardous_waste", className='circle', style={'background': '#FF0000','color':'black',
                    'list-style':'none','text-indent': '17px'}),
                html.Li("Plastic_bags", className='circle', style={'background': '#00ff00','color':'black',
                    'list-style':'none','text-indent': '17px'}),
                html.Li("Recycling_bins", className='circle',  style={'background': '#824100','color':'black',
                    'list-style':'none','text-indent': '17px'}),
            ], style={'border-bottom': 'solid 3px', 'border-color':'#00FC87','padding-top': '6px'}
            ),
        # Borough_checklist
        html.Label(children=['Borough: ']),
        dcc.Checklist(
            id='boro_name',
            options=[{'label':str(i),'value':i} for i in sorted(df['boro'].unique())],
            value=[i for i in sorted(df['boro'].unique())],
        ),
        html.Label(children=['Looking to recycle: ']),
        # Recycling Checklist
        dcc.Checklist(
            id='recycling_types',
            options=[{'label':str(i),'value':i} for i in sorted(df['type'].unique())],
            value=[i for i in sorted(df['type'].unique())],
        ),
        # Web link information
        html.Br(),
        html.Label(['Website:']),
        html.Pre(id='web_link',children=[]),
    ]),
    html.Div([
        dcc.Graph(
            id='graph', config={'displayModeBar':False, 'scrollZoom':True}
        )
    ])
])

@app.callback(Output('graph','figure'),)
