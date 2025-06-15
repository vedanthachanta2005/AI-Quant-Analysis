import yfinance as yf
import pandas as pd
from datetime import date
#y finance only allows 60 days of data when trying to get low interval data
data = yf.download("EURUSD=X", start="2025-5-1", end=date.today(), interval='15m')
data.iloc[-1:,:]
data.Open.iloc