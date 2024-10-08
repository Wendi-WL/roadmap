from models.objective import Objective

class Roadmap():
    """Singleton class: Roadmap with a list of Objectives"""

    _objectives : list[Objective]

    def __init__(self):
        self._objectives = []

    def __new__(self):
        if not hasattr(self, 'instance'):
            self.instance = super(Roadmap, self).__new__(self)
        return self.instance
    
    @property
    def objectives(self):
        return self._objectives
    
    def get_objectives_descriptions(self):
        """Returns a list of strings containing the descriptions of the Roadmap's objectives"""

        objectives_list: list[Objective] = []
        for obj in self._objectives:
            objectives_list.append(obj.description)
        return objectives_list

    def create_objective(self, obj):
        if not isinstance(obj, Objective):
            raise TypeError("Roadmap objective should be an Objective")
        if obj not in self._objectives:
            self._objectives.append(obj)
    
    def delete_objective(self, obj):
        if obj in self._objectives:
            self._objectives.remove(obj)

