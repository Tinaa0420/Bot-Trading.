from datetime import datetime
import matplotlib.pyplot as plt
import csv
import traceback
import os

def plot_profit_over_time(csv_file):
    try:
        if not os.path.exists(csv_file):  # Check if the file exist
            raise Exception(f"File '{csv_file}' does not exist.")
        
        if os.path.getsize(csv_file) == 0:  # Check if the file is empty
            raise Exception(f"File '{csv_file}' is empty.")
        
        file_name = csv_file[:-4]
        
        times = []
        profits = []
        with open(csv_file, 'r') as file:
            reader = csv.reader(file)
            next(reader)
            for row in reader:
                date_time_str = row[3] + ' ' + row[2]
                date_time_obj = datetime.strptime(date_time_str, '%Y-%m-%d %H:%M:%S')
                times.append(date_time_obj)
                profits.append(float(row[4]))
        
        plt.figure(figsize=(10, 6))
        plt.plot(times, profits)
        plt.xlabel('Date')
        plt.ylabel('Profit')
        plt.title(f'Profit over time - {file_name}')
        plt.show()

    except Exception as e:
        print(f"Error during chart display: {str(e)}")
        print(traceback.format_exc())



plot_profit_over_time("Arbitrage999.csv")
plot_profit_over_time("Arbitrage9995.csv")
plot_profit_over_time("RandomBuySell.csv")
plot_profit_over_time("SMA4_10.csv")
plot_profit_over_time("SMA8_21.csv")
plot_profit_over_time("SMA9_20.csv")
plot_profit_over_time("SMA20_50.csv")
