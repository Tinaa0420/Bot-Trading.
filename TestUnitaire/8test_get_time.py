import pytest
import Config as C

def test_get_time():
    time = C.get_time()
    print(time)
    assert len(time) == 8
    assert isinstance(time, str)
test_get_time()