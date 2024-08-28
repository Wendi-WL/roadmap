import pytest
from models.category import Category

@pytest.fixture
def c():
    return Category("cat")

def test_constructor(c):
    assert c.name == "cat"

def test_constructor_typeerror():
    with pytest.raises(TypeError) as excinfo:  
        Category(1) 
    assert str(excinfo.value) == "Name should be a string"

def test_set_name(c):
    c.name = "dog"
    assert c.name == "dog"

def test_set_name_typeerror(c):
    with pytest.raises(TypeError) as excinfo:  
        c.name = False
    assert str(excinfo.value) == "Name should be a string"