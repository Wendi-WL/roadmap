import pytest
from models.dates import *

d1 = date(2024, 2, 3)
d2 = date(2024, 3, 4)
d3 = date(2024, 3, 2)

@pytest.fixture
def tf():
    return Timeframe(d1, d2)

def test_constructor(tf):
    assert tf.start == d1
    assert tf.end == d2

def test_constructor_typeerror():
    with pytest.raises(TypeError) as excinfo:  
        Timeframe("string", d2) 
    assert str(excinfo.value) == "Start and end should both be dates"
    with pytest.raises(TypeError) as excinfo:  
        Timeframe(d1, 1) 
    assert str(excinfo.value) == "Start and end should both be dates"

def test_set_start(tf):
    tf.start = d3
    assert tf.start == d3

def test_set_start_typeerror(tf):
    with pytest.raises(TypeError) as excinfo:  
        tf.start = 0
    assert str(excinfo.value) == "Start should be a date"

def test_set_end(tf):
    tf.end = d3
    assert tf.end == d3

def test_set_end_typeerror(tf):
    with pytest.raises(TypeError) as excinfo:  
        tf.end = False
    assert str(excinfo.value) == "End should be a date"