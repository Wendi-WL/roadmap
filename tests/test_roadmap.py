import pytest
from models.roadmap import Roadmap
from models.objective import Objective
from datetime import date

d1 = date(2024, 2, 3)
d2 = date(2024, 3, 4)
o1 = Objective("test", d1, d2)
o2 = Objective("other test", d1, d2)
o3 = Objective("test", d1, d2)

@pytest.fixture
def r():
    return Roadmap()

def test_constructor(r):
    assert r.get_objectives_descriptions() == []

def test_singleton(r):
    r = Roadmap()
    r2 = Roadmap()
    assert r == r2

def test_create_objective(r):
    r.create_objective(o1)
    assert r.get_objectives_descriptions() == ["test"]
    r.create_objective(o2)
    assert r.get_objectives_descriptions() == ["test", "other test"]

def test_create_objective_duplicate_object(r):
    r.create_objective(o1)
    r.create_objective(o1)
    assert r.get_objectives_descriptions() == ["test"]

def test_create_objective_duplicate_diff_object(r):
    r.create_objective(o1)
    r.create_objective(o2)
    r.create_objective(o3)
    assert r.get_objectives_descriptions() == ["test", "other test", "test"]

def test_create_objective_typeerror(r):    
    with pytest.raises(TypeError) as excinfo:  
        r.create_objective("string")
    assert str(excinfo.value) == "Roadmap objective should be an Objective"

def test_delete_objective(r):
    r.create_objective(o1)
    r.delete_objective(o1)
    assert r.get_objectives_descriptions() == []

def test_delete_objective_nonexistent(r):
    r.create_objective(o1)
    r.delete_objective(o2)
    assert r.get_objectives_descriptions() == ["test"]

def test_delete_objective_duplicate_object(r):
    r.create_objective(o1)
    r.delete_objective(o3)
    assert r.get_objectives_descriptions() == ["test"]