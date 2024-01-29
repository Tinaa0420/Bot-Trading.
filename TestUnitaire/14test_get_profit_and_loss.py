import pytest
import Config as C

def test_get_profit_and_loss():
    START_AMOUNT = 5000
    wallet = {'USDT': START_AMOUNT+1000, 'BTC': 0, 'ETH': 0,}
    SYMBOL_LIST = ['BTC', 'ETH']
    EXCHANGE = ['binance', 'bybit']
    list_amount_usdt = [1000, 2000]
    result = C.get_profit_and_loss(wallet, list_amount_usdt, START_AMOUNT, SYMBOL_LIST, EXCHANGE)
    assert result[0] == 'Gain: +1000.0$ (+4000$)'
test_get_profit_and_loss()
    
    