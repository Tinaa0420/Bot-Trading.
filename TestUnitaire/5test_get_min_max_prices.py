import pytest
import Config as C

def test_get_min_max_prices():
    # Test with valid prices
    prices = {'bybit': 50000.0, 'binance': 50100.0}
    min_price, max_price = C.get_min_max_prices(prices)
    assert min_price == 50000.0
    assert max_price == 50100.0

    # Test with equal prices
    prices = {'bybit': 50000.0, 'binance': 50000.0}
    min_price, max_price = C.get_min_max_prices(prices)
    assert min_price == 50000.0
    assert max_price == 50000.0

    # Test with invalid prices
    prices = {'bybit': 'invalid', 'binance': 50000.0}
    min_price, max_price = C.get_min_max_prices(prices)
# test_get_min_max_prices()