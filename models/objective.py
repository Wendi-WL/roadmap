from models.dates import date, Timeframe, Phase
from models.category import Category
from models.achievable import Achievable
from models.actionables import Goal

class Objective(Achievable):
    """Concrete implementation of Achievable class: Objective with a description, progress out of 10, and timeframe
    
    Contains three lists of types Category, Phase, and Goal, to store such objects related to the Objective
    """

    _timeframe : Timeframe
    _categories : list[Category]
    _phases : list[Phase]
    _goals : list[Goal]
    
    def __init__(self, description, tf_start, tf_end):
        super().__init__(description)
        if not isinstance(tf_start, (date)) or not isinstance(tf_end, (date)):
            raise TypeError("Start and end dates should be dates")
        self._timeframe = Timeframe(tf_start, tf_end) 
        self._categories = []
        self._phases = []
        self._goals = []
    
    @property
    def timeframe(self):
        return self._timeframe
    
    @timeframe.setter
    def timeframe(self, tf):
        if not isinstance(tf, (Timeframe)):
            raise TypeError("Timeframe should be a Timeframe")
        self._timeframe = tf 
    
    @property
    def categories(self):
        return self._categories

    @property
    def phases(self):
        return self._phases
    
    @property
    def goals(self):
        return self._goals
    
    def get_categories_names(self):
        """Returns a list of strings that provide the names of the Categories of the Objective"""

        cats_list = []
        for cat in self._categories:
            cats_list.append(cat.name)
        return cats_list

    def create_category(self, cat):
        """Adds a Category to the list of Categories, not allowing different objects with duplicate names"""

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
        """Returns a list of strings that provide the names of the Phases in the Objective"""

        phs_list = []
        for ph in self._phases:
            phs_list.append(ph.name)
        return phs_list

    def create_phase(self, ph):
        """Adds a Phase to the list of Phases, ordered by the following criteria:
        - by earliest start date
        - by earlier end date if start date is the same
        - by creation order if start and end dates are the same
        not allowing phases with duplicate names, even if they have different timeframes"""

        if not isinstance(ph, (Phase)):
            raise TypeError("Objective phase should be a Phase")
        if not ph.timeframe.start >= self.timeframe.start or not ph.timeframe.end <= self.timeframe.end:
            raise ValueError("Objective phase must have a Timeframe within the objective timeframe")
        if ph.name in self.get_phases_names():
            raise ValueError("Objective phases must have unique names")
        else: 
            counter = 0
            for phase in self.phases:
                if ph.timeframe.start > phase.timeframe.start:
                    counter += 1
                elif ph.timeframe.start == phase.timeframe.start:
                    if ph.timeframe.end >= phase.timeframe.end:
                        counter += 1
                    else:
                        break
                else:
                    break
            self._phases.insert(counter, ph)

    def delete_phase(self, cat):
        if cat in self._phases:
            self._phases.remove(cat)
    
    def get_goals_names(self):
        goals_list = []
        for goal in self._goals:
            goals_list.append(goal.name)
        return goals_list

    def add_goal(self, goal):
        """Adds a goal to the list, allowing different objects with duplicate names"""

        if not isinstance(goal, (Goal)):
            raise TypeError("Objective goal should be a Goal")
        if goal not in self._goals:
            self._goals.append(goal) 

    def remove_goal(self, goal):
        if goal in self._goals:
            self._goals.remove(goal)