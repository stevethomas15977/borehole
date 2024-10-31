

class LatitudeLongitudeDistance:
    def __init__(self,
                 reference_api: str,
                 reference_name:str,
                 target_api: str,
                 target_name:str,
                 start_latitude:int=None,
                 start_longitude:int=None,
                 start_z:int=None,
                 start_hypotenuse:int=None,
                 mid_latitude:int=None,
                 mid_longitude:int=None,
                 mid_z:int=None,
                 mid_hypotenuse:int=None,
                 end_latitude:int=None,
                 end_longitude:int=None,
                 end_z:int=None,
                 end_hypotenuse:int=None):
        self._reference_api = reference_api
        self._reference_name = reference_name
        self._target_api = target_api
        self._target_name = target_name
        self._start_latitude = start_latitude
        self._start_longitude = start_longitude
        self._start_z = start_z
        self._start_hypotenuse = start_hypotenuse
        self._mid_latitude = mid_latitude
        self._mid_longitude = mid_longitude
        self._mid_z = mid_z
        self._mid_hypotenuse = mid_hypotenuse
        self._end_latitude = end_latitude
        self._end_longitude = end_longitude
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
    def start_latitude(self):
        return self._start_latitude
    
    @start_latitude.setter
    def start_latitude(self, value):
        self._start_latitude = value

    @property
    def start_longitude(self):
        return self._start_longitude
    
    @start_longitude.setter
    def start_longitude(self, value):
        self._start_longitude = value

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
    def mid_latitude(self):
        return self._mid_latitude
    
    @mid_latitude.setter
    def mid_latitude(self, value):
        self._mid_latitude = value

    @property
    def mid_longitude(self):
        return self._mid_longitude
    
    @mid_longitude.setter
    def mid_longitude(self, value):
        self._mid_longitude = value

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
    def end_latitude(self):
        return self._end_latitude
    
    @end_latitude.setter
    def end_latitude(self, value):
        self._end_latitude = value

    @property
    def end_longitude(self):
        return self._end_longitude
    
    @end_longitude.setter
    def end_longitude(self, value):
        self._end_longitude = value

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
    