# App that displays stock information and some indicators


# Libraries
import dash # Web framework application
import dash_core_components as dcc # Graphs and interactive elements
import dash_html_components as html # Text and html elements
from dash.dependencies import Input, Output # Decorator components

import pandas as pd # Dataframes
import plotly.graph_objs as go # Graphs structure

# Define dataframes and create a list with them
df1 = pd.read_csv('AMZN.csv')
df2 = pd.read_csv('NKE.csv')
df3 = pd.read_csv('AAPL.csv')
df4 = pd.read_csv('TSLA.csv')

companies = [df1, df2, df3, df4]

# Get stylish elements
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']


# Initialize the web app and define its layout
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

app.layout = html.Div([
    # Creates the dropdown element
    dcc.Dropdown(   id = 'ticker-selector', 
                    options = [ {'label' : 'Amazon', 'value' : '0'}, 
                                {'label' : 'Nike', 'value' : '1'}, 
                                {'label' : 'Apple', 'value' : '2'}, 
                                {'label' : 'Tesla', 'value' : '3'}],
                    value = '0'),

    # Creates the title
    html.H1(id = 'title'),

    # Creates the graph
    dcc.Graph(id = 'my-graph')
])


# The function is responsable for changing the elements in the graph depending on the dropdown input
@app.callback(
    [Output('my-graph', 'figure'),
    Output('title', 'children')],
    [Input('ticker-selector', 'value')]
)
def update_figure(input_value):
    if input_value == '0':
        comp = 'Amazon'
    elif input_value == '1':
        comp = 'Nike'
    elif input_value == '2':
        comp = 'Apple'
    else:
        comp = 'Tesla'

    return {'data' : [go.Candlestick(   x = companies[int(input_value)]['Date'], 
                                        open = companies[int(input_value)]['Open'],
                                        close = companies[int(input_value)]['Close'],
                                        high = companies[int(input_value)]['High'],
                                        low = companies[int(input_value)]['Low'])],
            'layout' : {
                    'xaxis' : {'rangeslider' : {'visible' : False}}}
            }, '{} stock prices over the last year'.format(comp)

if __name__ == '__main__':
    app.run_server(debug=True)
