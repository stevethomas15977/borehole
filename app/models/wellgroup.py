class WellGroup:
    def __init__(self, name:str, color:str, avg_cumoil_per_ft:float=None):
        self._name = name
        self._color = color
        self._avg_cumoil_per_ft = avg_cumoil_per_ft

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

    @property
    def avg_cumoil_per_ft(self):
        return self._avg_cumoil_per_ft
    
    @avg_cumoil_per_ft.setter
    def avg_cumoil_per_ft(self, value):
        self._avg_cumoil_per_ft = value
