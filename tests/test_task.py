import pytest
from models.actionables import Task
from models.category import Category
from datetime import date

c = Category("test category")
d = date(2024, 1, 1)

@pytest.fixture
def t():
    return Task("test task", c, d)

def test_constructor(t):
    assert t.name == "test task"
    assert t.category == c
    assert t.due == d
    assert t.completed == False

def test_constructor_typeerror():
    with pytest.raises(TypeError) as excinfo:  
        Task(0, c, d) 
    assert str(excinfo.value) == "Name should be a string"
    with pytest.raises(TypeError) as excinfo:  
        Task("test task", "not a category", d) 
    assert str(excinfo.value) == "Category should be a Category"
    with pytest.raises(TypeError) as excinfo:  
        Task("test task", c, "not a date") 
    assert str(excinfo.value) == "Due date should be a date"

def test_set_name(t):
    t.name = "new name"
    assert t.name == "new name"

def test_set_name_typeerror(t):
    with pytest.raises(TypeError) as excinfo:  
        t.name = False
    assert str(excinfo.value) == "Name should be a string"

def test_set_category(t):
    new_c = Category("new category")
    t.category = new_c
    assert t.category == new_c

def test_set_category_typeerror(t):
    with pytest.raises(TypeError) as excinfo:  
        t.category = "new category"
    assert str(excinfo.value) == "Category should be a Category"

def test_set_due_date(t):
    new_d = date(2024, 2, 3)
    t.due = new_d
    assert t.due == new_d

def test_set_due_date_typeerror(t):
    with pytest.raises(TypeError) as excinfo:  
        t.due = False
    assert str(excinfo.value) == "Due date should be a date"

def test_set_completion_status(t):
    t.completed = True
    assert t.completed == True

def test_set_completion_status_typeerror(t):
    with pytest.raises(TypeError) as excinfo:  
        t.completed = "not complete"
    assert str(excinfo.value) == "Completion status should be a boolean"