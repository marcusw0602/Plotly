# Running the necessary packages to make the code work.
import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly
import plotly.express as px
from dash.dependencies import Input, Output, ALL, State, MATCH, ALLSMALLER
import pandas as pd
import numpy as np

# Reading in a practice dataframe for plotly graphs.
df = pd.read_csv("D:\GapminderFiveYearData.csv")
# Created an options list for dropdowm menue.
options=df[['pop','lifeExp','gdpPercap']]
# Saving only the continent names for each row and saving it in a list for later.
CountryNames=list(df.country.unique())
Yearlist=list(df.year.unique())
# Establishing the dash application
app=dash.Dash()
# Establishing the title for the web page of the Dash application.
app.title='World GDP dashboard'
# The body of the entire application below
app.layout=html.Div([
    # First Div containing the dropdown menues for the scatterplot at the top of the page.
    html.Div([
        # First dropdown menue contains a title.
        # The dropdowm only contains the only two columns to display the relationship of life and money per-person.
        html.Label(['X-axis']),
        dcc.Dropdown(
            id='xaxis_dropdown',
            options=[{'label':'GDP Per Capita','value':'gdpPercap'},{'label':'Life Expenctancy','value':'lifeExp'}],
            value='gdpPercap'
        ),
        html.Label(['Y-axis']),
        dcc.Dropdown(
            id='yaxis_dropdown',
            options=[{'label':'GDP Per Capita','value':'gdpPercap'},{'label':'Life Expenctancy','value':'lifeExp'}],
            value='lifeExp'
            ),
        dcc.Graph(id='Scatter_graph'),
        # Added a year slider to show the data year by year progression.
        dcc.Slider(
        id='year-slider',
        min=df['year'].min(),
        max=df['year'].max(),
        value=df['year'].min(),
        marks={str(year): str(year) for year in df['year'].unique()},
        step=None
    ),
    ]),
    html.Div([
        html.Label(['Y-axis']),
        dcc.Dropdown(
        id='yaxis_dropdown1',
        options=[{'label': i.title(), 'value': i} for i in options],
        value='pop'
        ),
        dcc.Dropdown(
            id='ContinentName',
            options=[{'label':i,'value':i} for i in CountryNames],
            multi=True,
            value=['China','Brazil']
        ),
        dcc.Graph(id='Bar_Graph')
    ])
])

@app.callback(
    Output(component_id='Bar_Graph',component_property='figure'),
    [Input(component_id='yaxis_dropdown1',component_property='value'),
    Input(component_id='ContinentName',component_property='value')])
def update_graph_Bar(yaxis_dropdown1,ContinentName):
    #dff = df[df.year == selected_year]
    dff = df[df.country.isin(ContinentName)]
    BarChart=px.bar(
        data_frame=dff,
        x='year',
        y=yaxis_dropdown1,
        text='pop',
        # animation_group='country',
        # animation_frame='year',
        color='country',
        barmode='group',
        # facet_row='continent',
        labels={
            'pop': 'Population',
            'gdpPercap': 'GDP per Capita',
            'year': 'Year',
            'lifeExp': 'Life Expectancy',
            'continent': 'Continent'
        }
    )
    BarChart.update_traces(
        texttemplate='%{text:.2s}',
        textposition='auto'
    )
    BarChart.update_layout(
        xaxis={'categoryorder':'total ascending'},
        uniformtext_minsize=8,
        uniformtext_mode='hide'
    )
    return(BarChart)

@app.callback(
    Output(component_id='Scatter_graph',component_property='figure'),
    [Input(component_id='xaxis_dropdown',component_property='value'),
    Input(component_id='yaxis_dropdown',component_property='value'),
    Input('year-slider', 'value')])
def update_graph_Scatter(xaxis_dropdown,yaxis_dropdown,selected_year):
    dff = df[df.year == selected_year]
    Scatterchart=px.scatter(
        data_frame=dff,
        x=xaxis_dropdown,
        y=yaxis_dropdown,
        title=xaxis_dropdown+': by '+yaxis_dropdown,
        color='continent',
        size='pop',
        # animation_group='country',
        # animation_frame='year',
        hover_name='country',
        labels={
            'pop': 'Population',
            'gdpPercap': 'GDP per Capita',
            'year': 'Year',
            'lifeExp': 'Life Expectancy',
            'continent': 'Continent'
        },
        size_max=100,
        facet_col='continent'
    )
    Scatterchart.update_layout(transition_duration=500,height=700)
    return(Scatterchart)


if __name__=='__main__':
    app.run_server(debug=True)
