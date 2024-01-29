def main_SMA(WINDOW_SCALE_1, WINDOW_SCALE_2, name_csv):
    # Author: L2M1
    # Team: L2M1 Trading Bot
    # Teacher: Mme Elodie Roussel
    # Date: 2023 Juanuary - May
    # Numbers of peoples in the team: 4


    import time # To have time.sleep()
    import traceback # To have error in console
    import Config # To have the functions

    EXCHANGE = ["binance", "bybit"]
    START_AMOUNT = 1000000
    WALLETSMA = {"USDT": START_AMOUNT, "BTC": 0, "ETH": 0, "BNB": 0, "LTC": 0, "AVAX": 0}
    SYMBOL_LIST = {"BTC": 0.5, "ETH":0.2, "BNB":0.1, "LTC":0.1, "AVAX":0.1}
    PRICE_DICT = {symbol: {"values": [], "bought": False, "amount": 0} for symbol in SYMBOL_LIST}
    START_TIME = time.time()
    SECONDS_IN_A_WEEK = 7 * 24 * 60 * 60
    NUMBER_OF_TRANSACTION = 0
    POSSIBLE_SMA = False
    ONE_DECISION = False

    headers = ['Bot', 'Trade', 'Time', 'Date', 'Profit', 'Profit_last_tx', 'Wallet']
    Config.init_header_csv(name_csv, headers)

    #-------------------- GET MOVING AVERAGE --------------------
    # Function to get the moving average for a list of prices and a given period
    def get_moving_average(prices, period):
        try:
            return sum(prices[-period:]) / period
        except Exception as e:
            print("Error in get_moving_average():")
            print(str(e))
            print(traceback.format_exc())
    #-------------------- SMA --------------------
    # Main function to make a decision to buy or sell based on moving averages
    def SMA(prices, symbol):
        try:
            global ONE_DECISION
            sma1 = get_moving_average(prices, WINDOW_SCALE_1)
            sma2 = get_moving_average(prices, WINDOW_SCALE_2)
            if not sma1 or not sma2:
                return None, False
            print(f"SMA{WINDOW_SCALE_1}: {round(sma1, 2)}")
            print(f"SMA{WINDOW_SCALE_2}: {round(sma2, 2)}")
            portfolio_value = Config.portfolio_value(WALLETSMA, SYMBOL_LIST, EXCHANGE)
            BOUGHT = PRICE_DICT[symbol]["bought"]
            print(f"Current state: {BOUGHT}")
            if not BOUGHT and sma1 >= sma2:
                print(f"##### Buy signal detected. #####")
                Buy_AmountUSDT = Config.buy_token(symbol, prices[-1], WALLETSMA, portfolio_value, SYMBOL_LIST)
                PRICE_DICT[symbol]["amount"] = Buy_AmountUSDT
                BOUGHT = True
                PRICE_DICT[symbol]["bought"] = BOUGHT
                ONE_DECISION = True
                return None, ONE_DECISION
            elif BOUGHT and sma1 < sma2:
                print(f"***** Sell signal detected. *****")
                Sell_AmountUSDT = Config.sell_token(symbol, prices[-1], WALLETSMA)
                Last_Profit_Loss = Sell_AmountUSDT - PRICE_DICT[symbol]["amount"]
                BOUGHT = False
                PRICE_DICT[symbol]["bought"] = BOUGHT
                print(f"Last Profit/Loss: {Last_Profit_Loss} USDT")
                ONE_DECISION = True
                return Last_Profit_Loss, ONE_DECISION
            else:
                return None, False
        except Exception as e:
            print("Error in SMA()")
            print(str(e))
            print(traceback.format_exc())

    #-------------------- DECISION FUNCTION --------------------
    # Run the SMA function and return the capital gain
    def run_SMA(prices, symbol):
        try:
            Last_Profit_Loss, ONE_DECISION = SMA(prices, symbol)
            if Last_Profit_Loss != None:
                return Last_Profit_Loss, ONE_DECISION
            else:
                return 0, ONE_DECISION
        except Exception as e:
            print("Error in run_SMA()")
            print(str(e))
            print(traceback.format_exc())
    print("Bot started!") 
    while time.time() - START_TIME < SECONDS_IN_A_WEEK:
        try:
            CAPITAL_GAIN_GLOBAL = 0
            array_prices = Config.get_array_prices_sma(SYMBOL_LIST, EXCHANGE, PRICE_DICT)
            ONE_DECISION_AT_LEAST = False
            print("--------------------------------------------------")
            print(f"{Config.get_time()} - SMA [{WINDOW_SCALE_1}/{WINDOW_SCALE_2}] - {NUMBER_OF_TRANSACTION} transactions")
            
            for symbol in SYMBOL_LIST:
                print("--------------------------------------------------")
                print(f"Current price of {symbol}: {array_prices[symbol]['values'][-1]} USDT")
                if len(array_prices[symbol]['values']) >= WINDOW_SCALE_2:
                    Last_Profit_Loss, ONE_DECISION = run_SMA(PRICE_DICT[symbol]['values'], symbol)
                    CAPITAL_GAIN_GLOBAL += Last_Profit_Loss
                    if ONE_DECISION:
                        ONE_DECISION_AT_LEAST = True
                    POSSIBLE_SMA = True
                    
            if ONE_DECISION_AT_LEAST:
                NUMBER_OF_TRANSACTION += 1
            
            if POSSIBLE_SMA:
                if CAPITAL_GAIN_GLOBAL != 0:
                    print(f"Capital gain last: {round(CAPITAL_GAIN_GLOBAL, 2)} USDT")
                print(f"Wallet: {WALLETSMA}")
                capital_gain = Config.get_capital_gain(WALLETSMA, START_AMOUNT, SYMBOL_LIST, EXCHANGE)
                if capital_gain != 0:
                    print(f"SMA Profit/Loss: {capital_gain} USDT")
                if ONE_DECISION_AT_LEAST:
                    Config.write_to_csv(name_csv, f"Trade {NUMBER_OF_TRANSACTION}", Config.get_time(), Config.get_date(), capital_gain, round(CAPITAL_GAIN_GLOBAL, 2), WALLETSMA, name_csv)
                Config.wait(60*30)
            else:
                Config.wait(60*30)
        except Exception as e:
            print("Error in main()")
            print(str(e))
            print(traceback.format_exc())