# Author: L2M1
# Team: L2M1 Trading Bot
# Teacher: Mme Elodie Roussel
# Date: 2023 Juanuary - May
# Numbers of peoples in the team: 4

# This is a trading bot program that performs random buying and selling of cryptocurrencies on the 
# Binance exchanges. The bot trades with a fixed starting amount of USDT and a predetermined set of cryptocurrencies. 
# The program uses functions from the "Config" module, which includes severals functions. 
# The program logs each transaction and writes data to a CSV file.


import time # To have time.sleep()
import traceback # To have error in console
import Config # To have the functions

EXCHANGE = ["binance", "bybit"]
START_AMOUNT = 1000000
WALLETBUYSELLRANDOM = {"USDT": START_AMOUNT, "BTC": 0, "ETH": 0, "BNB": 0, "LTC": 0, "AVAX": 0}
SYMBOL_LIST = {"BTC": 0.5, "ETH":0.2, "BNB":0.1, "LTC":0.1, "AVAX":0.1}
START_TIME = time.time()
SECONS_IN_A_WEEK = 7 * 24 * 60 * 60 
LIST_AMOUNT_USDT_RANDOM = []
NUMBER_OF_TRANSACTION = 0
PRICE_DICT = {symbol: 0 for symbol in SYMBOL_LIST}
print(PRICE_DICT)
headers = ['Bot', 'Trade', 'Time', 'Date', 'Profit', 'Profit_last_tx', 'Wallet']
Config.init_header_csv("RandomBuySellTest.csv", headers)

#-------------------- BUY/SELL RANDOM --------------------
def makeRandomBuyOrSell():
    try:
        BuyPrice, SellPrice = 0, 0
        array_list_prices = Config.get_array_prices(SYMBOL_LIST, EXCHANGE) # Get the prices of the symbols on the exchanges
        portfolio_value = Config.portfolio_value(WALLETBUYSELLRANDOM, SYMBOL_LIST, EXCHANGE) # Get the value of the portfolio
        for list_prices in array_list_prices:
            symbol = list_prices['symbol']
            BuyPrice = Config.buy_token(symbol, list_prices[EXCHANGE[0]], WALLETBUYSELLRANDOM, portfolio_value, SYMBOL_LIST)
            PRICE_DICT[symbol] = BuyPrice
            # For each symbol, we buy it on binance
        Config.wait(5)
        array_list_prices = Config.get_array_prices(SYMBOL_LIST, EXCHANGE) # Get the prices of the symbols on the exchanges
        for list_prices in array_list_prices:
            symbol = list_prices['symbol']
            SellPrice = Config.sell_token(symbol, list_prices[EXCHANGE[0]], WALLETBUYSELLRANDOM)
            Difference = round(SellPrice - PRICE_DICT[symbol], 2)
            if Difference > 0:
                print(f"Difference: +{Difference}")
            else:
                print(f"Difference: {Difference}")
            # For each symbol, we sell it on binance
        # Return the profit and loss of the portfolio
        return Config.get_profit_and_loss(WALLETBUYSELLRANDOM, LIST_AMOUNT_USDT_RANDOM, START_AMOUNT, SYMBOL_LIST, EXCHANGE)
    except Exception as e:
        print("Error in makeRandomBuyOrSell():")
        print(str(e))
        print(traceback.format_exc())

def run_random():
    try:
        Random_Profit_Loss, capital_gain_total, capital_gain_last_tx = makeRandomBuyOrSell()
        print("--------------------------------------------------")
        print(f"Random: {Random_Profit_Loss}")
        return capital_gain_total, capital_gain_last_tx
    except Exception as e:
        print("Error in run_random():")
        print(str(e))
        print(traceback.format_exc())

print("Bot started!") 
while time.time() - START_TIME < SECONS_IN_A_WEEK:
    try:
        NUMBER_OF_TRANSACTION += 1
        TEMPS = time.time() - START_TIME
        print("--------------------------------------------------")
        print(f"{Config.get_time()} - Random - {NUMBER_OF_TRANSACTION} transactions - Execution time : {round(TEMPS, 2)}s\n")
        capital_gain_total, capital_gain_last_tx = run_random()
        Config.write_to_csv("Random", f"Trade {NUMBER_OF_TRANSACTION}", Config.get_time(), Config.get_date(), capital_gain_total, capital_gain_last_tx, WALLETBUYSELLRANDOM, "RandomBuySell.csv")
        Config.wait(60*30)
    except Exception as e:
        print("Error in while loop:")
        print(str(e))
        print(traceback.format_exc())