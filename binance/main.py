import requests
import time
import pandas as pd
from datetime import datetime

BASE_URL = "https://api.binance.com"
SYMBOL = "BTCUSDT"

INTERVAL = 86400
date_start = int(datetime.now().timestamp())
date_end = int(datetime(2023, 12, 25, 12, 0, 0).timestamp())

def get_request(url):
    try:
        response = requests.get(url)
        return response.json()
    except:
        return "erreur"

def get_price_symbol(symbol):
    ticker_url = f"{BASE_URL}/api/v3/ticker/price?symbol={symbol}"
    ticker_info = get_request(ticker_url)
    last_price = float(ticker_info["price"])
    print(f"Le dernier prix du BTC est de : {last_price} USDT")
    return last_price

def get_everytime_price():
    last_price = get_price_symbol(SYMBOL)
    time.sleep(1)
    return last_price

def buy_token(amount, balance, last_price):
    balance -= (last_price * amount)
    return balance
    
def sell_token(amount, balance, last_price):
    balance += (last_price * amount)
    return balance

def follow_chart():
    compteur_interval = 0
    balance = 1000
    buy_threshold = 21840
    sell_threshold = 21815
    while date_start <= date_end:
        last_price = get_everytime_price()
        if compteur_interval > 1:
            compteur_interval -= 1
            print(f"Il reste {compteur_interval} secondes avant de pouvoir acheter")

        if (last_price < buy_threshold) and compteur_interval == 0:
            amount = 0.01
            compteur_buy = buy_token(0.01, balance, last_price)
            compteur_interval = INTERVAL
            print(f"##### Vous avez acheté {amount} BTC au prix de {last_price} USDT #####")
            print(f"Il vous reste {balance - compteur_buy} USDT")
        if (last_price > sell_threshold) and compteur_interval == 0:
            amount = 0.01
            compteur_sell = sell_token(amount, balance, last_price)
            compteur_interval = INTERVAL
            print(f"##### Vous avez vendu {amount} BTC au prix de {last_price} USDT#####")
            print(f"Il vous reste {balance + compteur_sell } USDT")
            
follow_chart()