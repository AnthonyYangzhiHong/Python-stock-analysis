import pickle

def unserializeTickers():
    with open("sp500tickers.pickle", "rb") as f:
            tickers = pickle.load(f)
    return tickers
