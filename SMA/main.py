# README
# Algo de trading basé sur les moyennes mobiles

import requests # To get data from API
import time # To have time.sleep()
import pandas as pd # To have dataframe
from datetime import datetime # To have hour
import pytz # To have hour in Local zone
import traceback # To have error in console

EXCHANGE = {"binance", "bybit"}
SYMBOL = "BTC"
INTERVAL = "1s"
LIMIT = 1
# STARTTIME = int((time.time() - LIMIT * 86400) * 1000)  # timestamp en millisecondes
START_AMOUNT = 1000000
WALLETSMA = {"USDT": START_AMOUNT}
BOUGHT = False
SYMBOL_LIST = {"BTC": 0.5, "ETH":0.2, "BNB":0.1, "LTC":0.1, "AVAX":0.1}
SYMBOL_LIST_INIT = {"BTC":0.5}
LISTDATAFRAME = []
LISTPRICE = []
start_time = time.time()
seconds_in_a_week = 7 * 24 * 60 * 60 
#-------------------- REQUESTS --------------------
def get_request(url):
    try:
        response = requests.get(url)
        return response.json()
    except Exception as e:
        print("Erreur lors de la requête :")
        print(str(e))
        print(traceback.format_exc())
        
#-------------------- GET LAST PRICE --------------------
def get_price_symbol(exchange, symbol):
    try:
        if exchange == "binance":
            data = get_request(f"https://api.binance.com/api/v3/ticker/price?symbol={symbol}USDT")
            last_price = data['price']
        elif exchange == "bybit":
            data = get_request(f"https://api.bybit.com/v2/public/tickers?symbol={symbol}USDT")
            last_price = data['result'][0]['last_price']
        return float(last_price)
    except Exception as e:
        print("Erreur lors de la récupération du prix :")
        print(str(e))
        print(traceback.format_exc())
        
#-------------------- GET DATAFRAME --------------------
def get_dataframe_symbol(symbol, interval, limit):
    klines_url = f"https://api.binance.com/api/v3/klines?symbol={symbol}USDT&interval={interval}&limit={limit}"
    data = get_request(klines_url)
    df = pd.DataFrame(data, columns=["Open time", "Open", "High", "Low", "Close", "Volume", "Close time", "Quote asset volume", "Number of trades", "Taker buy base asset volume", "Taker buy quote asset volume", "Ignore"])
    df = df.assign(Symbol=symbol)
    return df
#-------------------- SMA --------------------
def get_sma9(df):
    return df["Close"].rolling(window=9).mean()
def get_sma20(df):
    return df["Close"].rolling(window=20).mean()
#-------------------- MODIFY DATAFRAME --------------------
def modify_dataframe(symbol, interval, limit):
    try:
        df = get_dataframe_symbol(symbol, interval, limit)
        df["Open time"] = pd.to_datetime(df["Open time"], unit='ms', utc=True)
        df["Open time"] = df["Open time"].dt.tz_convert('Europe/Paris').strftime('%Y-%m-%d %H:%M:%S')
        # df = df.loc[:, ["Open time", "Close"]]
        df["SMA9"] = get_sma9(df)
        df["SMA20"] = get_sma20(df)
        # df.dropna(subset=["SMA9", "SMA20"], inplace=True)
        df = df.astype({'Close':float, "SMA9":float, "SMA20":float}).round(4)
        
        return df
    except Exception as e:
        print("Erreur lors de la modification du dataframe :")
        print(str(e))
        print(traceback.format_exc())
        
print(modify_dataframe(SYMBOL, INTERVAL, LIMIT))
#-------------------- BUY --------------------
# Acheter en fonction du token, du prix et du montant en USDT
def buy_token(token, last_price, wallet, amountUSDT):
    try:
        amountDollars = amountUSDT*SYMBOL_LIST[token]
        amountToken = amountDollars/last_price
        wallet["USDT"] -= amountDollars 
        if f"{token}" in wallet:
            wallet[f"{token}"] += amountToken
        else:
            wallet[f"{token}"] = amountToken
        print("Achat de", amountToken, token, "pour", amountDollars, "USDT")
    except Exception as e:
        print("Erreur lors de l'achat :")
        print(str(e))
        print(traceback.format_exc())
        
#-------------------- SELL --------------------
# Vend en fonction du token et du prix
def sell_token(token, last_price, wallet):
    try:
        amountToken = wallet[f"{token}"]
        amountDollars = amountToken*last_price
        wallet["USDT"] += amountDollars 
        wallet[f"{token}"] -= amountToken
        print("Vente de", amountToken, token, "pour", amountDollars, "USDT")
    except Exception as e:
        print("Erreur lors de la vente :")
        print(str(e))
        print(traceback.format_exc())
     
    
def get_time():
    try:
        return datetime.now(pytz.timezone('Europe/Paris')).strftime('%Y-%m-%d %H:%M:%S')
    except Exception as e:
        print("Erreur lors de la recuperation de l'heure :")
        print(str(e))
        print(traceback.format_exc())
# def take_decision():
#     global BOUGHT
#     df = modify_dataframe()
#     for dataframe in df:
#         # print(dataframe)
#         for i in range(0, len(dataframe)):
#             amountUSDT = WALLETSMA["USDT"]
#             if dataframe['SMA9'][i] >= dataframe['SMA20'][i] and BOUGHT == False:
#                 print(dataframe['Open time'][i], "Ici je dois acheter\nPrix d'achat : ", dataframe['Close'][i], "USDT")
#                 buy_token(SYMBOL, dataframe["Close"][i], WALLETSMA, amountUSDT)
#                 BOUGHT = True
#             elif dataframe['SMA9'][i] < dataframe['SMA20'][i] and BOUGHT == True:
#                 print(dataframe['Open time'][i], "Ici je dois vendre\nPrix de vente : ", dataframe['Close'][i], "USDT")
#                 sell_token(SYMBOL, dataframe["Close"][i], WALLETSMA)
#                 BOUGHT = False
#                 print("Mon portefeuille : ", WALLETSMA)

    
# while time.time() - start_time < seconds_in_a_week:
#     for symbol in SYMBOL_LIST_INIT:
#         df = modify_dataframe(symbol, interval=INTERVAL, limit=1)
#         LISTPRICE.append(df["Close"])
#     print(LISTPRICE)
#     time.sleep(1)