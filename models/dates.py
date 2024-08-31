from datetime import date

class Timeframe():
    """Timeframe with a start date and an end date"""

    _start : date
    _end : date

    def __init__(self, start, end):
        if not isinstance(start, (date)) or not isinstance(end, (date)):
            raise TypeError("Start and end should both be dates")
        if start > end:
            raise ValueError("End date should be on or after the start date")
        self._start = start
        self._end = end
    
    @property
    def start(self):
        return self._start
    
    @start.setter
    def start(self, start):
        if not isinstance(start, (date)):
            raise TypeError("Start should be a date")
        if start > self._end:
            raise ValueError("Start date should be on or before the end date")
        self._start = start

    @property
    def end(self):
        return self._end
    
    @end.setter
    def end(self, end):
        if not isinstance(end, (date)):
            raise TypeError("End should be a date")
        if self._start > end:
            raise ValueError("End date should be on or after the start date")
        self._end = end

class Phase():
    """Phase with a string name and a timeframe"""

    _name : str
    _timeframe : Timeframe

    def __init__(self, name, start, end):
        if not isinstance(name, (str)):
            raise TypeError("Name should be a string")
        self._name = name
        self._timeframe = Timeframe(start, end)
    
    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, name):
        if not isinstance(name, (str)):
            raise TypeError("Name should be a string")
        self._name = name

    @property
    def timeframe(self):
        return self._timeframe
    
    @timeframe.setter
    def timeframe(self, tf):
        if not isinstance(tf, (Timeframe)):
            raise TypeError("Timeframe should be a Timeframe")
        self._timeframe = tf 