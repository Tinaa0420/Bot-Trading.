import pytest
import Config as C


def test_get_array_prices():
    SYMBOL_LIST = ["BTC", "ETH"]
    EXCHANGE = ["binance", "bybit"]
    prices = C.get_array_prices(SYMBOL_LIST, EXCHANGE)
    assert isinstance(prices, list)
    assert len(prices) == len(SYMBOL_LIST)
    assert all(isinstance(price, dict) for price in prices)
    for price in prices:
        assert "symbol" in price
        assert price["symbol"] in SYMBOL_LIST
        for exchange in EXCHANGE:
            assert exchange in price
            assert isinstance(price[exchange], float)
# test_get_array_prices()