import yfinance as yf
import pandas as pd
from datetime import date
from apscheduler.schedulers.blocking import BlockingScheduler
from oandapyV20 import API
import oandapyV20.endpoints.orders as orders
from oandapyV20.contrib.requests import MarketOrderRequest
from oanda_candles import Pair, Gran, CandleCollector, CandleClient
from oandapyV20.contrib.requests import TakeProfitDetails, StopLossDetails
from config import access_token, accountID
#y finance only allows 60 days of data when trying to get low interval data
data = yf.download("EURUSD=X", start="2025-5-1", end=date.today(), interval='15m') #change later to 15m
data.iloc[-1:,:]
#data.Open.iloc

def signal(df): 
    open = df.Open.iloc[-1]
    close = df.Close.iloc[-1]
    previous_open = df.Open.iloc[-2]
    previous_close = df.Open.iloc[-2]

    #Bearish Market
    if(open > close and previous_open < previous_close and close<previous_open and open>=previous_close): 
        return 1
    #Bullish market
    elif (open < close and previous_open>previous_close and close>previous_open and open>=previous_close):
        return 2
    #return 0 if no clear pattern is there
    else: 
        return 0
    
signals = []
signals.append(0)
for i in range(1, len(data)):
    df = data[i-1: i+1]
    signal.append(signal(df))
data["signal"] = signals
data.signal.value_counts()
#data.iloc[:, :]

def get_candles(n):
    client = CandleClient(access_token, real=False)
    collector = client.get_collector(Pair.EUR_USD, Gran.M15)
    candles = collector.grab(n)
    return candles

candles = get_candles(3)

for candle in candles: 
    print(float(str(candle.bid.o))>1)
# barath test

def trading_job():
    candles = get_candles(3)
    dfstream = pd.DataFrame(columns = ['Open','Close','High','Low'])

    i = 0

    for candle in candles:
        dfstream.loc[i,['Open']] = float(str(candle.bid.o))
        dfstream.loc[i,['Close']] = float(str(candle.bid.c))
        dfstream.loc[i,['High']] = float(str(candle.bid.h))
        dfstream.loc[i,['Low']] = float(str(candle.bid.l))
        i=i+1

    dfstream['Open'] = dfstream['Open'].astype(float)
    dfstream['Close'] = dfstream['Close'].astype(float)
    dfstream['High'] = dfstream['High'].astype(float)
    dfstream['Low'] = dfstream['Low'].astype(float)

    signal = signal_generator(dfstream.iloc[:-1,:])

# Executing orders
# AccountID = "XXXXXXX" #your account ID here
    client = API(access_token)

    SLTPRatio = 2.

    previous_candleR = abs(dfstream['Highg'].iloc[-2]-dfstream['Close'].iloc[-2])

    SLBuy = float(str(candle.bid.o))-previous_candleR
    SLSell = float(str(candle.bid.o))+previous_candleR

    TPBuy = float(str(candle.bid.o))+previous_candleR*SLTPRatio
    TPSell = float(str(candle.bid.o))-previous_candleR*SLTPRatio

    print(dfstream.iloc[:-1,:])
    print(TPBuy, " ", SLBuy, " ", TPSell, " ", SLSell)

    #Sell
    if signal == 1:
        mo = MarketOrderRequest(instruments="Eur_USD",units=-1000, TakeProfitsOnFill=TakeProfitDetails(price=TPSell).data, stopLossOnFill=StopLossDetails(price=SLSell).data)
        r = orders.OrderCreate(accountID,data = mo.data)
        rv = client.request(r)
        print(rv)
    #Buy
    if signal == 2:
        mo = MarketOrderRequest(instruments="Eur_USD",units=1000, TakeProfitsOnFill=TakeProfitDetails(price=TPSell).data, stopLossOnFill=StopLossDetails(price=SLSell).data)
        r = orders.OrderCreate(accountID,data = mo.data)
        rv = client.request(r)
        print(rv)
        
