import pytest
from models.dates import *

d1 = date(2024, 2, 3)
d2 = date(2024, 3, 4)
d3 = date(2024, 3, 2)
d4 = date(2024, 3, 6)
d5 = date(2024, 2, 1)

@pytest.fixture
def tf():
    return Timeframe(d1, d2)

def test_constructor(tf):
    assert tf.start == d1
    assert tf.end == d2

def test_constructor_valueerror():
    with pytest.raises(ValueError) as excinfo:
        Timeframe(d2, d3)
    assert str(excinfo.value) == "End date should be on or after the start date"

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

def test_set_start_same_date(tf):
    tf.start = d2
    assert tf.start == d2

def test_set_start_typeerror(tf):
    with pytest.raises(TypeError) as excinfo:  
        tf.start = 0
    assert str(excinfo.value) == "Start should be a date"

def test_set_start_valueerror(tf):
    with pytest.raises(ValueError) as excinfo:  
        tf.start = d4
    assert str(excinfo.value) == "Start date should be on or before the end date"

def test_set_end(tf):
    tf.end = d3
    assert tf.end == d3

def test_set_end_same_date(tf):
    tf.end = d1
    assert tf.start == d1

def test_set_end_typeerror(tf):
    with pytest.raises(TypeError) as excinfo:  
        tf.end = False
    assert str(excinfo.value) == "End should be a date"

def test_set_end_valueerror(tf):
    with pytest.raises(ValueError) as excinfo:  
        tf.end = d5
    assert str(excinfo.value) == "End date should be on or after the start date"