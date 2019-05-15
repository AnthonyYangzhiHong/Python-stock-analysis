import fix_yahoo_finance as yf

data = yf.download("BRK.B", start="2017-01-01", end="2017-04-30")
print(data.head())