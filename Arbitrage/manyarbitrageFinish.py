# Dans ce code ici j'ai decider de faire un arbitrage 
# entre 2 exchanges (binance et bybit) pour le BTC, ETH, BNB, LTC, AVAX

import requests # To get data from API
import time # To have time.sleep()
import pandas as pd # To have dataframe
from datetime import datetime # To have hour
import pytz # To have hour in Local zone
import traceback # To have error in console
EXCHANGE = {"binance", "bybit"}
START_AMOUNT = 1000000
WALLETARBITRAGE = {"USDT": START_AMOUNT, "BTC": 0, "ETH": 0, "BNB": 0, "LTC": 0, "AVAX": 0}
WALLETBUYSELLRANDOM = {"USDT": START_AMOUNT, "BTC": 0, "ETH": 0, "BNB": 0, "LTC": 0, "AVAX": 0}

# Liste des 5 symboles que je vais utilise avec le pourcentage de mon capital que je veux investir
SYMBOL_LIST = {"BTC": 0.5, "ETH":0.2, "BNB":0.1, "LTC":0.1, "AVAX":0.1}
start_time = time.time()
seconds_in_a_week = 7 * 24 * 60 * 60 
list_amount_usdt_arbitrage = []
list_amount_usdt_random = []

def get_request(url):
    try:
        response = requests.get(url)
        return response.json()
    except Exception as e:
        print("Erreur lors de la requête :")
        print(str(e))
        print(traceback.format_exc())

def get_price_symbol(exchange, symbol):
    # retourne le prix d'un symbole sur un exchange sous forme de float
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

def get_array_prices():
    try:
        LASTPRICES = []
        for symbol in SYMBOL_LIST: # Pour chaque symbole dans la liste des symboles
            each_symbol_dict = {} 
            each_symbol_dict["symbol"] = symbol 
            for exchange in EXCHANGE: # Pour chaque exchange dans la liste des exchanges
                last_price = get_price_symbol(exchange, symbol) # On recupere le prix du symbole sur l'exchange
                each_symbol_dict[exchange] = last_price # On ajoute le prix du symbole sur l'exchange dans le dictionnaire
            LASTPRICES.append(each_symbol_dict) 
        return LASTPRICES # On retourne la liste des dictionnaires
    except Exception as e:
        print("Erreur lors de la récupération des prix :")
        print(str(e))
        print(traceback.format_exc())

def get_min_max_prices(list_prices):
    # retourne le prix min et le prix max d'un symbole sur les 2 exchanges
    try:
        bybit = list_prices['bybit']
        binance = list_prices['binance']
        return min(bybit, binance), max(bybit, binance)
    except Exception as e:
        print("Erreur lors de la récupération du prix min :")
        print(str(e))
        print(traceback.format_exc())
        
def buy_token(token, last_price, wallet, amountUSDT):
    try:
        amountDollars = amountUSDT*SYMBOL_LIST[token]
        amountToken = amountDollars/last_price
        wallet["USDT"] -= amountDollars 
        if f"{token}" in wallet:
            wallet[f"{token}"] += amountToken
        else:
            wallet[f"{token}"] = amountToken
    except Exception as e:
        print("Erreur lors de l'achat :")
        print(str(e))
        print(traceback.format_exc())
    
def sell_token(token, last_price, wallet):
    try:
        amountToken = wallet[f"{token}"]
        amountDollars = amountToken*last_price
        wallet["USDT"] += amountDollars 
        wallet[f"{token}"] -= amountToken
    except Exception as e:
        print("Erreur lors de la vente :")
        print(str(e))
        print(traceback.format_exc()) 
        
def get_plus_value(wallet):
    try:
        return wallet["USDT"] - START_AMOUNT
    except Exception as e:
        print("Erreur lors de la récupération de la plus-value :")
        print(str(e))
        print(traceback.format_exc())

def get_plus_value_last_tx(wallet, list_amount_usdt):
    try:
        if len(list_amount_usdt) > 1:
            plus_value_last_tx = list_amount_usdt[-1] - list_amount_usdt[-2]
            return round(plus_value_last_tx, 2)
        else:
            return wallet["USDT"] - START_AMOUNT
    except Exception as e:
        print("Erreur lors de la récupération de la plus-value de la derniere transaction :")
        print(str(e))
        print(traceback.format_exc())
        
def wait(timer):
    compteur = timer
    while compteur > 0:
        compteur -= 1
        print(f"Temps restant : {compteur}")
        time.sleep(1)
        
def arbitrage(array_list_prices):
    try:
        amountUSDT = WALLETARBITRAGE["USDT"]
        for list_prices in array_list_prices: # Pour chaque dictionnaire dans la liste des dictionnaires
            symbole = list_prices['symbol']
            min_prices, max_prices = get_min_max_prices(list_prices)
            if min_prices < max_prices*0.9995:
                print(f"Symbole: {symbole} - Min: {min_prices} - Max: {max_prices}\nArbitrage possible! ==> difference: {round((max_prices-min_prices), 2)}$\n")
                buy_token(symbole, min_prices, WALLETARBITRAGE, amountUSDT)
                sell_token(symbole, max_prices, WALLETARBITRAGE)
            else:
                print(f"Symbole: {symbole} - Min: {min_prices} - Max: {max_prices}\nPas d'arbitrage possible!\n")
        print("--------------------------------------------------")
        list_amount_usdt_arbitrage.append(WALLETARBITRAGE["USDT"])
        plus_value_total = get_plus_value(WALLETARBITRAGE)
        plus_value_last_tx = get_plus_value_last_tx(WALLETARBITRAGE, list_amount_usdt_arbitrage)
        if plus_value_last_tx > 0:
            plus_value_last_tx = "+" + str(round(plus_value_last_tx, 2))
        else:
            plus_value_last_tx = str(round(plus_value_last_tx, 2))
        if plus_value_total > 0:
            print(f"Gain: {round(plus_value_total, 2)}$ ({plus_value_last_tx}$)")
        else:
            print(f"Perte: {round(plus_value_total, 2)}$ ({plus_value_last_tx}$)")
        print("--------------------------------------------------")
    except Exception as e:
        print("Erreur lors de l'arbitrage :")
        print(str(e))
        print(traceback.format_exc())

def take_decision():
    try:  
        array_list_prices = get_array_prices() # On recupere la liste des dictionnaires
        arbitrage(array_list_prices) # On fait de l'arbitrage
                
    except Exception as e:
        print("Erreur lors de la prise de décision :")
        print(str(e))
        print(traceback.format_exc())

def get_time():
    try:
        return datetime.now(pytz.timezone('Europe/Paris')).strftime('%H:%M:%S')
    except Exception as e:
        print("Erreur lors de la recuperation de l'heure :")
        print(str(e))
        print(traceback.format_exc())
    
while time.time() - start_time < seconds_in_a_week:
    print("--------------------------------------------------")
    print(get_time()  + "\n")
    take_decision()
    time.sleep(5)
    