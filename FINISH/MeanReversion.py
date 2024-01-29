import requests
import time
import pandas as pd
from datetime import datetime, timedelta
import pytz # To have hour in Local zone
import csv
import matplotlib.pyplot as plt
#-------------------- PARAMETRES --------------------

local_tz = pytz.timezone('Europe/Paris')   # Set the timezone to Europe/Paris
BASE_URL = "https://api.binance.com"  # Set the base URL for the Binance API
SYMBOL = ["BTCUSDT","ETHUSDT","BNBUSDT","LTCUSDT","AVAXUSDT"] # Define the list of symbols to work on
INTERVAL = "1s"  # Set the interval for data request from the Binance API
PARAM_BOLLINGER = 2 # Set the parameter for the Bollinger Bands
LIMIT = 1  # Set the limit for data request from the Binance API
START_AMOUNT = 1000000  # Set the starting amount for the USDT wallet
WALLET = { "USDT": START_AMOUNT, "BTCUSDT" : 0, "ETHUSDT" : 0 ,"BNBUSDT" : 0,"LTCUSDT" : 0,"AVAXUSDT" : 0 } # Set up the wallet with the starting amount of USDT and 0 amounts of other cryptocurrencies
SYMBOL_LIST = {"BTCUSDT": 0.5, "ETHUSDT":0.2, "BNBUSDT":0.1, "LTCUSDT":0.1, "AVAXUSDT":0.1} # Set up the list of symbols and the percentage to invest in each cryptocurrency
CRYPTO_GAINS = {"BTCUSDT": [], "ETHUSDT": [], "BNBUSDT": [], "LTCUSDT": [], "AVAXUSDT": []} # Set up a dictionary to keep track of each cryptocurrency gain per transaction 
BOUGHT = {symbol : False for symbol in SYMBOL}  # Set up a dictionary to keep track of whether a cryptocurrency has been bought or not
TRANSAC_COST = 0 #To keep track of transaction's fees
headers = ['Bot', 'Trade', 'Time', 'Date', 'Profit', 'Profit_last_tx', 'Fees', 'Total', 'Wallet']
with open('MeanReversion.csv', 'w', newline='') as file: # Create a new CSV file for trading data and write the headers to the file
    writer = csv.writer(file)
    writer.writerow(headers)

#-------------------- REQUESTS --------------------

def get_request(url):
    try:
        response = requests.get(url) #Ask for data from the given url 
        return response.json() #Return the data as JSON
    except Exception as e:
        print(f"Erreur during URL request : {str(e)}") 

#-------------------- GET DATAFRAME --------------------
#Create a pandas DataFrame with the latest data from the Binance API for a given symbol and interval

def get_dataframe_symbol(symbol, interval, limit):
    try:
        klines_url = f'{BASE_URL}/api/v3/klines?symbol={symbol}&interval={interval}&limit={limit}' # Build the URL for the API request based on the symbol, interval, and limit parameters
        data = get_request(klines_url) #Import the data from the given API
        # Create a pandas DataFrame with the imported data and set the column names
        df = pd.DataFrame(data, columns=["Open time", "Open", "High", "Low", "Close", "Volume", "Close time", "Quote asset volume", "Number of trades", "Taker buy base asset volume", "Taker buy quote asset volume", "Ignore"])
        return df # Return the DataFrame
    except Exception as e:
        print(f"Error creating DataFrame : {str(e)}")


#-------------------- MODIFY DATAFRAME --------------------
# Update the DataFrame by concatenating it with a new DataFrame containing the latest available data

def modify_dataframe(df):
    try:
        df_list=[] # Create an empty list to store DataFrames for each symbol
        for symbol in SYMBOL:   # Create a DataFrame for each symbol in the SYMBOL list
            df1 = get_dataframe_symbol(symbol, INTERVAL, LIMIT)
            df1["Open time"] = pd.to_datetime(df1["Open time"], unit='ms', utc=True) # Convert the "Open time" column to a datetime object and convert to local timezone
            df1["Open time"] = df1["Open time"].dt.tz_convert(local_tz).dt.strftime('%Y-%d-%m %H:%M:%S')
            df1 = df1[["Open time", "Close"]]  # Select only the "Open time" and "Close" columns and add new columns for SMA20, upper, and lower
            df1["SMA20"] = get_sma20(df1)  
            df1["upper"] = get_upper(df1)
            df1["lower"] = get_lower(df1) 
            df1 = df1.astype({'Close':float, "SMA20":float, "upper":float, "lower":float}).round(2)  # Convert the data types of the columns to float and round to 2 decimal places
            df_list.append(df1)
        if df.empty :           # Initialisation : If the original DataFrame is empty, concatenate the list of DataFrames ( containing one dataframe per Symbol ) and return the result
            return pd.concat(df_list, axis=1, keys=SYMBOL) 
        df2=pd.concat(df_list,axis=1,keys=SYMBOL)          # Otherwise, concatenate row by row the list of DataFrames ( containing one dataframe per Symbol ) to the original DataFrame
        df = pd.concat([df,df2], axis=0).reset_index(drop=True)     
        for symbol in SYMBOL:                               # Update SMA20, upper, lower columns for the new dataframe created
            df[(symbol, "SMA20")] = get_sma20(df[symbol])
            df[(symbol, "upper")] = get_upper(df[symbol])
            df[(symbol, "lower")] = get_lower(df[symbol])
        return df   # Return the updated DataFrame
    except Exception as e:
        print(f"Error while modifying DataFrame : {str(e)}")


#------------------- BOLLINGER'S BANDS -----------------
def get_sma20(df):          # Calculates the simple moving average over the last 20 periods
    return df["Close"].rolling(window=20).mean()
def get_ecarttype(df):      # Calculates the standard deviation of the closing prices over the last 20 periods
    return df["Close"].rolling(window=20).std()
#Upper and lower Boolinger Bands Curves
def get_upper(df):          
    return get_sma20(df) + PARAM_BOLLINGER * get_ecarttype(df) # Calculates the upper Bollinger Band using the SMA20 and a multiple of the standard deviation
def get_lower(df):
    return get_sma20(df) - PARAM_BOLLINGER * get_ecarttype(df) # Calculates the lower Bollinger Band using the SMA20 and a multiple of the standard deviation


#-------------------- BUY --------------------
#Buys according to the cryptocurrency given as input a quantity of token based on the percentage chosen in SYMBOL_LIST

def buy_token(symbol, i, df):
    global BOUGHT, WALLET, TRANSAC_COST, CRYPTO_GAINS
    try:
        price = df[symbol]["Close"][i]  # Get the current price of the token
        amountDollars = WALLET["USDT"] * SYMBOL_LIST[symbol]  # Calculate the amount of USDT to spend based on the investment ratio for the token
        transaction_cost = 0.001 * amountDollars  # Calculate the transaction cost based on the amount of USDT being spent (0.1% transaction fee for Binance)
        amountToken = (amountDollars - transaction_cost) / price  # Calculate the amount of token to buy based on the current price
        WALLET["USDT"] -= amountDollars # Subtract the amount of USDT spent from the wallet
        TRANSAC_COST += transaction_cost # Add the transaction cost to the total transaction cost
        try: # Try to add the amount of token purchased to the wallet
            WALLET[f"{symbol}"] += amountToken
        except:
            WALLET[f"{symbol}"] = amountToken
        BOUGHT[symbol] = True # Mark the token as bought 
        CRYPTO_GAINS[symbol].append(amountDollars)  # Record the amount of USDT spent on the token for calculating gains
        # Print information about the purchase
        print(f"Bought {amountToken} {symbol} at price {price} USDT")
        print(f"Transaction cost: {transaction_cost:.2f} USDT")
        print(WALLET)
        print("\n")
    except Exception as e:
        print(f"Error buying {symbol} : {str(e)}")


#-------------------- SELL --------------------
#Sell all the token bought for ​​the symbol given as input

def sell_token(symbol, i, df):
    global BOUGHT, WALLET, TRANSAC_COST, CRYPTO_GAINS
    try:
        price = df[symbol]["Close"][i]  # Get the current price of the token
        amountToken = WALLET[f"{symbol}"]  # Get the amount of the token in the wallet
        transaction_cost = 0.001 * amountToken * price  # Calculate the transaction cost  (0.1% transaction fee for Binance)
        amountDollars = amountToken*price - transaction_cost # Calculate the amount in USDT obtained from selling the token
        WALLET["USDT"] += amountDollars # Add the USDT amount obtained from the selling the token to the wallet
        WALLET[f"{symbol}"] -= amountToken # Remove the sold token from the wallet
        TRANSAC_COST += transaction_cost  # Calculate the total transaction cost
        BOUGHT[symbol] = False # Mark the token as sold
        gain = ((amountDollars / CRYPTO_GAINS[symbol][-1]) - 1) * 100   # Calculate the percentage gain for this token
        CRYPTO_GAINS[symbol][-1] = gain  # Store the percentage gain for this token in the gains list
        # Print the details of the sale
        print(f"Sold {amountToken} {symbol} at the price of {price} USDT")
        print(f"Transaction cost : {transaction_cost:.2f} USDT")
        print(f"Realized gain : {gain:.2f}%")
        print(WALLET)
        print("\n")
    except Exception as e:
        print(f"Error while selling {symbol} : {str(e)}")

#--------------------- AUXILIARY FUNCTIONS -------------------

def total_value(df,index):
    global WALLET, SYMBOL
    # Calculate the total value in USDT
    try:
        usdt_value = WALLET["USDT"]
        crypto_value = 0
        for symbol in SYMBOL: #Calculate for each symbol the total value in USDT and add it in the total    
                crypto_price = df[symbol]["Close"][index] # Get the current price of the crypto
                crypto_amount = WALLET[symbol] # Get the amount of the crypto in the wallet
                crypto_value += crypto_amount * crypto_price # Add the value of the crypto to the total value
        total = crypto_value + usdt_value # Calculate the total value
        return total
    except Exception as e :
        print(f"Error while calculating the total wallet value in USDT : {str(e)}")

def get_plus_value(df,index):
    try:
        return round(total_value(df,index) - START_AMOUNT, 2) # Calculate the difference between the current total value of the wallet and the starting amount
    except Exception as e:
        print(f"Error while retrieving plus value: : {str(e)}")

def get_plus_value_last_tx(df,index):
    try:
            if index == 0: 
                return 0 # If index is 0, df does not exist for index = -1 so the plus value is 0
            return round(total_value(df,index) - total_value(df,index-1), 2) # Otherwise, the plus value is the difference between the current total value and the previous total value
    except Exception as e:
        print(f"Error while retrieving last transaction plus value : {str(e)}")

#-------------------- AFFICHAGE --------------------
#Allows to view the final results of all transactions

def print_wallet_total(df,index):
    global WALLET, TRANSAC_COST, CRYPTO_GAINS
    try:
        usdt_value = WALLET["USDT"]
        total = total_value(df,index)
        crypto_value = total - usdt_value # calculate and print crypto value
        print("\n")
        print(f"Total wallet value in USD : {total:.2f} USD")
        print(f"  - {crypto_value:.2f} USD in cryptocurrencies")
        for symbol in SYMBOL:
            if symbol == "USDT":
                continue
            else:
                crypto_price = df[symbol]["Close"][len(df)-1] # Get the current price of the crypto
                crypto_amount = WALLET[symbol] # Get the amount of the crypto in the wallet
                crypto_value = crypto_amount * crypto_price # Calculate the value of the crypto 
                crypto_symbol = symbol[0:len(symbol)-4] 
                gain_symbol = 0 
                # calculate gain for the crypto
                if BOUGHT[symbol] == False :
                    for i in range (len(CRYPTO_GAINS[symbol])) :
                        gain_symbol =  gain_symbol + CRYPTO_GAINS[symbol][i]
                elif BOUGHT[symbol] == True : 
                    for i in range (len(CRYPTO_GAINS[symbol])-1) :
                        gain_symbol =  gain_symbol + CRYPTO_GAINS[symbol][i]
                elif CRYPTO_GAINS[symbol] == [] :
                        gain_symbol = 0
                # print crypto amount, symbol, crypto value, and gain for each crypto
                print(f"      - {crypto_amount:.8f} {crypto_symbol} ({crypto_value/total*100:.2f}%), Realized gain in percentage: {gain_symbol:.3f}% ")
        # print USDT value and transaction cost
        print(f"  - {usdt_value:.2f} USD in USDT")
        print(f" Transaction cost in USD : {TRANSAC_COST:.2f} USD")
    except Exception as e:
        print(f"Error during results display : {str(e)}")
    
#---------------------- WRITE TO CSV --------------------------

def write_to_csv(bot, trade, heure, date, profit, profit_last_tx, fees, total,wallet):
    data = [bot, trade, heure, date, profit, profit_last_tx, fees, total, wallet]  # create a list with the data to write to the csv file
    with open('MeanReversion.csv', 'a', newline='') as file:  # open the csv file and write the data to it
        writer = csv.writer(file)
        writer.writerow(data)

def get_time():
    #return the time as Hour:Min:Sec
    try:
        return datetime.now(local_tz).strftime('%H:%M:%S')
    except Exception as e:
        print("Error while getting the time: :")
        print(str(e))

def get_date():
    #return the date as Year-Month-Day
    try:
        return datetime.now(local_tz).strftime('%Y-%m-%d')
    except Exception as e:
        print("Error while getting the date:")
        print(str(e))

#-------------------- READ CSV -----------------------------

def plot_profit_over_time(csv_file):
    # Create empty lists to store data
    times = []
    profits = []
    with open(csv_file, 'r') as file: # Open the CSV file and read data row by row
        reader = csv.reader(file)
        next(reader) # skip header row
        for row in reader:
            date_time_str = row[3] + ' ' + row[2] # combine date and time strings 
            date_time_obj = datetime.strptime(date_time_str, '%Y-%m-%d %H:%M:%S') # convert the string to datetime object
            times.append(date_time_obj)
            profits.append(float(row[4]))
    
    plt.plot(times, profits) # Create a line plot of profits over time using matplotlib
    plt.xlabel('Time')
    plt.ylabel('Profit')
    plt.title('Profit over time')
    plt.show()


#-------------------- DECISION MAKING --------------------
#Gives buy and sell orders

def take_decision(df,index):
    global BOUGHT
    if len(df)>=19 : # SMA20, upper and lower are not calculated before the 20th value of the array
        for symbol in SYMBOL:
            # Buy if the token value goes below the lower Bollinger band curve
            if df[symbol]['Close'][index] <= df[symbol]['lower'][index] and BOUGHT[symbol] == False and WALLET["USDT"] != 0 : 
                buy_token(symbol, index, df)
            # Sell if the token value goes above the upper Bollinger band curve
            elif df[symbol]['Close'][index] >= df[symbol]['upper'][index] and BOUGHT[symbol] == True: #On vend si la valeur du token passe au dessus de la courbe supérieur de la bande de Bollinger
                sell_token(symbol, index, df)
            else :
                print(f"No transaction this time for {symbol[:-4]}")
            

def main() : 
    global TRANSAC_COST
    start_time = datetime.now()
    end_time = start_time + timedelta(days=7) # Set the duration of the code to run
    df = pd.DataFrame()
    index = 0
    print("Transactions will begin when the first 20 values have been imported from the API.")
    try:
        while datetime.now() < end_time:
            print("--------------------------------------------------")
            print(datetime.now().strftime('%D %H:%M:%S'))
            print("\n")
            #This code runs in a loop for the interval we have chosen (INTERVAL = "5m")
            df = modify_dataframe(df) # Call modify_dataframe() function to update the dataframe
            take_decision(df,index) # Call take_decision() function to make a buy/sell decision based on the dataframe
            # Write trade details to a CSV file
            write_to_csv("Mean Reversion", f"Trade {index}", get_time(), get_date(), get_plus_value(df,index), get_plus_value_last_tx(df,index), TRANSAC_COST, total_value(df,index), WALLET)
            index = index + 1 # Update the index to the last row of the dataframe
            time.sleep(1) # Wait for 5 minutes to update the dataframe
        print_wallet_total(df,index-1) # Print the wallet and various results after the trading session ends
    except Exception as e:
        print(f"An error occurred : {e}")


main()
plot_profit_over_time('MeanReversion.csv') # Open the CSV containing the trade details and create a line plot of profits over time using matplotlib