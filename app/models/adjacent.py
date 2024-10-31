

class Adjacent:
    def __init__(self, 
                 reference_api: str,
                 reference_name:str, 
                 target_api: str,
                 target_name:str, 
                 north=None, 
                 south=None, 
                 east=None, 
                 west=None,
                 hypotenuse=None):
        
        self._reference_api = reference_api
        self._target_api = target_api
        self._reference_name = reference_name
        self._target_name = target_name
        self._north = north
        self._south = south
        self._east = east
        self._west = west
        self._hypotenuse = hypotenuse

    @property
    def reference_api(self):
        return self._reference_api
    
    @reference_api.setter
    def reference_api(self, value):
        self._reference_api = value

    @property
    def reference_name(self):
        return self._reference_name

    @reference_name.setter
    def reference_name(self, value):
        self._reference_name = value

    @property
    def target_api(self):
        return self._target_api
    
    @target_api.setter
    def target_api(self, value):
        self._target_api = value
        
    @property
    def target_name(self):
        return self._target_name

    @target_name.setter
    def target_name(self, value):
        self._target_name = value

    @property
    def north(self):
        return self._north

    @north.setter
    def north(self, value):
        self._north = value

    @property
    def south(self):
        return self._south

    @south.setter
    def south(self, value):
        self._south = value

    @property
    def east(self):
        return self._east

    @east.setter
    def east(self, value):
        self._east = value

    @property
    def west(self):
        return self._west

    @west.setter
    def west(self, value):
        self._west = value

    @property
    def hypotenuse(self):
        return self._hypotenuse
    
    @hypotenuse.setter
    def hypotenuse(self, value):
        self._hypotenuse = value