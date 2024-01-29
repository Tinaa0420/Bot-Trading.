import pytest
import Config as C

def test_get_date():
    date = C.get_date()
    print(date)
    assert len(date) == 10
    assert isinstance(date, str)
test_get_date()