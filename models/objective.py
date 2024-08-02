from models.dates import Timeframe
from models.achievable import Achievable
from models.actionables import *

class Objective(Achievable):
    _timeframe : Timeframe
    _actionables : list[Actionable]
    
    def __init__(self, description, timeframe):
        super().__init__(description)
        if not isinstance(timeframe, (Timeframe)):
            raise TypeError("Timeframe should be a Timeframe")
        self._timeframe = timeframe 
        self._actionables = []
    
    @property
    def timeframe(self):
        return self._timeframe
    
    @timeframe.setter
    def timeframe(self, timeframe):
        if not isinstance(timeframe, (Timeframe)):
            raise TypeError("Timeframe should be a Timeframe")
        self._timeframe = timeframe 

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