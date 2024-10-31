class NewMexicoLandSurveySystem:
    def __init__(self, 
                 township: int,
                 township_direction: str,
                 range: int,
                 range_direction: str,
                 section: int,
                 southwest_latitude: float=None,
                 southwest_longitude: float=None,
                 northwest_latitude: float=None,
                 northwest_longitude: float=None,
                 southeast_latitude: float=None,
                 southeast_longitude: float=None,
                 northeast_latitude: float=None,
                 northeast_longitude: float=None
        ):
        self._township = township
        self._township_direction = township_direction
        self._range = range
        self._range_direction = range_direction
        self._section = section
        self._southwest_latitude = southwest_latitude
        self._southwest_longitude = southwest_longitude
        self._northwest_latitude = northwest_latitude
        self._northwest_longitude = northwest_longitude
        self._southeast_latitude = southeast_latitude
        self._southeast_longitude = southeast_longitude
        self._northeast_latitude = northeast_latitude
        self._northeast_longitude = northeast_longitude


    @property
    def township(self):
        return self._township
    
    @property
    def township_direction(self):
        return self._township_direction
    
    @property
    def range(self):
        return self._range
    
    @property
    def range_direction(self):
        return self._range_direction
    
    @property
    def section(self):
        return self._section
    
    @property
    def southwest_latitude(self):
        return self._southwest_latitude
    
    @property
    def southwest_longitude(self):
        return self._southwest_longitude
    
    @property
    def northwest_latitude(self):
        return self._northwest_latitude
    
    @property
    def northwest_longitude(self):
        return self._northwest_longitude
    
    @property
    def southeast_latitude(self):
        return self._southeast_latitude
    
    @property
    def southeast_longitude(self):
        return self._southeast_longitude
    
    @property
    def northeast_latitude(self):
        return self._northeast_latitude
    
    @property
    def northeast_longitude(self):
        return self._northeast_longitude




        

