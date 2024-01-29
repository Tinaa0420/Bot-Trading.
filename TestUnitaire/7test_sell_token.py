import pytest
import Config as C

def test_sell_token():
    symbol = "BTC"
    last_price = 50000
    wallet = {"USDT": 50000, "BTC": 1}
    C.sell_token(symbol, last_price, wallet)
    assert wallet["USDT"] == 100000
    assert wallet["BTC"] == 0
    print(wallet)
test_sell_token()