import pytest
import Config as C

def test_buy_token():
    symbol = "BTC"
    last_price = 50000
    wallet = {"USDT": 100000}
    amountUSDT = wallet["USDT"]
    SYMBOL_LIST = {"BTC": 0.5}
    C.buy_token(symbol, last_price, wallet, amountUSDT, SYMBOL_LIST)
    assert wallet["USDT"] == 50000
    assert wallet["BTC"] == 1
test_buy_token()