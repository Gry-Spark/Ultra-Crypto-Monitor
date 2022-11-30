import streamlit as st
import pandas as pd
import binance.client
from binance.client import Client
import seaborn as sns




import pandas as pd 
import numpy as np  
import datetime as dt
import numpy as np
import pandas_ta as ta 
import talib as taa 
import pandas as pd
from PyQt5.QtCore import *
from PyQt5.QtGui import *
import sys
import os
import PySide2
dirname = os.path.dirname(PySide2.__file__)
plugin_path = os.path.join(dirname, 'plugins', 'platforms')
os.environ['QT_QPA_PLATFORM_PLUGIN_PATH'] = plugin_path
from PySide2.QtWidgets import *
import binance.client
from binance.client import Client

st.set_page_config(layout="wide")

#Binance api
Pkey = '5tkCncueCdFgtWW7lb0mqa73pP88iPZgR0XTNIQPcVrYSi5rId6NwC2PVdegA0Ox'
Skey = 'TuS5YKZBxCYglKVY560dORBASH99EHg7Eg8VHHS1NxpqmBXpJbOCkgB4KE2ytiJK'



client = Client(api_key = Pkey, api_secret = Skey)
price_chg_list  = []
TPS_1h_list = []
TPS_1H_LIVE_LISt = []
TPS_chg_1H_list= []
Score48_1h_list = []
ATS_1h_list= []
ATS_chg_1H_list= []
SortData_1h_list= []
coin_list_1h = []
v48_Space_list = []
list_coin_final_sort = []

MAHMAD_LISt = []
#Code

intevral = Client.KLINE_INTERVAL_1HOUR ; depth = '4 days ago UTC+3'

intevral_4 = Client.KLINE_INTERVAL_5MINUTE ; depth_4 = '2500 minutes ago UTC+3'

tickers = ['fdfdfd','BTCUSDT', 'ETHUSDT']

for ticker in tickers:
    try:
        df = client.get_historical_klines(ticker , intevral , depth)
        df = pd.DataFrame(df)
        if not df.empty:
            df[0] = pd.to_datetime(df[0],unit='ms')
            df.columns = ['Date','Open','High','Low','Close','Volume','IGNORE','Quote_Volume','Trades_Count','BUY_VOL','BUY_VOL_VAL','x']
            df ["Open"] = pd.to_numeric(df["Open"])
            df ["High"] = pd.to_numeric(df["High"])
            df ["Low"] = pd.to_numeric(df["Low"])
            df ["Close"] = pd.to_numeric(df["Close"])
            df ["Volume"] = round(pd.to_numeric(df["Volume"]))
            df ["BUY_VOL"] = round(pd.to_numeric(df["BUY_VOL"]))
            df ["Quote_Volume"] = round(pd.to_numeric(df["Quote_Volume"]))
            df ["Trades_Count"] = pd.to_numeric(df["Trades_Count"])
            df ["asset"] = ticker
            avg_price = client.get_avg_price(symbol=ticker)
            avg_price = round(float(avg_price['price']),2)                                                     
            #Buy/Sell volume per succend
            #df ["SELL_VOL"]    = (df.Volume -df.BUY_VOL)
            #df ["BTS"]    = round(df.BUY_VOL /3600,2)
            #df ["BTS:1H %"] = round(df.BTS.pct_change(1)*100,2).fillna(0) 
            #df ["STS"]    = round(df.SELL_VOL /3600,2)
            #df ["STS:1H %"] = round(df.STS.pct_change(1)*100,2).fillna(0) 

            df['mean'] = taa.SUM(df['Volume']*df['Close'],
                                48) / taa.SUM(df['Volume'], 48)
            df['vwapsd'] = np.sqrt(taa.SMA(pow(df['Close']-df['mean'], 2), 48))
            df[f'vwap_zscore{48}'] = (df['Close']-df['mean']) / df['vwapsd']


            #Price
            df ["Price_1H"] = round(df.Close.pct_change(1)*100,2).fillna(0) 
            ##Trades per saccend
            df ["TPS_1h"]    = round(df.Trades_Count /3600,2) 
            df ["TPS_chg_1H"] = round(df.TPS_1h.pct_change(1)*100,2).fillna(0) 
            #ATS  
            df ['ATS_1h'] = df ["Quote_Volume"] / 3600
            df ["ATS_chg_1H"] = round(df.ATS_1h.pct_change(1)*100,2).fillna(0) 
            df ['SortData_1h']  = (df.TPS_1h / df.Price_1H) #* -100
            #df['SortData_1h'] = np.sqrt(round(df["SortData_1h"],2))


            Price_1H = df[f'Price_1H'][95]
            TPS_1h = df["TPS_1h"][94]
            TPS_1h_Live = df["TPS_1h"][95]
            TPS_chg_1H = df[f'TPS_chg_1H'][94]
            Score48_1h = df['vwap_zscore48'][94]               
            ATS_1h = df["ATS_1h"][94]
            ATS_chg_1H = df[f'ATS_chg_1H'][94]
            SortData_1h = df["SortData_1h"][94]
            ticker_1h = df['asset'][94]

            price_chg_list.append(Price_1H)
            TPS_1h_list.append(TPS_1h)
            TPS_1H_LIVE_LISt.append(TPS_1h_Live)
            TPS_chg_1H_list.append(TPS_chg_1H)
            Score48_1h_list.append(Score48_1h)            
            ATS_1h_list.append(ATS_1h)
            ATS_chg_1H_list.append(ATS_chg_1H)
            SortData_1h_list.append(SortData_1h)
            coin_list_1h.append(ticker_1h)

            df_4 = client.get_historical_klines(ticker , intevral_4 , depth_4)
            df_4 = pd.DataFrame(df_4)
            if not df_4.empty:
                df_4[0] = pd.to_datetime(df_4[0],unit='ms')
                df_4.columns = ['Date','Open','High','Low','Close','Volume','IGNORE','Quote_Volume','Trades_Count','BUY_VOL','BUY_VOL_VAL','x']
                df_4 ["Open"] = pd.to_numeric(df_4["Open"])
                df_4 ["High"] = pd.to_numeric(df_4["High"])
                df_4 ["Low"] = pd.to_numeric(df_4["Low"])
                df_4 ["Close"] = pd.to_numeric(df_4["Close"])
                df_4 ["Volume"] = round(pd.to_numeric(df_4["Volume"]))
                df_4 ["BUY_VOL"] = round(pd.to_numeric(df_4["BUY_VOL"]))
                df_4 ["Quote_Volume"] = round(pd.to_numeric(df_4["Quote_Volume"]))
                df_4 ["Trades_Count"] = pd.to_numeric(df_4["Trades_Count"])  
                #df_4.set_index("Date" , inplace=True)
                tpss = df_4 ["Trades_Count"][498]
                TPSS =  tpss / 60

                df_4['vc'] = (( df_4.Close + df_4.Low + df_4.High) / 3) * df_4.Volume 
                df_4['vwap48']=round((df_4['vc'].rolling(window=48).sum())/(df_4['Volume'].rolling(window=48).sum()),100).fillna(method='bfill')
                df_4['vwap84']=round((df_4['vc'].rolling(window=84).sum())/(df_4['Volume'].rolling(window=84).sum()),100).fillna(method='bfill')

                df_4['v48_01'] = (df_4.Close - df_4.vwap48) 
                df_4['v488_02'] = round((df_4.v48_01 / df_4.Close) *100 , 2)

                v48_Space = df_4 ["v488_02"][498]

                MAHMAD_LISt.append(TPSS)
                v48_Space_list.append(v48_Space)
                    #price_chg_list.append(Price_1H)




                dfc = pd.DataFrame()
                dfc['Coin'] = coin_list_1h
                dfc['1H Live %'] = price_chg_list  
                dfc['1hr_tps'] = TPS_1h_list 
                dfc['⚡️W48 5min⚡️'] = v48_Space_list
                dfc['Score48_1h'] = Score48_1h_list
                dfc['TPS_chg_1H'] = TPS_chg_1H_list 
                dfc['TPS_1H_LIVE'] = TPS_1H_LIVE_LISt

                dfc['TPS_5m'] = MAHMAD_LISt
                dfc['🎁Special TPS🎁'] = dfc['⚡️W48_Space5m⚡️'] / dfc['TPS_1h']
                dfc['ATS_1h_list'] = ATS_1h_list
                dfc['ATS_chg_1H_list'] = ATS_chg_1H_list

                
                dfc['Score48_1h'] = Score48_1h_list
                dfc['SortData_final1h'] = SortData_1h_list
                
                

                df ["price_chg_Live"] = pd.to_numeric(df["price_chg_Live"])
                df ["TPS_1h"] = pd.to_numeric(df["TPS_1h"])
                df ["⚡️W48_Space5m⚡️"] = pd.to_numeric(df["⚡️W48_Space5m⚡️"])
                df ["Score48_1h"] = pd.to_numeric(df["Score48_1h"])
                df ["TPS_chg_1H"] = pd.to_numeric(df["TPS_chg_1H"])
                df ["TPS_1H_LIVE"] = pd.to_numeric(df["TPS_1H_LIVE"])
                df ["TPS_5m"] = pd.to_numeric(df["TPS_5m"])
                df ["🎁Special TPS🎁"] = pd.to_numeric(df["🎁Special TPS🎁"])
                df ["ATS_1h_list"] = pd.to_numeric(df["ATS_1h_list"])
                df ["ATS_chg_1H_list"] = pd.to_numeric(df["ATS_chg_1H_list"])

                df ["SortData_final1h"] = pd.to_numeric(df["SortData_final1h"])      
                     
              
                #Price 4H
                df_4 ["Price_4H"] = round(df_4.Close.pct_change(1)*100,2).fillna(0) 
                #TPS
                df_4 ["TPS"]    = round(df.Trades_Count /14400,2) 
                df_4 ["TPS_chg_4H"] = round(df_4.TPS.pct_change(1)*100,2).fillna(0) 
                #ATS  
                df_4 ['ATS'] = df_4 ["Volume"] / df_4 ["Trades_Count"]
                df_4 ["ATS_chg_4H"] = round(df_4.ATS.pct_change(1)*100,2).fillna(0) 
                #Volume
                df_4 ["Vol_chg_4H"] = round(df_4.Volume.pct_change(1)*100,2).fillna(0) 
                df_4 ['SortData']  = df_4.TPS / df_4.Price_4H
    except:
        pass
                
cm = sns.light_palette("green", as_cmap=True)
# Function 
def color_df(val):
    return f'background-color: #ff6300'
# Our example Dataset

# Create Pandas DataFrame
dff = pd.DataFrame(dfc)
 
def color_negative_values(value): 
   """
   This function takes in values of dataframe 
   if particular value is negative it is colored as redwhich implies loss
   if value is greater than one it implies higher profit
   """
   if value < 0:
       color = '#989ba2'
   elif value > 0:
       color = '#c9f35b'
   else:
       color = '#989ba2'
   return f"color: {color}"

# Using Style for the Dataframe

expander_bar = st.expander("TPS")
expander_bar.dataframe(dff.style.applymap(color_negative_values , subset=['price_chg_Live','TPS_1h','⚡️W48_Space5m⚡️','Score48_1h','TPS_chg_1H','TPS_1H_LIVE','TPS_5m','🎁Special TPS🎁','ATS_1h_list','ATS_chg_1H_list','SortData_final1h']).applymap(lambda x: 'font-size:23.2px; background-color: #131c25' ))
