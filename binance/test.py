import requests, time
import pandas as pd
from datetime import datetime

BASE_URL = "https://api.binance.com"
SYMBOL = "BTCUSDT"
INTERVAL = "1d"
LIMIT = "100"   

def get_request(url):
    response = requests.get(url)
    return response.json()
def get_dataframe_symbol(symbol):
    klines_url = f"{BASE_URL}/api/v3/klines?symbol={symbol}&interval={INTERVAL}&limit={LIMIT}"
    data = get_request(klines_url)
    df = pd.DataFrame(data, columns=["Open time", "Open", "High", "Low", "Close", "Volume", "Close time", "Quote asset volume", "Number of trades", "Taker buy base asset volume", "Taker buy quote asset volume", "Ignore"])
    return df

df = get_dataframe_symbol(SYMBOL)
df = df[["Open time", "Open", "Close"]]
df["Open time"] = pd.to_datetime(df["Open time"], unit='ms')
df["Open"] = df["Open"].astype(float).round(2)
df["Close"] = df["Close"].astype(float).round(2)
df["SMA"] = df["Close"].rolling(10).mean().astype(float).round(2)
# .apply(lambda x: f"moy {x:.2f}")

df = df.tail(10)
print(df)