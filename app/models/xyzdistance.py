

class XYZDistance:
    def __init__(self,
        reference_api: str=None,
        reference_name: str=None,
        target_api: str=None,
        target_name: str=None,
        start_x: int=None,
        start_y: int=None,
        start_z: int=None,
        start_hypotenuse: int=None,
        mid_x: int=None,
        mid_y: int=None,
        mid_z: int=None,
        mid_hypotenuse: int=None,
        end_x: int=None,
        end_y: int=None,
        end_z: int=None,
        end_hypotenuse: int =None):

        self._reference_api = reference_api
        self._reference_name = reference_name
        self._target_api = target_api
        self._target_name = target_name
        self._start_x = start_x
        self._start_y = start_y
        self._start_z = start_z
        self._start_hypotenuse = start_hypotenuse
        self._mid_x = mid_x
        self._mid_y = mid_y
        self._mid_z = mid_z
        self._mid_hypotenuse = mid_hypotenuse
        self._end_x = end_x
        self._end_y = end_y
        self._end_z = end_z
        self._end_hypotenuse = end_hypotenuse

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
    def start_x(self):
        return self._start_x
    
    @start_x.setter
    def start_x(self, value):
        self._start_x = value

    @property
    def start_y(self):
        return self._start_y
    
    @start_y.setter
    def start_y(self, value):
        self._start_y = value

    @property
    def start_z(self):
        return self._start_z
    
    @start_z.setter
    def start_z(self, value):
        self._start_z = value
    
    @property
    def start_hypotenuse(self):
        return self._start_hypotenuse
    
    @start_hypotenuse.setter
    def start_hypotenuse(self, value):
        self._start_hypotenuse = value

    @property
    def mid_x(self):
        return self._mid_x
    
    @mid_x.setter
    def mid_x(self, value):
        self._mid_x = value

    @property
    def mid_y(self):
        return self._mid_y
    
    @mid_y.setter
    def mid_y(self, value):
        self._mid_y = value

    @property
    def mid_z(self):
        return self._mid_z
    
    @mid_z.setter
    def mid_z(self, value):
        self._mid_z = value

    @property
    def mid_hypotenuse(self):
        return self._mid_hypotenuse
    
    @mid_hypotenuse.setter
    def mid_hypotenuse(self, value):
        self._mid_hypotenuse = value

    @property
    def end_x(self):
        return self._end_x
    
    @end_x.setter
    def end_x(self, value):
        self._end_x = value

    @property
    def end_y(self):
        return self._end_y
    
    @end_y.setter
    def end_y(self, value):
        self._end_y = value

    @property
    def end_z(self):
        return self._end_z
    
    @end_z.setter
    def end_z(self, value):
        self._end_z = value
    
    @property
    def end_hypotenuse(self):
        return self._end_hypotenuse
    
    @end_hypotenuse.setter
    def end_hypotenuse(self, value):
        self._end_hypotenuse = value
    