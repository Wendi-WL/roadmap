from abc import ABC, abstractmethod
from datetime import date
from models.category import Category
from models.achievable import Achievable
from models.dates import Phase

class Actionable(ABC):
    """Abstract class: Actionable with a string name and a Category"""

    _name : str
    _category : Category

    @abstractmethod
    def __init__(self, name, category):
        if not isinstance(name, (str)):
            raise TypeError("Name should be a string")
        self._name = name
        if not isinstance(category, (Category)):
            raise TypeError("Category should be a Category")
        self._category = category
        
    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, name):
        if not isinstance(name, (str)):
            raise TypeError("Name should be a string")
        self._name = name

    @property
    def category(self):
        return self._category

    @category.setter
    def category(self, category):
        if not isinstance(category, (Category)):
            raise TypeError("Category should be a Category")
        self._category = category

class Task(Actionable):
    """Concrete implementation of Actionable class: Task with a name, category, due date, and completion status"""

    _due : date
    _completed : bool

    def __init__(self, name, category, due):
        super().__init__(name, category)
        if not isinstance(due, (date)):
            raise TypeError("Due date should be a date")
        self._due = due 
        self._completed = False

    @property
    def due(self):
        return self._due

    @due.setter
    def due(self, due):
        if not isinstance(due, (date)):
            raise TypeError("Due date should be a date")
        self._due = due

    @property
    def completed(self):
        return self._completed

    @completed.setter
    def completed(self, completed):
        if not isinstance(completed, (bool)):
            raise TypeError("Completion status should be a boolean")
        self._completed = completed

class Goal(Actionable, Achievable):
    """Concrete implementation of Actionable, Achievable classes: Goal with a name, category, description, progress, and phase
    
    Can have sub-actionables that are either Tasks or other Goals (accomplished though composite design pattern)
    """

    _phase : Phase
    _subs : list[Actionable]

    def __init__(self, name, category, description, phase):
        super().__init__(name, category)
        Achievable.__init__(self, description) 
        if not isinstance(phase, (Phase)):
            raise TypeError("Phase should be a Phase")
        self._phase = phase
        self._subs = []

    @property
    def phase(self):
        return self._phase

    @phase.setter
    def phase(self, phase):
        if not isinstance(phase, (Phase)):
            raise TypeError("Phase should be a Phase")
        self._phase = phase

    @property
    def subs(self):
        return self._subs

    def get_subs_names_and_types(self):
        """Returns a list of strings that provide the type of sub-actionable and its name"""

        subs_list = []
        for sub in self._subs:
            if isinstance(sub, (Goal)):
                subs_list.append("Goal: " + sub.name)
            elif isinstance(sub, (Task)):
                subs_list.append("Task: " + sub.name)
        return subs_list

    def add_sub(self, sub):
        """Adds a sub-actionable to the list of subs, allowing different objects with duplicate names and types"""

        if not isinstance(sub, (Actionable)):
            raise TypeError("Sub-actionable should be a Goal or Task")
        if sub not in self._subs:
            self._subs.append(sub) 
    
    def remove_sub(self, sub):
        if sub in self._subs:
            self._subs.remove(sub)
