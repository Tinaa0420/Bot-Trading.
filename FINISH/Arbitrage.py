def main(LIMIT_ARBITRAGE, name_csv):
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
    WALLETARBITRAGE = {"USDT": START_AMOUNT, "BTC": 0, "ETH": 0, "BNB": 0, "LTC": 0, "AVAX": 0}
    SYMBOL_LIST = {"BTC": 0.5, "ETH":0.2, "BNB":0.1, "LTC":0.1, "AVAX":0.1}
    START_TIME = time.time()
    SECONDS_IN_A_WEEK = 7 * 24 * 60 * 60 
    LIST_AMOUNT_USDT_ARBITRAGE = []
    NUMBER_OF_TRANSACTION = 0

    headers = ['Bot', 'Trade', 'Time', 'Date', 'Profit', 'Profit_last_tx', 'Wallet']
    Config.init_header_csv(name_csv, headers)     

    #-------------------- ARBITRAGE --------------------
    # Return the list of dictionaries with the prices of each symbol
    def arbitrage():
        try:
            ONE_ARBITRAGE_AT_LEAST = False
            array_list_prices = Config.get_array_prices(SYMBOL_LIST, EXCHANGE)
            portfolio_value = Config.portfolio_value(WALLETARBITRAGE, SYMBOL_LIST, EXCHANGE)
            for list_prices in array_list_prices:
                symbol = list_prices['symbol']
                min_prices, max_prices = Config.get_min_max_prices(list_prices)
                try:
                    if min_prices < max_prices*LIMIT_ARBITRAGE: 
                        print(f"Symbol: {symbol} - Min: {min_prices} - Max: {max_prices}\nArbitrage possible! ==> difference: {round((max_prices-min_prices), 2)}$")
                        Config.buy_token(symbol, min_prices, WALLETARBITRAGE, portfolio_value, SYMBOL_LIST)
                        
                    else:
                        print(f"Symbol: {symbol} - Min: {min_prices} - Max: {max_prices}\nNo arbitrage possible! XXXXX\nDifference: {round((max_prices-min_prices), 2)}$ < min_diff: {round((max_prices*(1-LIMIT_ARBITRAGE)), 2)}$\n")
                except Exception as e:
                    print("Error in arbitrage() - 1st loop:")
                    print(min_prices, max_prices)
                    print(str(e))
            Config.wait(5)
            array_list_prices = Config.get_array_prices(SYMBOL_LIST, EXCHANGE)
            for list_prices in array_list_prices:
                symbol = list_prices['symbol']
                min_prices, max_prices = Config.get_min_max_prices(list_prices)
                try:
                    if WALLETARBITRAGE[symbol] > 0:
                        Config.sell_token(symbol, max_prices, WALLETARBITRAGE)
                        ONE_ARBITRAGE_AT_LEAST = True
                except Exception as e:
                    print("Error in arbitrage() - 2nd loop:")
                    print(str(e))
            if ONE_ARBITRAGE_AT_LEAST:
                return *Config.get_profit_and_loss(WALLETARBITRAGE, LIST_AMOUNT_USDT_ARBITRAGE, START_AMOUNT, SYMBOL_LIST, EXCHANGE), True
            else:
                return *Config.get_profit_and_loss(WALLETARBITRAGE, LIST_AMOUNT_USDT_ARBITRAGE, START_AMOUNT, SYMBOL_LIST, EXCHANGE), False
        except Exception as e:
            print("Error in arbitrage():")
            print(str(e))
            print(traceback.format_exc())
            
    # Main function
    def run_arbitrage():
        try:
            Arbitrage_Profit_Loss, capital_gain_total, capital_gain_last_tx, ONE_ARBITRAGE_AT_LEAST = arbitrage() # We perform arbitrage
            if ONE_ARBITRAGE_AT_LEAST:
                print(f"Arbitrage: {Arbitrage_Profit_Loss}")
            print("--------------------------------------------------")
            return capital_gain_total, capital_gain_last_tx, ONE_ARBITRAGE_AT_LEAST
        except Exception as e:
            print("Error in run_arbitrage():")
            print(str(e))
            print(traceback.format_exc())

    print("Bot started!") 
    while time.time() - START_TIME < SECONDS_IN_A_WEEK:
        try:
            NUMBER_OF_TRANSACTION += 1
            TIME = time.time() - START_TIME
            print("--------------------------------------------------")
            print(f"{Config.get_time()} - Arbitrage[{LIMIT_ARBITRAGE}] - {NUMBER_OF_TRANSACTION} transactions - Execution time: {round(TIME, 2)}s\n")
            ONE_ARBITRAGE_AT_LEAST = False
            NUMBER_OF_RETRY = 0
            while not ONE_ARBITRAGE_AT_LEAST:
                capital_gain_total, capital_gain_last_tx, ONE_ARBITRAGE_AT_LEAST = run_arbitrage()
                if ONE_ARBITRAGE_AT_LEAST:
                    Config.write_to_csv(f"Arbitrage[{LIMIT_ARBITRAGE}]", f"Trade {NUMBER_OF_TRANSACTION}", Config.get_time(), Config.get_date(), capital_gain_total, capital_gain_last_tx, WALLETARBITRAGE, name_csv)
                    Config.wait(60*30) # Wait 1 min
                else:
                    NUMBER_OF_RETRY += 1
                    Config.wait(60/2) 
                    print("--------------------------------------------------")
                    print(f"{Config.get_time()} - Number of retries: {NUMBER_OF_RETRY}\n")
        except Exception as e:
            print("Error in main():")
            print(str(e))
            print(traceback.format_exc())