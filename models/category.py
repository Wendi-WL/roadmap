class Category():
    _name : str
    _subs : list['Category']

    def __init__(self, name):
        if not isinstance(name, (str)):
            raise TypeError("Name should be a string")
        self._name = name
        self._subs = []

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, name):
        if not isinstance(name, (str)):
            raise TypeError("Name should be a string")
        self._name = name

    def get_subs_names(self):
        subs_list: list[str] = []
        for sub in self._subs:
            subs_list.append(sub.name)
        return subs_list

    def add_sub(self, sub):
        if not isinstance(sub, (Category)):
            raise TypeError("Sub-category should be a Category")
        if sub not in self._subs:
            self._subs.append(sub)

    def remove_sub(self, sub):
        if sub in self._subs:
            self._subs.remove(sub)

