# -*- coding: utf-8 -*-
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
import technical_analysis.utils as utils
import data_process.data_process_utils as dp_utils

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

##App initialization stage

#Remove /n from pickled ticker names
def processTicker(tickerList):
    tickers = []
    for ticker in tickerList:
        tickerRenamed = ticker[:ticker.find('\n')]
        tickers.append({'label': tickerRenamed, 'value': tickerRenamed})
    return tickers
            
    #return list(map(lambda ticker: {'label': ticker, 'value': ticker}, tickerList))

tickerList = dp_utils.unserializeTickers()
tickers = processTicker(tickerList)

app.layout = html.Div(children=[
    html.H1(children='Technical Inspector'),
    html.Div([
        html.Div([
            html.H2(children='Stock selector'),
            dcc.Dropdown(
                id='ticker-dropdown',
                options = tickers,
                value = 'AAPL'
            ),
        ]),
        html.Div([
            html.H2(children='Technical Pattern'),
            dcc.Dropdown(
                id='tp-dropdown',
                options=[
                    {'label': 'Doji', 'value': 'DOJI'},
                    {'label': 'Engulfing Pattern', 'value': 'ENGULFING'},
                    {'label': 'Evening Star', 'value': 'EVENINGSTAR'}
                ],
                value='DOJI'
            )
        ]),
        html.Div([
            html.H2(children='Start Date'),
            dcc.Input(id='start-date-state', value='2017-01-01', type='text')
        ]),
        html.Div([
            html.H2(children='End Date'),
            dcc.Input(id='end-date-state', value='2017-12-30', type='text')
        ])
    ],style={}),

    html.Button(id='submit-button', n_clicks=0, children='Submit'),

    html.Div([
        html.H2(id='add-ticker-section', children='Add Ticker data'),
        dcc.Input(id='ticker-to-pull', type='text'),
        html.Button(id='ticker-to-pull-submit-button', n_clicks=0, children='Add')
    ]),
    

    dcc.Graph(
        id='tp-graph',
    )
])




@app.callback(Output('tp-graph', 'figure'),
                [Input('submit-button', 'n_clicks')],
                [State('ticker-dropdown', 'value'),
                 State('tp-dropdown', 'value'),
                 State('start-date-state', 'value'),
                 State('end-date-state', 'value')]
                )
def updateOutput(n_clicks, ticker, pattern, startDate, endDate):
    return utils.drawCandleChartWithTAPattern(ticker, startDate, endDate, pattern)

    
if __name__ == '__main__':
    app.run_server(debug=True)
