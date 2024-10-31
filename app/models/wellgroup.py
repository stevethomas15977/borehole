class WellGroup:
    def __init__(self, name:str, color:str):
        self._name = name
        self._color = color

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        self._name = value

    @property
    def color(self):
        return self._color

    @color.setter
    def color(self, value):
        self._color = value
