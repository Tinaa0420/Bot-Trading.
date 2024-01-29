import pytest
import Config as C

def test_get_array_prices_sma():
    SYMBOL_LIST = ["BTC", "ETH"]
    EXCHANGE = ["binance", "bybit"]
    PRICE_DICT = {symbol: {"values": [], "bought": False} for symbol in SYMBOL_LIST}
    price_dict = C.get_array_prices_sma(SYMBOL_LIST, EXCHANGE, PRICE_DICT)
    assert isinstance(price_dict, dict)
    assert len(price_dict) == len(SYMBOL_LIST)
    for symbol in SYMBOL_LIST:
        assert symbol in price_dict
        assert "values" in price_dict[symbol]
        assert isinstance(price_dict[symbol]["values"], list)
        assert len(price_dict[symbol]["values"]) == 1
        assert isinstance(price_dict[symbol]["values"][0], float)
# test_get_array_prices_sma()