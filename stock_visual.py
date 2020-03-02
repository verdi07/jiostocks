# App that displays stock information and some indicators
# Test

# Libraries
import dash # Web framework application
import dash_core_components as dcc # Graphs and interactive elements
import dash_html_components as html # Text and html elements
from dash.dependencies import Input, Output, State # Decorator components
import plotly.graph_objs as go # Graphs structure
import dash_bootstrap_components as dbc # Themes

import ta # Technical indicators
import yfinance as yf # Fix yahoo API
import datetime # Date and time
import webbrowser # Open browser and navigate

import pandas as pd # Dataframes
from pandas_datareader import data as web # Get data from web

# Fix yahoo finance API
yf.pdr_override()


# Technical indicators

# MACD
def macd(df, nfast = 12, nslow = 26):
    mCd = {
            'macd' : ta.trend.macd(df, nfast, nslow),
            'signal' : ta.trend.macd_signal(df, nfast, nslow),
            'diff' : ta.trend.macd_diff(df, nfast, nslow)
            }
    return mCd

# Awesome Oscillator
def ao(high, low, s = 5, len = 34):
    return ta.momentum.ao(high, low, s, len, fillna = True)

# Moneyflow index
def mfi(high, low, close, volume, n = 14):
    return ta.momentum.money_flow_index(high, low, close, volume, n, fillna = True)

# True strenght index
def tsi(close, r = 25, s = 13):
    return ta.momentum.tsi(close, r, s, fillna = structure)

# Ultimate Oscillator
def uo(high, low, close, s = 7, m = 14, len = 28):
    return ta.momentum.uo(high, low, close, s, m, len, fillna = True)



# Initialize the web app and define its layout
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.DARKLY])

app.layout = html.Div([
    # Searches for the requested ticker
    dcc.Input(      id = 'ticker-typer',
                    type = 'text',
                    value = 'AAPL'),

    dbc.Button(    'Search', id = 'button'),

    dcc.DatePickerRange(id = 'date',
                        start_date = datetime.date(2018, 1, 1),
                        end_date = datetime.date.today(),
                        number_of_months_shown = 2),

    # Gets the indicators wanted
    dcc.Dropdown(   id = 'indicators',
                    options = [ {'label' : 'Awesome Oscillator', 'value' : '0'},
                                {'label' : 'Bollinger Bands', 'value' : '1'},
                                {'label' : 'Exponential Moving Average', 'value' : '2'},
                                {'label' : 'MACD', 'value' : '3'},
                                {'label' : 'Moneyflow Index', 'value' : '4'},
                                {'label' : 'Relative Strenth Index', 'value' : '5'},
                                {'label' : 'Stochastic Oscillator', 'value' : '6'},
                                {'label' : 'True Strength Index', 'value' : '7'},
                                {'label' : 'Ultimate Oscillator', 'value' : '8'}],
                    value = [],
                    multi = True,
                    style={'backgroundColor': 'black', 'color': 'black'}
                    ),

    # Creates the title
    html.H1(id = 'title'),

    # Creates the stock graph
    dcc.Graph(id = 'stock-graph', relayoutData = {'autosize' : True}),

    # Creates the Awesome Oscillator graph
    html.Div(   id = 'ao-toggle',
                children = [
                    html.Div('Awesome Oscillator'),
                    dcc.Graph(id = 'ao-graph')]),

    # Creates the MACD graph
    html.Div(   id = 'macd-toggle',
                children = [html.Div('MACD analysis'),
                dcc.Graph(id = 'macd-graph')]),

    # Creates the Moneyflow index
    html.Div(   id = 'mf-toggle',
                children = [html.Div('Money flow Index'),
                dcc.Graph(id = 'mf-graph')]),

    # Creates the RSI graph
    html.Div(   id = 'rsi-toggle',
                children = [html.Div('Relative Strength Index analyisis'),
                dcc.Graph(id = 'rsi-graph')]),

    # Creates the Stochastic Oscillator graph
    html.Div(   id = 'stoch-toggle',
                children = [html.Div('Stochastic analysis'),
                dcc.Graph(id = 'stoch-graph')]),

    # Creates the TSI graph
    html.Div(   id = 'tsi-toggle',
                children = [html.Div('True Strength Index analysis'),
                dcc.Graph(id = 'tsi-graph')])
])


# The function is responsable for changing the elements in the graph depending on the dropdown input
@app.callback(
    [Output('title', 'children'),
    Output('stock-graph', 'figure'),
    Output('ao-graph', 'figure'),
    Output('macd-graph', 'figure'),
    Output('mf-graph', 'figure'),
    Output('rsi-graph', 'figure'),
    Output('stoch-graph', 'figure'),
    Output('tsi-graph', 'figure'),
    Output('ao-toggle', 'style'),
    Output('macd-toggle', 'style'),
    Output('mf-toggle', 'style'),
    Output('rsi-toggle', 'style'),
    Output('stoch-toggle', 'style'),
    Output('tsi-toggle', 'style')],
    [Input('button', 'n_clicks'),
    Input('indicators', 'value'),
    Input('date', 'start_date'),
    Input('date', 'end_date'),
    Input('stock-graph', 'relayoutData')],
    [State('ticker-typer', 'value')]
)
def update_figure(button, indicators, start_date, end_date, relayoutData, company):
    # Variables initializer

    awesomegraph = {}
    macdgraph = {}
    moneyflowgraph = {}
    rsigraph = {}
    stochasticgraph = {}
    tsigraph = {}


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


    # Stock graph
    fig = {
            'data' : [  go.Candlestick( x = stock_df.index,
                                        open = stock_df['Open'],
                                        close = stock_df.Close,
                                        high = stock_df.High,
                                        low = stock_df.Low,

                                        showlegend = False)],

            'layout' : {'xaxis' : {'rangeslider' : {'visible' : False}, 'range' : xlims},
                        'yaxis' : {'range' : ylims},
                        'legend': {'y' : 1.2, 'x' : 0}
        }}


    # Indicator graphs

    # Awesome Oscillator
    if '0' in indicators:
        stock_df['Awesome'] = ta.momentum.ao(stock_df.High, stock_df.Low, fillna = True)
        awesome_toggle = {'display' : 'block'}
        awesomegraph = {'data' : [  go.Bar( x = stock_df.index,
                                            y = stock_df['Awesome'],
                                            showlegend = False)],
                        'layout' : {'xaxis' : {'range' : xlims}}}
    else:
        awesome_toggle = {'display' : 'none'}

    # Bollinger Bands
    if '1' in indicators:
        fig['data'].append(go.Scatter(  x = stock_df.index,
                                        y = ta.volatility.bollinger_hband(stock_df.Close),
                                        name = 'Bollinger High band'))

        fig['data'].append(go.Scatter(  x = stock_df.index,
                                        y = ta.volatility.bollinger_lband(stock_df.Close),
                                        name = 'Bollinger Low Band'))

    # Exponential moving average
    if '2' in indicators:
        fig['data'].append(go.Scatter(  x = stock_df.index,
                                        y = ta.trend.ema(stock_df.Close, 9),
                                        name = 'Exponential moving average of {} days'.format('nine')))


    # MACD analysis
    if '3' in indicators:
        macd_toggle = {'display' : 'block'}
        macdgraph = {'data' : [ go.Scatter( x = stock_df.index,
                                            y = macd(stock_df.Close)['macd'],
                                            showlegend = False),
                                go.Scatter( x = stock_df.index,
                                            y = macd(stock_df.Close)['signal'],
                                            showlegend = False),
                                go.Bar( x = stock_df.index,
                                        y = macd(stock_df.Close)['diff'],
                                        showlegend = False)],
                    'layout' : {'xaxis' : {'range' : xlims}}
                    }
    else:
        macd_toggle = {'display' : 'none'}

    # Money flow Index
    if '4' in indicators:
        mfi_toggle = {'display' : 'block'}
        moneyflowgraph = {'data' : [    go.Scatter( x = stock_df.index,
                                                    y = ta.momentum.money_flow_index(
                                                        stock_df.High,
                                                        stock_df.Low,
                                                        stock_df.Close,
                                                        stock_df.Volume,
                                                        fillna = True),
                                                    showlegend = False),

                                        go.Scatter( x = stock_df.index,
                                                    y = [80] * stock_df.index.size,
                                                    line = dict(dash = 'dash', color = '#D6DBD8'),
                                                    showlegend = False),

                                        go.Scatter( x = stock_df.index,
                                                    y = [20] * stock_df.index.size,
                                                    fill = 'tonexty',
                                                    line = dict(dash = 'dash', color = '#D6DBD8'),
                                                    showlegend = False)]}
    else:
        mfi_toggle = {'display' : 'none'}


    # RSI analysis
    if '5' in indicators:
        rsi_toggle = {'display' : 'block'}
        rsigraph = {'data' : [  go.Scatter( x = stock_df.index,
                                            y = ta.momentum.rsi(stock_df.Close),
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

    # Stochastic Oscillator
    if '6' in indicators:
        stochastic_toggle = {'display' : 'block'}
        stochasticgraph = {'data' : [   go.Scatter( x = stock_df.index,
                                                    y = ta.momentum.stoch(stock_df.High, stock_df.Low, stock_df.Close, fillna = True),
                                                    showlegend = False),

                                        go.Scatter( x = stock_df.index,
                                                    y = ta.momentum.stoch_signal(stock_df.High, stock_df.Low, stock_df.Close),
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

    # True Strenght Index
    if '7' in indicators:
        tsi_toggle = {'display' : 'block'}
        tsigraph = {'data' : [  go.Scatter( x = stock_df.index,
                                            y = ta.momentum.tsi(stock_df.Close, fillna = True),
                                            showlegend = False)]}
    else:
        tsi_toggle = {'display' : 'none'}


    return('{} stock prices over the last year'.format(company.upper()), fig,
                            awesomegraph, macdgraph, moneyflowgraph, rsigraph, stochasticgraph, tsigraph,
                            awesome_toggle, macd_toggle, mfi_toggle, rsi_toggle, stochastic_toggle, tsi_toggle)



if __name__ == '__main__':
    webbrowser.open('http://127.0.0.1:8050/', new = 1)
    app.run_server(debug=True)
