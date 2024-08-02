import pytest
from models.category import Category

@pytest.fixture
def c1():
    return Category("cat")

@pytest.fixture
def c2():
    return Category("shorthair")

@pytest.fixture
def c3():
    return Category("siamese")

def test_constructor(c1):
    assert c1.name == "cat"
    assert c1.get_subs_names() == []

def test_constructor_typeerror():
    with pytest.raises(TypeError) as excinfo:  
        Category(1) 
    assert str(excinfo.value) == "Name should be a string"

def test_set_name(c1):
    c1.name = "dog"
    assert c1.name == "dog"

def test_set_name_typeerror(c1):
    with pytest.raises(TypeError) as excinfo:  
        c1.name = False
    assert str(excinfo.value) == "Name should be a string"

def test_add_sub(c1, c2, c3):
    c1.add_sub(c2)
    assert c1.get_subs_names() == ["shorthair"]
    c1.add_sub(c3)
    assert c1.get_subs_names() == ["shorthair", "siamese"]

def test_add_sub_duplicate(c1, c2):
    c1.add_sub(c2)
    c1.add_sub(c2)
    assert c1.get_subs_names() == ["shorthair"]

def test_add_sub_typeerror(c1):
    with pytest.raises(TypeError) as excinfo:  
        c1.add_sub("string")
    assert str(excinfo.value) == "Sub-category should be a Category"

def test_remove_sub(c1, c2):
    c1.add_sub(c2)
    c1.remove_sub(c2)
    assert c1.get_subs_names() == []

def test_remove_sub_nonexistent(c1, c2, c3):
    c1.add_sub(c3)
    c1.remove_sub(c2)
    assert c1.get_subs_names() == ["siamese"]