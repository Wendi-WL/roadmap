import pytest
from models.objective import Objective
from models.actionables import Goal, Task
from models.category import Category
from models.dates import *

d1 = date(2024, 2, 3)
d2 = date(2024, 3, 4)
d3 = date(2024, 3, 2)
tf = Timeframe(d1, d2)
new_tf = Timeframe(d1, d3)
c = Category("test category")
p = Phase("test phase", d1, d2)
g = Goal("test goal", c, "test description", p)
dupe_g = Goal("test goal", c, "test description", p)
t = Task("test task", c, d3)
dupe_t = Task("test goal", c, d3)

@pytest.fixture
def obj():
    return Objective("test objective", tf)

def test_constructor(obj):
    assert obj.description == "test objective"
    assert obj.progress == 0
    assert obj.timeframe == tf
    assert obj._actionables == []

def test_constructor_typeerror():
    with pytest.raises(TypeError) as excinfo:  
        Objective(10, tf) 
    assert str(excinfo.value) == "Description should be a string"
    with pytest.raises(TypeError) as excinfo:  
        Objective("String", "Not a timeframe") 
    assert str(excinfo.value) == "Timeframe should be a Timeframe"

def test_set_description(obj):
    obj.description = "New description"
    assert obj.description == "New description"

def test_set_description_typeerror(obj):
    with pytest.raises(TypeError) as excinfo:  
        obj.description = 2
    assert str(excinfo.value) == "Description should be a string"

def test_set_progress(obj):
    obj.progress = 1
    assert obj.progress == 1
    obj.progress = 5
    assert obj.progress == 5
    obj.progress = 10
    assert obj.progress == 10
    obj.progress = 0
    assert obj.progress == 0

def test_set_progress_typeerror(obj):
    with pytest.raises(TypeError) as excinfo:
        obj.progress = "string"
    assert str(excinfo.value) == "Progress should be an integer"

def test_set_progress_valueerror(obj):
    with pytest.raises(ValueError) as excinfo:
        obj.progress = -1
    assert str(excinfo.value) == "Progress should be a value between 0 and 10"
    with pytest.raises(ValueError) as excinfo:
        obj.progress = 11
    assert str(excinfo.value) == "Progress should be a value between 0 and 10"

def test_set_timeframe(obj):
    obj.timeframe = new_tf
    assert obj.timeframe == new_tf

def test_set_timeframe_typeerror(obj):
    with pytest.raises(TypeError) as excinfo:  
        obj.timeframe = d1
    assert str(excinfo.value) == "Timeframe should be a Timeframe"

def test_add_actionable(obj):
    obj.add_actionable(g)
    assert obj.get_actionables_names_and_types() == ["Goal: test goal"]
    obj.add_actionable(t)
    assert obj.get_actionables_names_and_types() == ["Goal: test goal", "Task: test task"]

def test_add_actionable_duplicate_object(obj):
    obj.add_actionable(g)
    obj.add_actionable(g)
    assert obj.get_actionables_names_and_types() == ["Goal: test goal"]

def test_add_actionable_duplicate_diff_object(obj):
    obj.add_actionable(g)
    obj.add_actionable(dupe_t)
    obj.add_actionable(dupe_g)
    assert obj.get_actionables_names_and_types() == ["Goal: test goal", "Task: test goal", "Goal: test goal"]

def test_add_actionable_typeerror(obj):    
    with pytest.raises(TypeError) as excinfo:  
        obj.add_actionable("string")
    assert str(excinfo.value) == "Objective actionable should be a Goal or Task"

def test_remove_actionable(obj):
    obj.add_actionable(g)
    obj.remove_actionable(g)
    assert obj.get_actionables_names_and_types() == []

def test_remove_actionable_nonexistent(obj):
    obj.add_actionable(g)
    obj.remove_actionable(t)
    assert obj.get_actionables_names_and_types() == ["Goal: test goal"]

def test_remove_actionable_duplicate_object(obj):
    obj.add_actionable(g)
    obj.remove_actionable(dupe_g)
    assert obj.get_actionables_names_and_types() == ["Goal: test goal"]