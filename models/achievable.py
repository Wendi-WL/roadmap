from abc import ABC, abstractmethod

class Achievable(ABC):
    _description : str
    _progress : int
    
    @abstractmethod
    def __init__(self, description):
        if not isinstance(description, (str)):
            raise TypeError("Description should be a string")
        self._description = description
        self._progress = 0

    @property
    def description(self):
        return self._description

    @description.setter
    def description(self, description):
        if not isinstance(description, (str)):
            raise TypeError("Description should be a string")
        self._description = description

    @property
    def progress(self):
        return self._progress
    
    @progress.setter
    def progress(self, progress):
        if not isinstance(progress, (int)):
            raise TypeError("Progress should be an integer")
        elif progress > 10 or progress < 0:
            raise ValueError("Progress should be a value between 0 and 10")
        self._progress = progress