import pytest
import Config as C

def test_get_capital_gain():
    wallet = {'BTC': 0.1, 'ETH': 1.0, 'USDT': 1000}
    SYMBOL_LIST = ['BTC', 'ETH']
    EXCHANGE = ['binance', 'bybit']
    START_AMOUNT = 5000
    bitcoin = C.get_last_price(EXCHANGE[0], SYMBOL_LIST[0])
    ethereum = C.get_last_price(EXCHANGE[0], SYMBOL_LIST[1])
    total = wallet['USDT'] + wallet['BTC'] * bitcoin + wallet['ETH'] * ethereum
    print(f"total: {round(total, 2)}")
    capital_gain = C.get_capital_gain(wallet, START_AMOUNT, SYMBOL_LIST, EXCHANGE)
    print(f"capital_gain: {capital_gain}")
    assert total - START_AMOUNT == capital_gain or (total - START_AMOUNT - capital_gain < 0 and total - START_AMOUNT - capital_gain > -5) or (total - START_AMOUNT - capital_gain > 0 and total - START_AMOUNT - capital_gain < 5)
    # Explication:
    # First assert: total - START_AMOUNT == capital_gain
    # Second assert: total - START_AMOUNT - capital_gain < 0 and total - START_AMOUNT - capital_gain > -5 (ex: 4999.99 - 5000 = -0.01)
    # Third assert: total - START_AMOUNT - capital_gain > 0 and total - START_AMOUNT - capital_gain < 5 (ex: 5000.01 - 5000 = 0.01)
test_get_capital_gain()