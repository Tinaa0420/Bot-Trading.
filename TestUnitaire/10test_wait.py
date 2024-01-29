import pytest
import Config as C
import time

def test_wait():
    timer = 5
    start_time = time.time()
    C.wait(timer)
    end_time = time.time()
    elapsed_time = end_time - start_time
    print(elapsed_time)
    assert elapsed_time >= timer
test_wait()