from operator import le


class Well:
    def __init__(
        self,
        api:str=None,
        name:str=None,
        direction:str=None,
        operator:str=None,
        status:str=None,
        lease:str=None,
        interval:str=None,
        formation:str=None,
        first_production_date:str=None,
        surface_latitude:float=0,
        surface_longitude:float=0,
        bottom_hole_latitude:float=0,
        bottom_hole_longitude:float=0,
        total_vertical_depth:int=0,
        measured_depth:int=0,
        kelly_bushing_elevation:int=0,
        lateral_length:int=0,
        perf_interval:int=0,
        proppant_intensity:int=0,
        state:str=None,
        county:str=None,
        abstract:str=None,
        township:str=None,
        range:str=None,
        section:str=None,
        cumlative_oil:int=None,
        last_producing_month:str=None,
        cumoil_bblper1000ft:int=None,
        cumoil_bblperft:int=None
    ):
        self._api = api
        self._name = name
        self._direction = direction
        self._operator = operator
        self._status = status
        self._lease = lease
        self._interval = interval
        self._formation = formation
        self._first_production_date = first_production_date
        self._surface_latitude = surface_latitude
        self._surface_longitude = surface_longitude
        self._bottom_hole_latitude = bottom_hole_latitude
        self._bottom_hole_longitude = bottom_hole_longitude
        self._total_vertical_depth = total_vertical_depth
        self._measured_depth = measured_depth
        self._kelly_bushing_elevation = kelly_bushing_elevation
        self._lateral_length = lateral_length
        self._perf_interval = perf_interval
        self._proppant_intensity = proppant_intensity
        self._state = state
        self._county = county
        self._abstract = abstract
        self._township = township
        self._range = range
        self._section = section
        self._cumlative_oil = cumlative_oil
        self._last_producing_month = last_producing_month
        self._cumoil_bblper1000ft = cumoil_bblper1000ft
        self.cumoil_bblperft = cumoil_bblperft

    # Getters
    @property
    def api(self):
        return self._api

    @property
    def name(self):
        return self._name

    @property
    def direction(self):
        return self._direction

    @property
    def operator(self):
        return self._operator

    @property
    def status(self):
        return self._status
    
    @property
    def lease(self):
        return self._lease
    
    @property
    def interval(self):
        return self._interval

    @property
    def formation(self):
        return self._formation

    @property
    def first_production_date(self):
        return self._first_production_date

    @property
    def surface_latitude(self):
        return self._surface_latitude

    @property
    def surface_longitude(self):
        return self._surface_longitude

    @property
    def bottom_hole_latitude(self):
        return self._bottom_hole_latitude

    @property
    def bottom_hole_longitude(self):
        return self._bottom_hole_longitude

    @property
    def total_vertical_depth(self):
        return self._total_vertical_depth

    @property
    def measured_depth(self):
        return self._measured_depth

    @property
    def kelly_bushing_elevation(self):
        return self._kelly_bushing_elevation

    @property
    def lateral_length(self):
        return self._lateral_length

    @property
    def perf_interval(self):
        return self._perf_interval
    
    @property
    def proppant_intensity(self):
        return self._proppant_intensity
    
    @property
    def state(self):
        return self._state
    
    @property
    def county(self):
        return self._county

    @property
    def abstract(self):
        return self._abstract
    
    @property
    def township(self):
        return self._township
    
    @property
    def range(self):
        return self._range
    
    @property
    def section(self):
        return self._section
    
    # Setters
    @api.setter
    def api(self, value):
        self._api = value

    @name.setter
    def name(self, value):
        self._name = value

    @direction.setter
    def direction(self, value):
        self._direction = value

    @operator.setter
    def operator(self, value):
        self._operator = value

    @status.setter
    def status(self, value):
        self._status = value
        
    @lease.setter
    def lease(self, value):
        self._lease = value

    @interval.setter
    def interval(self, value):
        self._interval = value

    @formation.setter
    def formation(self, value):
        self._formation = value

    @first_production_date.setter
    def first_production_date(self, value):
        self._first_production_date = value

    @surface_latitude.setter
    def surface_latitude(self, value):
        self._surface_latitude = value

    @surface_longitude.setter
    def surface_longitude(self, value):
        self._surface_longitude = value

    @bottom_hole_latitude.setter
    def bottom_hole_latitude(self, value):
        self._bottom_hole_latitude = value

    @bottom_hole_longitude.setter
    def bottom_hole_longitude(self, value):
        self._bottom_hole_longitude = value

    @total_vertical_depth.setter
    def total_vertical_depth(self, value):
        self._total_vertical_depth = value

    @measured_depth.setter
    def measured_depth(self, value):
        self._measured_depth = value

    @kelly_bushing_elevation.setter
    def kelly_bushing_elevation(self, value):
        self._kelly_bushing_elevation = value

    @lateral_length.setter
    def lateral_length(self, value):
        self._lateral_length = value

    @perf_interval.setter
    def perf_interval(self, value):
        self._perf_interval = value

    @proppant_intensity.setter
    def proppant_intensity(self, value):
        self._proppant_intensity = value

    @state.setter
    def state(self, value):
        self._state = value

    @county.setter
    def county(self, value):
        self._county = value

    @abstract.setter
    def abstract(self, value):
        self._abstract = value

    @township.setter
    def township(self, value):
        self._township = value

    @range.setter
    def range(self, value):
        self._range = value

    @section.setter
    def section(self, value):
        self._section = value

    @property
    def cumlative_oil(self):
        return self._cumlative_oil
    
    @cumlative_oil.setter
    def cumlative_oil(self, value):
        self._cumlative_oil = value

    @property
    def last_producing_month(self):
        return self._last_producing_month
    
    @last_producing_month.setter
    def last_producing_month(self, value):
        self._last_producing_month = value

    @property
    def cumlative_oil(self):
        return self._cumlative_oil
    
    @cumlative_oil.setter
    def cumlative_oil(self, value):
        self._cumlative_oil = value
    
    @property
    def cumoil_bblper1000ft(self):
        return self._cumoil_bblper1000ft
    
    @cumoil_bblper1000ft.setter
    def cumoil_bblper1000ft(self, value):
        self._cumoil_bblper1000ft = value
        
    @property
    def cumoil_bblperft(self):
        return self._cumoil_bblperft
    
    @cumoil_bblperft.setter
    def cumoil_bblperft(self, value):
        self._cumoil_bblperft = value