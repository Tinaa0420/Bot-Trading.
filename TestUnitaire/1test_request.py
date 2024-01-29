import pytest
import Config as C

def test_get_request():
    # Test with a valid URL
    URL = "https://api.binance.com/api/v3/ticker/price?symbol=BTCUSDT"
    response = C.get_request(URL)
    print(response['price'])
    assert response['symbol'] == "BTCUSDT"
    
    # Test with a non-existent URL
    NONE_URL = "https://api.binance.com/api/v3/ticker/price?symbol=XYZUSDT"
    response = C.get_request(NONE_URL)
    print(response['msg'])
    assert response['msg'] == "Invalid symbol."
test_get_request()