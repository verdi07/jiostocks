# App that displays stock information and some indicators


# Libraries
import dash # Web framework application
import dash_core_components as dcc # Graphs and interactive elements
import dash_html_components as html # Text and html elements
from dash.dependencies import Input, Output # Decorator components
import plotly.graph_objs as go # Graphs structure

import ta # Technical indicators
import yfinance as yf # Fix yahoo API
import datetime # Date and time

import pandas as pd # Dataframes
from pandas_datareader import data as web # Get data from web

# Fix yahoo finance API
yf.pdr_override()

# Define dates
start_date = datetime.date(2019, 1, 1)
end_date = datetime.datetime.now()


# Technical indicators

# Simple moving average
def stochastic(high, low, close, n = 14, nd = 3, fillna = True):
    return [ta.momentum.stoch(high, low, close, n, nd), ta.momentum.stoch_signal(high, low, close, n, nd)]

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
    # Searches for the requested ticker
    dcc.Input(      id = 'ticker-typer',
                    type = 'text',
                    value = 'AAPL'),

    html.Button(    'Search', id = 'button', type = 'submit'),

    # Gets the indicators wanted
    dcc.Dropdown(   id = 'indicators',
                    options = [ {'label' : 'Stochastic Oscillator', 'value' : '0'},
                                {'label' : 'Exponential Moving Average', 'value' : '1'},
                                {'label' : 'MACD', 'value' : '2'},
                                {'label' : 'Relative Strenth Index', 'value' : '3'}],
                    value = [],
                    multi = True),

    # Creates the title
    html.H1(id = 'title'),

    # Creates the stock graph
    dcc.Graph(id = 'stock-graph', relayoutData = {'autosize' : True}),

    # Creates the stochastic oscillator graph
    html.Div(id = 'stoch-toggle', children = [html.Div('Stochastic analysis'), dcc.Graph(id = 'stoch-graph')]),

    # Creates the macd graph
    html.Div(id = 'macd-toggle', children = [html.Div('MACD analysis'), dcc.Graph(id = 'macd-graph')]),

    # Creates the rsi graph
    html.Div(id = 'rsi-toggle', children = [html.Div('RSI analyisis'), dcc.Graph(id = 'rsi-graph')])
])


# The function is responsable for changing the elements in the graph depending on the dropdown input
@app.callback(
    [Output('title', 'children'),
    Output('stock-graph', 'figure'),
    Output('stoch-graph', 'figure'),
    Output('macd-graph', 'figure'),
    Output('rsi-graph', 'figure'),
    Output('stoch-toggle', 'style'),
    Output('macd-toggle', 'style'),
    Output('rsi-toggle', 'style')],
    [Input('button', 'n_clicks'),
    Input('ticker-typer', 'value'),
    Input('indicators', 'value'),
    Input('stock-graph', 'relayoutData')]
)
def update_figure(button, company, indicators, relayoutData):
    # Variables initializer

    # Get the requested ticker
    stock_df = web.DataReader(company.upper(), start_date, end_date, 'yahoo')

    # Define figure limits
    if 'autosize' in relayoutData or 'xaxis.autorange' in relayoutData:
        xlims = []
        ylims = []
    else:
        if 'xaxis.range[0]' in relayoutData:
            xlims = [relayoutData['xaxis.range[0]'], relayoutData['xaxis.range[1]']]
        else:
            xlims = []
        if 'yaxis.range[0]' in relayoutData:
            ylims = [relayoutData['yaxis.range[0]'], relayoutData['yaxis.range[1]']]
        else:
            ylims = []

    stochasticgraph = {}
    macdgraph = {}
    rsigraph = {}


    # Stock graph
    fig = {
            'data' : [  go.Candlestick( x = stock_df.index,
                                        open = stock_df['Open'],
                                        close = stock_df['Close'],
                                        high = stock_df['High'],
                                        low = stock_df['Low'],

                                        showlegend = False)],

            'layout' : {'xaxis' : {'rangeslider' : {'visible' : False}, 'range' : xlims},
                        'yaxis' : {'range' : ylims},
                        'legend': {'y' : 1.2, 'x' : 0}
        }}


    # Indicator graphs

    # Exponential moving average
    if '0' in indicators:
        stochastic_toggle = {'display' : 'block'}
        stochasticgraph = {'data' : [   go.Scatter( x = stock_df.index,
                                                    y = stochastic(stock_df['High'], stock_df['Low'], stock_df['Close'])[0],
                                                    showlegend = False),

                                        go.Scatter( x = stock_df.index,
                                                    y = stochastic(stock_df['High'], stock_df['Low'], stock_df['Close'])[1],
                                                    showlegend = False),

                                        go.Scatter( x = stock_df.index,
                                                    y = [20] * stock_df.index.size,
                                                    fill = 'tonexty',
                                                    line = dict(dash = 'dash', color = '#D6DBD8'),
                                                    showlegend = False),

                                        go.Scatter( x = stock_df.index,
                                                    y = [80] * stock_df.index.size,
                                                    line = dict(dash = 'dash', color = '#D6DBD8'),
                                                    showlegend = False)],

                            'layout' : {'xaxis' : {'range' : xlims}}
                            }
    else:
        stochastic_toggle = {'display' : 'none'}

    if '1' in indicators:
        fig['data'].append(go.Scatter(  x = stock_df.index,
                                        y = ema(stock_df['Close'], 9),
                                        name = 'Exponential moving average of {} days'.format('nine')))



    # MACD analysis
    if '2' in indicators:
        macd_toggle = {'display' : 'block'}
        macdgraph = {'data' : [ go.Scatter( x = stock_df.index,
                                            y = macd(stock_df['Close'])['macd'],
                                            showlegend = False),
                                go.Scatter( x = stock_df.index,
                                            y = macd(stock_df['Close'])['signal'],
                                            showlegend = False),
                                go.Bar( x = stock_df.index,
                                        y = macd(stock_df['Close'])['diff'],
                                        showlegend = False)],
                    'layout' : {'xaxis' : {'range' : xlims}}
                    }
    else:
        macd_toggle = {'display' : 'none'}


    # RSI analysis
    if '3' in indicators:
        rsi_toggle = {'display' : 'block'}
        rsigraph = {'data' : [  go.Scatter( x = stock_df.index,
                                            y = rsi(stock_df['Close']),
                                            line = dict(color = 'purple'),
                                            showlegend = False),

                                go.Scatter( x = stock_df.index,
                                            y = [70] * stock_df.index.size,
                                            line = dict(dash = 'dash', color = '#D6DBD8'),
                                            showlegend = False),

                                go.Scatter( x = stock_df.index,
                                            y = [30] * stock_df.index.size,
                                            fill = 'tonexty',
                                            line = dict(dash = 'dash', color = '#D6DBD8'),
                                            showlegend = False)],
                    'layout' : {'xaxis' : {'range' : xlims}}
                                }
    else:
        rsi_toggle = {'display' : 'none'}


    return('{} stock prices over the last year'.format(company.upper()), fig, stochasticgraph, macdgraph, rsigraph, stochastic_toggle, macd_toggle, rsi_toggle)



if __name__ == '__main__':
    app.run_server(debug=True)
