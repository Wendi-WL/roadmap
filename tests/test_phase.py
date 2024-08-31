import pytest
from models.dates import *

d1 = date(2024, 2, 3)
d2 = date(2024, 3, 4)
d3 = date(2024, 3, 2)

@pytest.fixture
def p():
    return Phase("Phase 1", d1, d2)

def test_constructor(p):
    assert p.name == "Phase 1"
    assert p.timeframe.start == d1
    assert p.timeframe.end == d2

def test_constructor_typeerror():
    with pytest.raises(TypeError) as excinfo:  
        Phase(1, d1, d2)
    assert str(excinfo.value) == "Name should be a string"
    with pytest.raises(TypeError) as excinfo:  
        Phase("Phase 1", "not a date", d2)
    assert str(excinfo.value) == "Start and end should both be dates"
    with pytest.raises(TypeError) as excinfo:  
        Phase("Phase 1", d1, "not a date")
    assert str(excinfo.value) == "Start and end should both be dates"

def test_set_name(p):
    p.name = "1st phase"
    assert p.name == "1st phase"

def test_set_name_typeerror(p):
    with pytest.raises(TypeError) as excinfo:  
        p.name = True
    assert str(excinfo.value) == "Name should be a string"

def test_set_timeframe(p):
    tf = Timeframe(d1, d3)
    p.timeframe = tf
    assert p.timeframe == tf

def test_set_timeframe_typeerror(p):
    with pytest.raises(TypeError) as excinfo:  
        p.timeframe = d1
    assert str(excinfo.value) == "Timeframe should be a Timeframe"