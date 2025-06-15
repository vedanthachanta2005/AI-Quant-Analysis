from statsmodels.regression.rolling import RollingOLS
import pandas_datareader.data as web
import matplotlib.pyplot as plt
import statsmodels.api as sm
import pandas as pd
import numpy as np
import datetime as dt
import yfinance as yf
#import pandas_ta as ta
import warnings
warnings.filterwarnings('ignore')
snp500 = pd.read_html('https://en.wikipedia.org/wiki/List_of_S%26P_500_companies')[0]
snp500['Symbol'] = snp500['Symbol'].str.replace('.', '-')
symbols_list = snp500['Symbol'].unique().tolist()

end_date = '2025-03-10'
start_date = pd.to_datetime(end_date)-pd.DateOffset(50)
df = yf.download(tickers=symbols_list,
                start=start_date, 
                end=end_date)
df.stack()
print("Finished")
