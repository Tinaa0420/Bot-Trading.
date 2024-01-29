import requests
import time
import pandas as pd
from datetime import datetime
import pytz
import traceback
import csv
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
###################################################
#################### REQUEST ######################
#-------------------- GET REQUEST --------------------
# Function to make API request, return json
def get_request(URL):
    try:
        response = requests.get(URL)
        return response.json()
    except Exception as e:
        print("Error in get_request():")
        print(str(e))
        print(traceback.format_exc())
        time.sleep(60*10)
###################################################
#################### PRICE INFO ###################
#-------------------- GET LAST PRICE ------------------
# return last price of a symbol as float
def get_last_price(EXCHANGE, SYMBOL):
    try:
        last_price = 0
        if EXCHANGE == "binance":
            data = get_request(f"https://api.binance.com/api/v3/ticker/price?symbol={SYMBOL}USDT")
            try:
                last_price = data['price']
            except:
                last_price = None
        elif EXCHANGE == "bybit":
            data = get_request(f"https://api.bybit.com/v2/public/tickers?symbol={SYMBOL}USDT")
            try:
                last_price = data['result'][0]['last_price']
            except:
                last_price = None
        return float(last_price) if last_price else None
    except Exception as e:
        print("Error in get_last_price():")
        print(str(e))
        print(traceback.format_exc())
#-------------------- GET ARRAY PRICE --------------------
# example: [{'symbol': 'BTC', 'binance': 30330.0, 'bybit': 30339.1}, {'symbol': 'ETH', 'binance': 2100.15, 'bybit': 2100.33}] 
def get_array_prices(SYMBOL_LIST, EXCHANGE):
    try:
        LASTPRICES = []
        for symbol in SYMBOL_LIST: # for each symbol in the list of symbols
            each_symbol_dict = {} 
            each_symbol_dict["symbol"] = symbol 
            for exchange in EXCHANGE: # for each exchange in the list of exchanges
                last_price = get_last_price(exchange, symbol) # Get the price of the symbol on the exchange
                while last_price == None: # If the price is None, try again
                    last_price = get_last_price(exchange, symbol)
                    time.sleep(30)
                each_symbol_dict[exchange] = last_price # Add the price to the dictionary
            LASTPRICES.append(each_symbol_dict) # Add the dictionary to the list
        return LASTPRICES # Return the list of dictionaries
    except Exception as e:
        print("Error in get_array_prices():")
        print(str(e))
        print(traceback.format_exc())
#-------------------- GET ARRAY PRICE FOR SMA --------------------
# example: {'BTC': {'values': [], 'bought': False}, 'ETH': {'values': [], 'bought': False}}
def get_array_prices_sma(SYMBOL_LIST, EXCHANGE, PRICE_DICT):
    try:
        for symbol in SYMBOL_LIST: # For each symbol in the list of symbols
            last_price = get_last_price(EXCHANGE[0], symbol) # Get the price of the symbol on the exchange
            while last_price == None: # If the price is None, try again
                last_price = get_last_price(EXCHANGE[0], symbol)
                time.sleep(30)
            PRICE_DICT[symbol]['values'].append(last_price) # Add the price to the dictionary
        return PRICE_DICT # Return the list of dictionaries
    except Exception as e:
        print("Error in get_array_prices_sma():")
        print(str(e))
        print(traceback.format_exc())   
#-------------------- GET MIN MAX --------------------
# return min and max price of a symbol as float
def get_min_max_prices(list_prices):
    try:
        bybit = list_prices['bybit']
        binance = list_prices['binance']
        try:
            return min(bybit, binance), max(bybit, binance)
        except:
            return None, None
    except Exception as e:
        print("Error in get_min_max_prices():")
        print(str(e))
        print(traceback.format_exc())  
        
###################################################
#################### TRADE ########################
#-------------------- BUY --------------------
# Buy according to the token, the price and the amount of USDT
def buy_token(symbol, last_price, wallet, amountUSDT, SYMBOL_LIST):
    try:
        amountDollars = amountUSDT*SYMBOL_LIST[symbol] 
        if amountDollars >= wallet["USDT"]: 
            amountDollars = wallet["USDT"]
        amountToken = amountDollars/last_price
        wallet["USDT"] -= amountDollars
        if f"{symbol}" in wallet:
            wallet[f"{symbol}"] += amountToken
        else:
            wallet[f"{symbol}"] = amountToken
        print(f"Buy - {round(amountToken, 2)} {symbol} - {round(amountDollars, 2)} USDT - Last Price: {round(last_price, 2)}")
        return round(amountDollars, 3)
    except Exception as e:
        print("Error in buy_token():")
        print(str(e))
        print(traceback.format_exc())
#-------------------- SELL --------------------
# Sell according to the token and the price 
def sell_token(symbol, last_price, wallet):
    try:
        amountToken = wallet[f"{symbol}"]
        amountDollars = amountToken*last_price
        wallet["USDT"] += amountDollars 
        wallet[f"{symbol}"] -= amountToken
        print(f"Sell - {round(amountToken, 2)} {symbol} - {round(amountDollars, 2)} USDT - Last Price: {round(last_price, 2)}")
        return round(amountDollars, 3)
    except Exception as e:
        print("Error in sell_token():")
        print(str(e))
        print(traceback.format_exc()) 
    
###################################################
#################### TIME #########################    
def get_time():
    try:
        return datetime.now(pytz.timezone('Europe/Paris')).strftime('%H:%M:%S')
    except Exception as e:
        print("Error in get_time():")
        print(str(e))
        print(traceback.format_exc())
def get_date():
    try:
        return datetime.now(pytz.timezone('Europe/Paris')).strftime('%Y-%m-%d')
    except Exception as e:
        print("Error in get_date():")
        print(str(e))
        print(traceback.format_exc())
def wait(timer):
    counter = timer
    while counter > 0:
        counter -= 1
        print(f"TIME LEFT : {counter}")
        time.sleep(1)
        
###################################################
#################### PORTFOLIO ####################
def portfolio_value(wallet, SYMBOL_LIST, EXCHANGE):
    try:
        value = 0
        for symbol in SYMBOL_LIST:
            last_price = get_last_price(EXCHANGE[0], symbol)
            while last_price == None:
                last_price = get_last_price(EXCHANGE[0], symbol)
                time.sleep(30)
            value += wallet[symbol] * last_price
        value += wallet["USDT"]
        return round(value, 3)
    except Exception as e:
        print("Error while getting portfolio value:")
        print(str(e))
        print(traceback.format_exc())

#-------------------- GET PLUS VALUE --------------------
# Return the plus value of the portfolio 
def get_capital_gain(wallet, START_AMOUNT, SYMBOL_LIST, EXCHANGE):
    try:
        return round(portfolio_value(wallet, SYMBOL_LIST, EXCHANGE) - START_AMOUNT, 2)
    except Exception as e:
        print("Error in get_capital_gain():")
        print(str(e))
        print(traceback.format_exc())

#-------------------- GET LAST PLUS VALUE --------------------
# Return the plus value of the last transaction 
def get_capital_gain_last_tx(wallet, list_amount_usdt, START_AMOUNT, SYMBOL_LIST, EXCHANGE):
    try:
        if len(list_amount_usdt) > 1:
            capital_gain_last_tx = list_amount_usdt[-1] - list_amount_usdt[-2]
            return round(capital_gain_last_tx, 2)
        else:
            return get_capital_gain(wallet, START_AMOUNT, SYMBOL_LIST, EXCHANGE)
    except Exception as e:
        print("Error in get_capital_gain_last_tx():")
        print(str(e))
        print(traceback.format_exc())

#-------------------- GET PROFIT AND LOSS --------------------
# Return the profit and loss of the portfolio
def get_profit_and_loss(wallet, list_amount_usdt, START_AMOUNT, SYMBOL_LIST, EXCHANGE):
    try:
        list_amount_usdt.append(wallet["USDT"])
        capital_gain_total = get_capital_gain(wallet, START_AMOUNT, SYMBOL_LIST, EXCHANGE) 
        capital_gain_last_tx = get_capital_gain_last_tx(wallet, list_amount_usdt, START_AMOUNT, SYMBOL_LIST, EXCHANGE) 
        if capital_gain_last_tx >= 0:
            capital_gain_last_tx_modified = "+" + str(round(capital_gain_last_tx, 2))
        else:
            capital_gain_last_tx_modified = str(round(capital_gain_last_tx, 2))
        if capital_gain_total >= 0:
            profit = f"Gain: +{round(capital_gain_total, 2)}$ ({capital_gain_last_tx_modified}$)"
            return profit, capital_gain_total, capital_gain_last_tx
        else:
            loss = f"Loss: {round(capital_gain_total, 2)}$ ({capital_gain_last_tx_modified}$)"
            return loss, capital_gain_total, capital_gain_last_tx
    except Exception as e:
        print("Error in get_profit_and_loss():")
        print(str(e))
        print(traceback.format_exc())
###################################################
#################### CSV ##########################
#-------------------- WRITE TO CSV --------------------
def write_to_csv(bot, trade, time, date, profit, profit_last_tx, wallet, name_file):
    try:
        data = [bot, trade, time, date, profit, profit_last_tx, wallet]
        with open(name_file, 'a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(data)
    except Exception as e:
        print("Error in write_to_csv():")
        print(str(e))
        print(traceback.format_exc())
        
def init_header_csv(name_file, headers):
    try:
        with open(name_file, 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(headers)
    except Exception as e:
        print("Error in init_header_csv():")
        print(str(e))
        print(traceback.format_exc())
def read_csv_to_graph(name_file):	
    data = pd.read_csv(name_file, parse_dates=['Date'], index_col='Date')

    daily_data = data.groupby(data.index.date)['Profit_last_tx'].sum()

    # Create a new figure and axis for the plot
    fig, ax = plt.subplots(figsize=(10, 6))

    # Plot daily data (x-axis: dates, y-axis: sum of Profit_last_tx) with round markers and a solid line
    ax.plot(daily_data.index, daily_data.values, marker='o', linestyle='-', color='white')

    # Configure the x-axis to display dates correctly with format 'day-month'
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%d-%m'))

    # Set the x-axis label locations with a one-day interval
    ax.xaxis.set_major_locator(mdates.DayLocator(interval=1))

    # Rotate the x-axis labels by 45 degrees for better readability
    plt.xticks(rotation=45, color='white')
    plt.xlabel('Date', color='white')
    plt.ylabel('Profit', color='white')
    plt.title('Profit/loss per day', color='white')
    plt.grid(True, color='white')

    # Set the background color to black
    ax.set_facecolor('black')
    fig.patch.set_facecolor('black')

    plt.show()