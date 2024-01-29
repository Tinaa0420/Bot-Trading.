import requests
import time
import pandas as pd
from datetime import datetime
import pytz
import traceback

# Define list of symbols and their corresponding weights
SYMBOL_LIST = {"BTC": 0.5, "ETH":0.2, "BNB":0.1, "LTC":0.1, "AVAX":0.1}

START_AMOUNT = 1000000
WALLETSMA = {"USDT": START_AMOUNT, "BTC": 0, "ETH": 0, "BNB": 0, "LTC": 0, "AVAX": 0}
# Initialize empty dictionary to store prices
PRICE_DICT = {symbol: {"values": [], "bought": False} for symbol in SYMBOL_LIST}
list_amount_usdt_sma = []
#-------------------- GET REQUEST --------------------
# Function to make API request
def get_request(url):
    try:
        response = requests.get(url)
        return response.json()
    except Exception as e:
        print("Error during request:")
        print(str(e))
        print(traceback.format_exc())

#-------------------- GET LAST PRICE --------------------
# Function to get the last price of a symbol
def get_last_price(symbol):
    try:
        data = get_request(f"https://api.binance.com/api/v3/ticker/price?symbol={symbol}USDT")
        last_price = data['price']
        return float(last_price)
    except Exception as e:
        print("Error while retrieving price:")
        print(str(e))
        print(traceback.format_exc())

# Function to add the last price to the list of prices
def get_array_prices():
    try:
        for symbol in SYMBOL_LIST: # For each symbol in the list of symbols
            last_price = get_last_price(symbol) # Get the price of the symbol on the exchange
            PRICE_DICT[symbol]['values'].append(last_price) # Add the price to the dictionary
        return PRICE_DICT # Return the list of dictionaries
    except Exception as e:
        print("Error while retrieving prices:")
        print(str(e))
        print(traceback.format_exc())        
        
#-------------------- GET MOVING AVERAGE --------------------
# Function to get the moving average for a list of prices and a given period
def get_moving_average(prices, period):
    try:
        return sum(prices[-period:]) / period
    except Exception as e:
        print("Error during moving average calculation:")
        print(str(e))
        print(traceback.format_exc())

#-------------------- BUY TOKEN --------------------
# Function to buy a token based on its symbol, price, and amount in USDT
def buy_token(token, last_price, wallet, amountUSDT):
    try:
        amountDollars = amountUSDT * SYMBOL_LIST[token]
        amountToken = amountDollars / last_price
        wallet["USDT"] -= amountDollars
        if f"{token}" in wallet:
            wallet[f"{token}"] += amountToken
        else:
            wallet[f"{token}"] = amountToken
        print(f"Buy - {round(amountToken, 2)} {token} - {round(amountDollars, 2)} USDT - Last Price: {round(last_price, 2)}")
    except Exception as e:
        print("Error during buy:")
        print(str(e))
        print(traceback.format_exc())

#-------------------- SELL TOKEN --------------------
# Function to sell a token based on its symbol and price
def sell_token(token, last_price, wallet):
    try:
        amountToken = wallet[f"{token}"]
        amountDollars = amountToken * last_price
        wallet["USDT"] += amountDollars
        wallet[f"{token}"] -= amountToken
        print(f"Sold - {round(amountToken, 2)} {token} - {round(amountDollars, 2)} USDT - Last Price: {round(last_price, 2)}")
    except Exception as e:
        print("Error during sell:")
        print(str(e))
        print(traceback.format_exc())

# Renvoie la plus-value
def get_plus_value(wallet):
    try:
        return round(portfolio_value(wallet) - START_AMOUNT, 3)
    except Exception as e:
        print("Erreur lors de la récupération de la plus-value :")
        print(str(e))
        print(traceback.format_exc())
        
# Renvoie la plus-value de la derniere transaction
def get_plus_value_last_tx(wallet, list_amount_usdt):
    try:
        if len(list_amount_usdt) > 1:
            plus_value_last_tx = list_amount_usdt[-1] - list_amount_usdt[-2]
            return round(plus_value_last_tx, 2)
        else:
            return get_plus_value(wallet)
    except Exception as e:
        print("Erreur lors de la récupération de la plus-value de la derniere transaction :")
        print(str(e))
        print(traceback.format_exc())
        
# Renvoie le profit ou la perte
def get_profit_and_loss(wallet, list_amount_usdt):
    try:
        list_amount_usdt.append(portfolio_value(wallet)) # On ajoute le montant en USDT dans la liste
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
    except Exception as e:
        print("Erreur lors de la récupération de la plus-value ou de la perte :")
        print(str(e))
        print(traceback.format_exc())


#-------------------- GET TIME --------------------
# Returns the current time
def get_time():
    try:
        return datetime.now(pytz.timezone('Europe/Paris')).strftime('%H:%M:%S')
    except Exception as e:
        print("Error while getting the time:")
        print(str(e))
        print(traceback.format_exc())

#-------------------- GET DATE --------------------
# Returns the current date
def get_date():
    try:
        return datetime.now(pytz.timezone('Europe/Paris')).strftime('%Y-%m-%d')
    except Exception as e:
        print("Error while getting the date:")
        print(str(e))
        print(traceback.format_exc())

#-------------------- WAIT --------------------
# Wait for a certain amount of time while displaying a countdown
def wait(timer):
    compteur = timer
    print("---------- WAIT ----------")
    while compteur > 0:
        compteur -= 1
        print(f"Time remaining: {compteur}")
        time.sleep(1)

def portfolio_value(wallet):
    try:
        value = 0
        for symbol in SYMBOL_LIST:
            value += wallet[symbol] * get_last_price(symbol)
        value += wallet["USDT"]
        return round(value, 3)
    except Exception as e:
        print("Error while getting portfolio value:")
        print(str(e))
        print(traceback.format_exc())


def SMA(prices, symbol):
    try:
        sma1 = get_moving_average(prices, WINDOW_SCALE_1)
        sma2 = get_moving_average(prices, WINDOW_SCALE_2)
        print(f"SMA{WINDOW_SCALE_1}: {sma1}")
        print(f"SMA{WINDOW_SCALE_2}: {sma2}")
        
        portfolio_values = portfolio_value(WALLETSMA)
        BOUGHT = PRICE_DICT[symbol]["bought"]
        if not BOUGHT and sma1 > sma2 and not premier_achat:
            print(f"Buy signal detected. Purchase price: {prices[-1]} USDT")
            buy_token(symbol, prices[-1], WALLETSMA, portfolio_values)
            BOUGHT = True
            PRICE_DICT[symbol]["bought"] = True
        elif BOUGHT and sma1 < sma2:
            print(f"Sell signal detected. Selling price: {prices[-1]} USDT")
            sell_token(symbol, prices[-1], WALLETSMA)
            BOUGHT = False
            PRICE_DICT[symbol]["bought"] = False
            print(f"Wallet: {WALLETSMA}")
        return get_profit_and_loss(WALLETSMA, list_amount_usdt_sma)
    except Exception as e:
        print("Error during SMA:")
        print(str(e))
        print(traceback.format_exc())
    

#-------------------- DECISION FUNCTION --------------------
# Make a decision to buy or sell based on moving averages
def run_SMA(prices, symbol):
    try:
        SMA_Profit_Loss, plus_value_total, plus_value_last_tx = SMA(prices, symbol)
        # print(f"SMA: {SMA_Profit_Loss}")
        print(list_amount_usdt_sma)
        return plus_value_total, plus_value_last_tx
    except Exception as e:
        print("Error while making decision:")
        print(str(e))
        print(traceback.format_exc())
        
NUMBERS_OF_TRANSACTION = 0
POSSIBLE = False
WINDOW_SCALE_1 = 4
WINDOW_SCALE_2 = 10
while True:
    array_prices = get_array_prices()
    NUMBERS_OF_TRANSACTION += 1
    for symbol in SYMBOL_LIST:
        premier_achat = PRICE_DICT[symbol]["bought"]
        print("--------------------------------------------------")
        print(f"{get_time()} - Current price of {symbol}: {array_prices[symbol]['values'][-1]} USDT, {NUMBERS_OF_TRANSACTION} transactions")
        if len(array_prices[symbol]['values']) >= WINDOW_SCALE_2:
            plus_value_total, plus_value_last_tx = run_SMA(PRICE_DICT[symbol]['values'], symbol)
            if not POSSIBLE:
                POSSIBLE = True
    if POSSIBLE:
        wait(10)
    else:
        wait(1)