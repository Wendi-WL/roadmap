from models.dates import Timeframe
from models.achievable import Achievable
from models.actionables import *

class Objective(Achievable):
    """Concrete implementation of Achievable class: Objective with a description, progress out of 10, and timeframe
    
    Contains three lists of types Category, Phase, and Actionable, to store such objects related to the Objective
    """

    _timeframe : Timeframe
    _categories : list[Category]
    _phases : list[Phase]
    _actionables : list[Actionable]
    
    def __init__(self, description, tf_start, tf_end):
        super().__init__(description)
        if not isinstance(tf_start, (date)) or not isinstance(tf_end, (date)):
            raise TypeError("Start and end dates should be dates")
        self._timeframe = Timeframe(tf_start, tf_end) 
        self._categories = []
        self._phases = []
        self._actionables = []
    
    @property
    def timeframe(self):
        return self._timeframe
    
    @timeframe.setter
    def timeframe(self, tf):
        if not isinstance(tf, (Timeframe)):
            raise TypeError("Timeframe should be a Timeframe")
        self._timeframe = tf 

    def get_categories_names(self):
        cats_list = []
        for cat in self._categories:
            cats_list.append(cat.name)
        return cats_list

    def create_category(self, cat):
        if not isinstance(cat, (Category)):
            raise TypeError("Objective category should be a Category")
        if cat.name in self.get_categories_names(): 
            raise ValueError("Objective categories must have unique names")
        else:
            self._categories.append(cat)

    def delete_category(self, cat):
        if cat in self._categories:
            self._categories.remove(cat)

    def get_phases_names(self):
        phs_list = []
        for ph in self._phases:
            phs_list.append(ph.name)
        return phs_list

    def create_phase(self, ph):
        if not isinstance(ph, (Phase)):
            raise TypeError("Objective phase should be a Phase")
        if not ph.start >= self.timeframe.start or not ph.end <= self.timeframe.end:
            raise ValueError("Objective phase must have a timeframe within the objective timeframe")
        if ph.name in self.get_phases_names():
            raise ValueError("Objective phases must have unique names")
        else: 
            self._phases.append(ph)

    def delete_phase(self, cat):
        if cat in self._phases:
            self._phases.remove(cat)
    
    def get_actionables_names_and_types(self):
        acts_list = []
        for act in self._actionables:
            if isinstance(act, (Goal)):
                acts_list.append("Goal: " + act.name)
            elif isinstance(act, (Task)):
                acts_list.append("Task: " + act.name)
        return acts_list

    def add_actionable(self, act):
        if not isinstance(act, (Actionable)):
            raise TypeError("Objective actionable should be a Goal or Task")
        if act not in self._actionables:
            self._actionables.append(act) #allows add as long as it's a new object, even if it has same name and type

    def remove_actionable(self, act):
        if act in self._actionables:
            self._actionables.remove(act)