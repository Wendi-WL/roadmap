import pytest
from models.objective import Objective
from models.actionables import Goal
from models.category import Category
from models.dates import *

d1 = date(2024, 2, 3)
d2 = date(2024, 3, 4)
d3 = date(2024, 3, 2)
d4 = date(2024, 3, 6)
d5 = date(2024, 2, 1)
d6 = date(2024, 3, 3)
c = Category("test category")
p = Phase("test phase", d1, d2)
p_5 = Phase("1", d1, d3)
p_4 = Phase("2", d3, d3)
p_1 = Phase("3", d3, d6)
p_3 = Phase("4", d3, d6)
p_2 = Phase("5", d3, d2)
p_6 = Phase("6", d6, d6)
g = Goal("test goal", c, "test description", p)
dupe_g = Goal("test goal", c, "test description", p)
g2 = Goal("2", c, "test description", p)
g3 = Goal("test goal", c, "different phase", p_1)

@pytest.fixture
def obj():
    return Objective("test objective", d1, d2)

def test_constructor(obj):
    assert obj.description == "test objective"
    assert obj.progress == 0
    assert obj.timeframe.start == d1
    assert obj.timeframe.end == d2
    assert obj.categories == []
    assert obj.phases == []
    assert obj.goals == []

def test_constructor_same_dates():
    same_date_obj = Objective("test objective", d1, d1)
    assert same_date_obj.description == "test objective"
    assert same_date_obj.progress == 0
    assert same_date_obj.timeframe.start == d1
    assert same_date_obj.timeframe.end == d1
    assert same_date_obj.categories == []
    assert same_date_obj.phases == []
    assert same_date_obj.goals == []

def test_constructor_typeerror():
    with pytest.raises(TypeError) as excinfo:  
        Objective(10, d1, d2) 
    assert str(excinfo.value) == "Description should be a string"
    with pytest.raises(TypeError) as excinfo:  
        Objective("String", "Not a date", d2) 
    assert str(excinfo.value) == "Start and end dates should be dates"
    with pytest.raises(TypeError) as excinfo:  
        Objective("String", d1, "Not a date") 
    assert str(excinfo.value) == "Start and end dates should be dates"

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
    tf = Timeframe(d1, d3)
    obj.timeframe = tf
    assert obj.timeframe == tf

def test_set_timeframe_typeerror(obj):
    with pytest.raises(TypeError) as excinfo:  
        obj.timeframe = d1
    assert str(excinfo.value) == "Timeframe should be a Timeframe"

def test_create_category(obj):
    obj.create_category(c)
    assert obj.get_categories_names() == ["test category"]

def test_create_category_typeerror(obj):
    with pytest.raises(TypeError) as excinfo:  
        obj.create_category("not a category")
    assert str(excinfo.value) == "Objective category should be a Category"    

def test_create_category_valueerror(obj):
    obj.create_category(c)
    c_dupe = Category("test category")
    with pytest.raises(ValueError) as excinfo:  
        obj.create_category(c_dupe)
    assert str(excinfo.value) == "Objective categories must have unique names"

def test_delete_category(obj):
    obj.create_category(c)
    obj.delete_category(c)
    assert obj.get_categories_names() == []

def test_create_phase(obj):
    obj.create_phase(p)
    assert obj.get_phases_names() == ["test phase"]

def test_create_phase_sorting(obj):
    obj.create_phase(p_1)
    obj.create_phase(p_2)
    obj.create_phase(p_3)
    obj.create_phase(p_4)
    obj.create_phase(p_5)
    obj.create_phase(p_6)
    assert obj.get_phases_names() == ["1", "2", "3", "4", "5", "6"]

def test_create_phase_typeerror(obj):
    with pytest.raises(TypeError) as excinfo:  
        obj.create_phase("not a phase")
    assert str(excinfo.value) == "Objective phase should be a Phase"

def test_create_phase_valueerror(obj):
    obj.create_phase(p)
    p_start_out_of_range = Phase("end out of range phase", d5, d1)
    with pytest.raises(ValueError) as excinfo:  
        obj.create_phase(p_start_out_of_range)
    assert str(excinfo.value) == "Objective phase must have a Timeframe within the objective timeframe" 
    p_end_out_of_range = Phase("end out of range phase", d1, d4)
    with pytest.raises(ValueError) as excinfo:  
        obj.create_phase(p_end_out_of_range)
    assert str(excinfo.value) == "Objective phase must have a Timeframe within the objective timeframe" 
    p_dupe = Phase("test phase", d1, d3)
    with pytest.raises(ValueError) as excinfo:  
        obj.create_phase(p_dupe)
    assert str(excinfo.value) == "Objective phases must have unique names"

def test_delete_phase(obj):
    obj.create_phase(p)
    obj.delete_phase(p)
    assert obj.get_phases_names() == []

def test_add_goal(obj):
    obj.add_goal(g)
    assert obj.get_goals_names() == ["test goal"]
    obj.add_goal(g2)
    assert obj.get_goals_names() == ["test goal", "2"]

def test_add_goal_duplicate_object(obj):
    obj.add_goal(g)
    obj.add_goal(g)
    assert obj.get_goals_names() == ["test goal"]

def test_add_goal_duplicate_diff_object(obj):
    obj.add_goal(g)
    obj.add_goal(g3)
    obj.add_goal(dupe_g)
    assert obj.get_goals_names() == ["test goal", "test goal", "test goal"]

def test_add_goal_typeerror(obj):    
    with pytest.raises(TypeError) as excinfo:  
        obj.add_goal("string")
    assert str(excinfo.value) == "Objective goal should be a Goal"

def test_remove_goal(obj):
    obj.add_goal(g)
    obj.remove_goal(g)
    assert obj.get_goals_names() == []

def test_remove_goal_nonexistent(obj):
    obj.add_goal(g)
    obj.remove_goal(g2)
    assert obj.get_goals_names() == ["test goal"]

def test_remove_goal_duplicate_object(obj):
    obj.add_goal(g)
    obj.remove_goal(dupe_g)
    assert obj.get_goals_names() == ["test goal"]