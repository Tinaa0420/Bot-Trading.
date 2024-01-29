# Dans ce code ici j'ai decider de faire un achat et une vente aleatoire 
# sur l'exchange de Binance pour le BTC, ETH, BNB, LTC, AVAX

import requests # To get data from API
import time # To have time.sleep()
import pandas as pd # To have dataframe
from datetime import datetime # To have hour
import pytz # To have hour in Local zone
import traceback # To have error in console
EXCHANGE = {"binance", "bybit"}
START_AMOUNT = 1000000
WALLETBUYSELLRANDOM = {"USDT": START_AMOUNT, "BTC": 0, "ETH": 0, "BNB": 0, "LTC": 0, "AVAX": 0}
SYMBOL_LIST = {"BTC": 0.5, "ETH":0.2, "BNB":0.1, "LTC":0.1, "AVAX":0.1}
start_time = time.time()
seconds_in_a_week = 7 * 24 * 60 * 60 
LIST_AMOUNT_USDT_RANDOM = []
NUMBER_OF_TRANSACTION = 0
import csv
headers = ['Bot', 'Trade', 'Time', 'Date', 'Profit', 'Profit_last_tx', 'Wallet']
with open('trading_data_random.csv', 'w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(headers)
    
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

#-------------------- GET ARRAY PRICES --------------------
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
        print(f"Achat - {round(amountToken, 2)} {token} - {round(amountDollars, 2)} USDT - Last Price: {round(last_price, 2)}")
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
        print(f"Vente - {round(amountToken, 2)} {token} - {round(amountDollars, 2)} USDT - Last Price: {round(last_price, 2)}")
    except Exception as e:
        print("Erreur lors de la vente :")
        print(str(e))
        print(traceback.format_exc()) 
        
#-------------------- GET PLUS VALUE --------------------
# Renvoie la plus-value   
def get_plus_value(wallet):
    try:
        return round(wallet["USDT"] - START_AMOUNT, 2)
    except Exception as e:
        print("Erreur lors de la récupération de la plus-value :")
        print(str(e))
        print(traceback.format_exc())

#-------------------- GET LAST PLUS VALUE --------------------
# Renvoie la plus-value de la derniere transaction 
def get_plus_value_last_tx(wallet, list_amount_usdt):
    try:
        if len(list_amount_usdt) > 1:
            plus_value_last_tx = list_amount_usdt[-1] - list_amount_usdt[-2]
            return round(plus_value_last_tx, 2)
        else:
            return round(wallet["USDT"] - START_AMOUNT, 2)
    except Exception as e:
        print("Erreur lors de la récupération de la plus-value de la derniere transaction :")
        print(str(e))
        print(traceback.format_exc())

# Renvoie le profit ou la perte
def get_profit_and_loss(wallet, list_amount_usdt):
    list_amount_usdt.append(wallet["USDT"]) # On ajoute le montant en USDT dans la liste
    plus_value_total = get_plus_value(wallet) # On récupère la plus-value total
    plus_value_last_tx = get_plus_value_last_tx(wallet, list_amount_usdt) # On récupère la plus-value de la dernière transaction
    # Quelques modifications pour l'affichage
    if plus_value_last_tx >= 0:
        plus_value_last_tx_modified = "+" + str(round(plus_value_last_tx, 2))
    else:
        plus_value_last_tx_modified = str(round(plus_value_last_tx, 2))
    if plus_value_total >= 0:
        profit = f"Gain: +{round(plus_value_total, 2)}$ ({plus_value_last_tx_modified}$)"
        return profit, plus_value_total, plus_value_last_tx
    else:
        loss = f"Perte: {round(plus_value_total, 2)}$ ({plus_value_last_tx_modified}$)"
        return loss, plus_value_total, plus_value_last_tx

#-------------------- BUY/SELL RANDOM --------------------
def makeRandomBuyOrSell():
    try:
        array_list_prices = get_array_prices()
        amountUSDT = WALLETBUYSELLRANDOM["USDT"]
        for list_prices in array_list_prices:
            symbole = list_prices['symbol']
            buy_token(symbole, list_prices[list(EXCHANGE)[0]], WALLETBUYSELLRANDOM, amountUSDT)
        wait(5)
        array_list_prices = get_array_prices()
        for list_prices in array_list_prices:
            symbole = list_prices['symbol']
            sell_token(symbole, list_prices[list(EXCHANGE)[0]], WALLETBUYSELLRANDOM)
        return get_profit_and_loss(WALLETBUYSELLRANDOM, LIST_AMOUNT_USDT_RANDOM)
    except Exception as e:
        print("Erreur lors de la vente :")
        print(str(e))
        print(traceback.format_exc())
        
#-------------------- WRITE TO CSV --------------------
def write_to_csv(bot, trade, heure, date, profit, profit_last_tx, wallet):
    data = [bot, trade, heure, date, profit, profit_last_tx, wallet]
    with open('trading_data_random.csv', 'a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(data)

def get_time():
    try:
        return datetime.now(pytz.timezone('Europe/Paris')).strftime('%H:%M:%S')
    except Exception as e:
        print("Erreur lors de la recuperation de l'heure :")
        print(str(e))
        print(traceback.format_exc())

def get_date():
    try:
        return datetime.now(pytz.timezone('Europe/Paris')).strftime('%Y-%m-%d')
    except Exception as e:
        print("Erreur lors de la récupération de la date :")
        print(str(e))
        print(traceback.format_exc())
def wait(timer):
    compteur = timer
    while compteur > 0:
        compteur -= 1
        print(f"Temps restant : {compteur}")
        time.sleep(1)

def run_random():
    try:
        Arbitrage_Profit_Perte, plus_value_total, plus_value_last_tx = makeRandomBuyOrSell() # On fait de l'arbitrage
        print("--------------------------------------------------")
        print(f"Aleatoire: {Arbitrage_Profit_Perte}")
        return plus_value_total, plus_value_last_tx
    except Exception as e:
        print("Erreur lors de la prise de décision :")
        print(str(e))
        print(traceback.format_exc())

print("Bot en cours d'execution...") 
while time.time() - start_time < seconds_in_a_week:
    NUMBER_OF_TRANSACTION += 1
    TEMPS = time.time() - start_time
    print("--------------------------------------------------")
    print(f"{get_time()} - Number of transactions: {NUMBER_OF_TRANSACTION} - Temps d'execution: {round(TEMPS, 2)}s\n")
    plus_value_total, plus_value_last_tx = run_random()
    write_to_csv("Aleatoire", f"Trade {NUMBER_OF_TRANSACTION}", get_time(), get_date(), plus_value_total, plus_value_last_tx, WALLETBUYSELLRANDOM)
    time.sleep(5)