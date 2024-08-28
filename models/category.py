class Category():
    """Category with a name"""

    _name : str

    def __init__(self, name):
        if not isinstance(name, (str)):
            raise TypeError("Name should be a string")
        self._name = name

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, name):
        if not isinstance(name, (str)):
            raise TypeError("Name should be a string")
        self._name = name