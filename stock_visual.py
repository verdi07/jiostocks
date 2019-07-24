# App that displays stock information and some indicators


# Libraries
import dash # Web framework application
import dash_core_components as dcc # Graphs and interactive elements
import dash_html_components as html # Text and html elements
from dash.dependencies import Input, Output # Decorator components

import ta # Technical indicators

import pandas as pd # Dataframes
import plotly.graph_objs as go # Graphs structure

# Define dataframes and create a list with them
df1 = pd.read_csv('stock_data/AMZN.csv')
df2 = pd.read_csv('stock_data/NKE.csv')
df3 = pd.read_csv('stock_data/AAPL.csv')
df4 = pd.read_csv('stock_data/TSLA.csv')

companies = [df1, df2, df3, df4]

# Technical indicators

# Simple moving average
def sma(df, n = 14, nd = 3):
    return ta.momentum.stoch_signal(df, n, nd)

# Exponential moving average
def ema(df, n = 12):
    return ta.trend.ema_indicator(df, n)

# MACD
def macd(df, nfast = 12, nslow = 26):
    mCd = {
            'macd' : ta.trend.macd(df, nfast, nslow),
            'signal' : ta.trend.macd_signal(df, nfast, nslow),
            'diff' : ta.trend.macd_diff(df, nfast, nslow)
            }
    return mCd

# RSI
def rsi(df, n = 14):
    return ta.momentum.rsi(df, n)



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

    # Gets the indicators wanted
    dcc.Dropdown(   id = 'indicators',
                    options = [ {'label' : 'Simple Moving Average', 'value' : '0'},
                                {'label' : 'Exponential Moving Average', 'value' : '1'},
                                {'label' : 'MACD', 'value' : '2'},
                                {'label' : 'Relative Strenth Index', 'value' : '3'}],
                    value = [],
                    multi = True),

    # Creates the title
    html.H1(id = 'title'),

    # Creates the graph
    dcc.Graph(id = 'my-graph'),

    # MACD graph
    dcc.Graph(id = 'macd')
])


# The function is responsable for changing the elements in the graph depending on the dropdown input
@app.callback(
    [Output('my-graph', 'figure'),
    Output('title', 'children'),
    Output('macd', 'figure')],
    [Input('ticker-selector', 'value'),
    Input('indicators', 'value')]
)
def update_figure(input_value, indicators):
    if input_value == '0':
        comp = 'Amazon'
    elif input_value == '1':
        comp = 'Nike'
    elif input_value == '2':
        comp = 'Apple'
    else:
        comp = 'Tesla'

    fig = {
            'data' : [  go.Candlestick( x = companies[int(input_value)]['Date'], 
                                        open = companies[int(input_value)]['Open'],
                                        close = companies[int(input_value)]['Close'],
                                        high = companies[int(input_value)]['High'],
                                        low = companies[int(input_value)]['Low'])],

            'layout' : {'xaxis' : {'rangeslider' : {'visible' : False}}}
        }
    macdgraph = {}
    if '1' in indicators:
        fig['data'].append(go.Scatter(x = companies[int(input_value)]['Date'],
                        y = ema(companies[int(input_value)]['Close'], 9)))        

    if '2' in indicators:
            macdgraph = {'data' : [ go.Scatter( x = companies[int(input_value)]['Date'],
                                                y = macd(companies[int(input_value)]['Close'])['macd']),
                                    go.Scatter( x = companies[int(input_value)]['Date'],
                                                y = macd(companies[int(input_value)]['Close'])['signal']),
                                    go.Bar( x = companies[int(input_value)]['Date'],
                                            y = macd(companies[int(input_value)]['Close'])['diff'])]}

    return(fig, '{} stock prices over the last year'.format(comp), macdgraph)



if __name__ == '__main__':
    app.run_server(debug=True)


