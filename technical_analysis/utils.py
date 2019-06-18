import os
import pandas as pd
import plotly
from plotly.tools import FigureFactory as FF
import plotly.graph_objs as go
import talib

## Return a python dataframe containing ohlc of given stock and date range
## First check if data exits at local, if not then pull it down from internet

def getPriceData(ticker , start_date, end_date):
    df = pd.read_csv('stock_dfs/{}.csv'.format(ticker), index_col=0).loc[start_date : end_date]
    ##convert date to datetime format
    ##df.index = pd.to_datetime(df.index)
    return df



## Draws an interactive candle stick chart of given dataframe

def drawOHLCChart(df, ticker, start_date, end_date):
    trace = go.Candlestick(x=df['Date'],
                open=df['AAPL.Open'],
                high=df['AAPL.High'],
                low=df['AAPL.Low'],
                close=df['AAPL.Close'])
    data = [trace]

    fig = FF.create_ohlc(df.Open, df.High, df.Low, df.Close, dates=df.index)
    plotly.offline.plot(fig, filename='OHLC/{}-ohlc-{}-{}.html'.format(ticker, start_date, end_date))


##Find Technical Pattern on given stock data
def findTAPattern(df, patternName):
    if patternName == '2CROWS':
        df[patternName] = talib.CDL2CROWS(df.Open.values, df.High.values, df.Low.values, df.Close.values)
    elif patternName == 'DOJI':
        df[patternName] = talib.CDLDOJI(df.Open.values, df.High.values, df.Low.values, df.Close.values)
    elif patternName == 'ENGULFING':
        df[patternName] = talib.CDLENGULFING(df.Open.values, df.High.values, df.Low.values, df.Close.values)
    elif patternName == 'EVENINGSTAR':
        df[patternName] = talib.CDLEVENINGSTAR(df.Open.values, df.High.values, df.Low.values, df.Close.values)
    elif patternName == 'MARUBOZU':
        df[patternName] = talib.CDLMARUBOZU(df.Open.values, df.High.values, df.Low.values, df.Close.values)
    else:
        print('Pattern not supported yet')

    patterned_df = df[df[patternName] != 0]
    return patterned_df
    #print(patterned_df)


##Return array of line positions
def generateLineCoord(df):
    date_list = df.index
    coordinate_list = []
    for date in date_list:
        coord = {
            'type': 'line',
            'x0': date,
            'y0': 0,
            'x1': date,
            'y1': 200,
            'line': {
                'color': 'rgb(55, 128, 191)',
                'width': 1,
            },
        }
        coordinate_list.append(coord)
    
    return coordinate_list


#Draw candle chart with pattern indicator
def drawCandleChartWithTAPattern(ticker, start_date, end_date, pattern):
    df = getPriceData(ticker , start_date, end_date)
    pattern_df = findTAPattern(df, pattern)
    coord = generateLineCoord(pattern_df)

    ##Plotly candle stick chart does not take indexed date
    df_noIndex = df.reset_index()
    trace = go.Candlestick(x=df_noIndex['Date'], open=df_noIndex['Open'], high=df_noIndex['High'], low=df_noIndex['Low'], close=df_noIndex['Close'])
    data = [trace]
    layout = {
        'xaxis': {
            'rangeslider': {
                'visible': False
            }
        },
        'shapes': coord
    }
    return go.Figure(data=data, layout=layout)
    #plotly.offline.plot(fig, filename='OHLC/{}-candle-{}-{}-{}.html'.format(ticker, start_date, end_date,pattern))



## Delete the "\n" of stock data names in stock_dfs folder
def batchProcessFilename():
    for filename in os.listdir():
        ##if filename contains "\n"
        if  filename.find('\n') > 0:
            os.rename(filename, filename[:filename.find('\n')])



def generateOHLC(ticker, start_date, end_date):
    df = getPriceData(ticker, start_date, end_date)
    drawOHLCChart(df, ticker, start_date, end_date)


#drawCandleChartWithTAPattern('AAPL', '2012-01-01', '2015-12-30', 'MARUBOZU')


def testImport():
    print('Function invoked!')