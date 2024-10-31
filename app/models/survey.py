class Survey:
    def __init__(self, api, station, md, inclination, azimuth, latitude, longitude, grid_x, grid_y, subsurface_depth):
        self._api = api
        self._station = station
        self._md = md
        self._inclination = inclination
        self._azimuth = azimuth
        self._latitude = latitude
        self._longitude = longitude
        self._grid_x = grid_x
        self._grid_y = grid_y
        self._subsurface_depth = subsurface_depth

    @property
    def api(self):
        return self._api

    @api.setter
    def api(self, value):
        self._api = value

    @property
    def station(self):
        return self._station

    @station.setter
    def station(self, value):
        self._station = value

    @property
    def md(self):
        return self._md

    @md.setter
    def md(self, value):
        self._md = value

    @property
    def inclination(self):
        return self._inclination

    @inclination.setter
    def inclination(self, value):
        self._inclination = value

    @property
    def azimuth(self):
        return self._azimuth

    @azimuth.setter
    def azimuth(self, value):
        self._azimuth = value

    @property
    def latitude(self):
        return self._latitude

    @latitude.setter
    def latitude(self, value):
        self._latitude = value

    @property
    def longitude(self):
        return self._longitude

    @longitude.setter
    def longitude(self, value):
        self._longitude = value

    @property
    def grid_x(self):
        return self._grid_x
    
    @grid_x.setter
    def grid_x(self, value):
        self._grid_x = value

    @property
    def grid_y(self):
        return self._grid_y
    
    @grid_y.setter
    def grid_y(self, value):
        self._grid_y = value

    @property
    def subsurface_depth(self):
        return self._subsurface_depth
    
    @subsurface_depth.setter
    def subsurface_depth(self, value):
        self._subsurface_depth = value

    def __str__(self):
        return f"""Survey(id={self._api}, 
        station={self._station}, 
        md={self._md}, 
        inclination={self._inclination}, 
        azimuth={self._azimuth}, 
        latitude={self._latitude}, 
        longitude={self._longitude},
        grid_x={self._grid_x},
        subsurface_depth={self._subsurface_depth})"""
