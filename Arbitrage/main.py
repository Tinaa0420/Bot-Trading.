import requests # To get data from API
import time # To have time.sleep()
import pandas as pd # To have dataframe
from datetime import datetime # To have hour 
import pytz # To have hour in Local zone
import traceback # To have error in console
import random

EXCHANGE = {"binance", "bybit"}
SYMBOL = "BTC"
WALLET = {"USDT": 1000,
          "BTC": 0,
          }
STARTWALLET = WALLET["USDT"]
RANGE = 10000
start_time = time.time()
seconds_in_a_week = 7 * 24 * 60 * 60 


def get_request(url):
    try:
        response = requests.get(url)
        return response.json()
    except Exception as e:
        print("Erreur lors de la requête :")
        print(str(e))
        print(traceback.format_exc())
        return None

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
        return None

def buy_token(token, last_price):
    try:
        global WALLET
        amountDollars = WALLET["USDT"]
        amountToken = amountDollars/last_price
        WALLET["USDT"] -= amountDollars 
        try:
            WALLET[f"{token}"] += amountToken
        except:
            WALLET[f"{token}"] = amountToken
        print(WALLET)
    except Exception as e:
        print("Erreur lors de l'achat :")
        print(str(e))
        print(traceback.format_exc())
    
def sell_token(token, last_price):
    try:
        global WALLET
        amountToken = WALLET[f"{token}"]
        amountDollars = amountToken*last_price
        WALLET["USDT"] += amountDollars 
        WALLET[f"{token}"] -= amountToken
        print(WALLET)
    except Exception as e:
        print("Erreur lors de la vente :")
        print(str(e))
        print(traceback.format_exc())     
def wait(timer):
    compteur = timer
    while compteur > 0:
        compteur -= 5
        print(f"Temps restant : {compteur}")
        time.sleep(5)
def makeRandomBuyOrSell():
    price = get_price_symbol("binance", SYMBOL)
    buy_token(SYMBOL, price)
    isBuy = True
    WAIT = random.randint(1, RANGE)
    print(f"Je ferai une vente dans {WAIT}sec")
    # time.sleep(WAIT)
    wait(WAIT)
    sell_token(SYMBOL, price)

while time.time() - start_time < seconds_in_a_week:
    makeRandomBuyOrSell()