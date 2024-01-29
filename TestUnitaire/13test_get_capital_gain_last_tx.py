import pytest
import Config as C

def test_get_capital_gain_last_tx():
    wallet = {'BTC': 0.1, 'ETH': 1.0, 'USDT': 1000}
    SYMBOL_LIST = ['BTC', 'ETH']
    EXCHANGE = ['binance', 'bybit']
    START_AMOUNT = 50000
    list_amount_usdt = [1000, 2000, 3000]
    capital_gain_last_tx = C.get_capital_gain_last_tx(wallet, list_amount_usdt, START_AMOUNT, SYMBOL_LIST, EXCHANGE)
    print(capital_gain_last_tx)
    assert capital_gain_last_tx == 1000
test_get_capital_gain_last_tx()