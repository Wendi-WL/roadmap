import pytest
from models.actionables import Goal, Task
from models.category import Category
from models.dates import date, Phase

c = Category("test category")
d1 = date(2024, 1, 1)
d2 = date(2024, 2, 2)
p = Phase("test phase", d1, d2)
sub_g = Goal("sub goal", c, "a sub goal", p)
dupe_sub_g = Goal("sub goal", c, "a sub goal", p)
t = Task("test task", c, d1)

@pytest.fixture
def g():
    return Goal("test goal", c, "test description", p)

def test_constructor(g):
    assert g.name == "test goal"
    assert g.category == c
    assert g.description == "test description"
    assert g.progress == 0
    assert g.phase == p

def test_constructor_typeerror():
    with pytest.raises(TypeError) as excinfo:  
        Goal(0, c, "test description", p)
    assert str(excinfo.value) == "Name should be a string"
    with pytest.raises(TypeError) as excinfo:  
        Goal("test goal", "not a category", "test description", p)
    assert str(excinfo.value) == "Category should be a Category"
    with pytest.raises(TypeError) as excinfo:  
        Goal("test goal", c, 1, p)
    assert str(excinfo.value) == "Description should be a string"
    with pytest.raises(TypeError) as excinfo:  
        Goal("test goal", c, "test description", "not a phase")
    assert str(excinfo.value) == "Phase should be a Phase"

def test_set_name(g):
    g.name = "new name"
    assert g.name == "new name"

def test_set_name_typeerror(g):
    with pytest.raises(TypeError) as excinfo:  
        g.name = False
    assert str(excinfo.value) == "Name should be a string"

def test_set_category(g):
    new_c = Category("new category")
    g.category = new_c
    assert g.category == new_c

def test_set_category_typeerror(g):
    with pytest.raises(TypeError) as excinfo:  
        g.category = "new category"
    assert str(excinfo.value) == "Category should be a Category"

def test_set_description(g):
    g.description = "New description"
    assert g.description == "New description"

def test_set_description_typeerror(g):
    with pytest.raises(TypeError) as excinfo:  
        g.description = 2
    assert str(excinfo.value) == "Description should be a string"

def test_set_progress(g):
    g.progress = 1
    assert g.progress == 1
    g.progress = 5
    assert g.progress == 5
    g.progress = 10
    assert g.progress == 10
    g.progress = 0
    assert g.progress == 0

def test_set_progress_typeerror(g):
    with pytest.raises(TypeError) as excinfo:
        g.progress = "string"
    assert str(excinfo.value) == "Progress should be an integer"

def test_set_progress_valueerror(g):
    with pytest.raises(ValueError) as excinfo:
        g.progress = -1
    assert str(excinfo.value) == "Progress should be a value between 0 and 10"
    with pytest.raises(ValueError) as excinfo:
        g.progress = 11
    assert str(excinfo.value) == "Progress should be a value between 0 and 10"

def test_set_phase(g):
    new_p = Phase("new phase", d1, d2)
    g.phase = new_p
    assert g.phase == new_p

def test_set_phase_typeerror(g):
    with pytest.raises(TypeError) as excinfo:  
        g.phase = "not a phase"
    assert str(excinfo.value) == "Phase should be a Phase"

def test_add_sub(g):
    g.add_sub(sub_g)
    assert g.get_subs_names_and_types() == ["Goal: sub goal"]
    g.add_sub(t)
    assert g.get_subs_names_and_types() == ["Goal: sub goal", "Task: test task"]

def test_add_sub_duplicate_object(g):
    g.add_sub(sub_g)
    g.add_sub(sub_g)
    assert g.get_subs_names_and_types() == ["Goal: sub goal"]

def test_add_sub_duplicate_diff_object(g):
    g.add_sub(sub_g)
    g.add_sub(t)
    g.add_sub(dupe_sub_g)
    assert g.get_subs_names_and_types() == ["Goal: sub goal", "Task: test task", "Goal: sub goal"]

def test_add_sub_typeerror(g):    
    with pytest.raises(TypeError) as excinfo:  
        g.add_sub("string")
    assert str(excinfo.value) == "Sub-actionable should be a Goal or Task"

def test_remove_sub(g):
    g.add_sub(sub_g)
    g.remove_sub(sub_g)
    assert g.get_subs_names_and_types() == []

def test_remove_sub_nonexistent(g):
    g.add_sub(sub_g)
    g.remove_sub(t)
    assert g.get_subs_names_and_types() == ["Goal: sub goal"]

def test_remove_sub_duplicate_object(g):
    g.add_sub(sub_g)
    g.remove_sub(dupe_sub_g)
    assert g.get_subs_names_and_types() == ["Goal: sub goal"]