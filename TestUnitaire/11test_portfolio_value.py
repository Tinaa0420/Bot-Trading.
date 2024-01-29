import pytest
import Config as C

def test_portfolio_value():
    wallet = {'USDT': 1000, 'BTC': 0.1, 'ETH': 1.0, }
    SYMBOL_LIST = ['BTC', 'ETH']
    EXCHANGE = ['binance', 'bybit']
    bitcoin = C.get_last_price(EXCHANGE[0], SYMBOL_LIST[0])
    ethereum = C.get_last_price(EXCHANGE[0], SYMBOL_LIST[1])
    value_portfolio = C.portfolio_value(wallet, SYMBOL_LIST, EXCHANGE)
    print(value_portfolio)
    total = wallet['USDT'] + wallet['BTC'] * bitcoin + wallet['ETH'] * ethereum
    print(total)
    assert value_portfolio - total == 0 or (value_portfolio - total < 0 and value_portfolio - total > -5) or (value_portfolio - total > 0 and value_portfolio - total < 5)
test_portfolio_value()