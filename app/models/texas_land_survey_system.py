class TexasLandSurveySystem:
    def __init__(self, 
                 county: str,
                 fips_code: str,
                 abstract: str,
                 block: str,
                 section: str,
                 grantee: str=None,
                 southwest_latitude: float=None,
                 southwest_longitude: float=None,
                 northwest_latitude: float=None,
                 northwest_longitude: float=None,
                 southeast_latitude: float=None,
                 southeast_longitude: float=None,
                 northeast_latitude: float=None,
                 northeast_longitude: float=None
        ):
        self._county = county
        self._fips_code = fips_code
        self._abstract = abstract
        self._block = block
        self._section = section
        self._grantee = grantee
        self._southwest_latitude = southwest_latitude
        self._southwest_longitude = southwest_longitude
        self._northwest_latitude = northwest_latitude
        self._northwest_longitude = northwest_longitude
        self._southeast_latitude = southeast_latitude
        self._southeast_longitude = southeast_longitude
        self._northeast_latitude = northeast_latitude
        self._northeast_longitude = northeast_longitude


    @property
    def county(self):
        return self._county
    
    @property
    def fips_code(self):
        return self._fips_code
    
    @property
    def abstract(self):
        return self._abstract
    
    @property
    def block(self):
        return self._block
    
    @property
    def section(self):
        return self._section
    
    @property
    def grantee(self):
        return self._grantee
    
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




        

