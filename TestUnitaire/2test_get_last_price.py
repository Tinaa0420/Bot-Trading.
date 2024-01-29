import pytest
import Config as C

def test_get_last_price():
    # Test with a valid symbol and exchange
    binance_btc_price = C.get_last_price('binance', "BTC")
    assert isinstance(binance_btc_price, float)
    assert binance_btc_price > 0

    # Test with a different symbol and exchange
    bybit_eth_price = C.get_last_price('bybit', "ETH")
    assert isinstance(bybit_eth_price, float)
    assert bybit_eth_price > 0
    
    # Test with a non-existent symbol and exchange
    invalid_price = C.get_last_price('binance', "XYZ")
    print(f"invalid_price: {invalid_price}")
    assert invalid_price is None
test_get_last_price()